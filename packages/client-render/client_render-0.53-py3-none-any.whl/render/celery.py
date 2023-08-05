import glob
import itertools
import logging
import os
import re
import shutil
import zipfile
from datetime import datetime
from pathlib import Path, PurePosixPath
from subprocess import Popen, PIPE, STDOUT

from celery import Celery

from render import RENDER_DIR, LOG_DIR
from render.logger import configure_logger
from render.s3 import S3, AWS_S3
from render.watch.logs import collect_instance_logs

celery = Celery()
celery.config_from_object('render.celeryconfig')

logger = logging.getLogger(__name__)


class FollowLog:
    BATCH_RENDER_NAME = re.compile(r'Batch render job being rendered:(.*)')
    COMPLETE = re.compile(r'Job Complete - Results in')

    def __init__(self, workdir: Path, extension: str):
        self.buffer = []
        self.current_view = self.next_handler = None
        assert workdir
        assert extension
        self.workdir = workdir
        self.extension = extension

        self.handlers = itertools.cycle([
            self.BATCH_RENDER_NAME, self.COMPLETE
        ])
        self.next()

    def clear(self):
        self.buffer = []

    @property
    def to_str(self):
        return ''.join(self.buffer)

    def next(self):
        self.clear()
        self.next_handler = next(self.handlers)
        logger.info(f'Following pattern "{self.next_handler.pattern}"')

    def make_view_dir(self):
        directory = self.workdir / self.current_view
        directory.mkdir(exist_ok=True)
        logger.info(f"Created directory - {directory}")

    def move_files(self):
        assert self.current_view
        dest_directory = self.workdir / self.current_view
        pattern = str(self.workdir / f'*.{self.extension}')
        for file in glob.glob(pattern):
            filename = os.path.basename(file)
            dst_filename = dest_directory / filename
            shutil.move(file, dst_filename)
            logger.info(f"File {filename} moved into {dest_directory}")

            yield dst_filename

    def process(self, s):
        self.buffer.append(s)
        matched = self.next_handler.search(self.to_str)
        if matched:
            if self.next_handler == self.BATCH_RENDER_NAME:
                self.current_view = matched.group(1).strip()
                self.make_view_dir()

            if self.next_handler == self.COMPLETE:
                yield from self.move_files()

            self.next()

    def iterate_files(self, stdout):
        # noinspection PyTypeChecker
        with open(self.workdir / 'rendering.log', 'wb') as f:
            for s in stdout:
                # remove ASCII NULL symbol inplace
                part = s.replace(b'\x00', b'')
                f.write(part)
                f.flush()

                yield from self.process(part.decode())


class Key:
    def __init__(self, key: str):
        self.path = PurePosixPath(key)

    @property
    def task_id(self):
        return self.path.parent

    @property
    def workdir(self):
        directory = RENDER_DIR / self.task_id.name
        directory.mkdir(exist_ok=True)
        return directory

    @property
    def filename(self):
        return self.path.name

    @property
    def localfile(self):
        return self.workdir / 'scene' / self.filename


class Texture(Key):
    @property
    def dst(self):
        return self.workdir / 'maps'


class Render:
    def __init__(self, scene: Key, client: S3, texture: str = None):
        self.scene = scene
        self.client = client
        self.texture = texture and Texture(texture)

    def unpack_texture(self):
        if self.texture:
            self.client.download_file(self.texture.path, self.texture.localfile)
            logger.info(f"Texture downloaded - {self.texture.localfile}")
            self.texture.dst.mkdir(exist_ok=True)
            with zipfile.ZipFile(self.texture.localfile, 'r') as f:
                f.extractall(self.texture.dst)
            logger.info(f"Texture unzipped to - {self.texture.dst}")

    def run(self, extension='exr'):
        self.unpack_texture()
        self.client.download_file(self.scene.path, self.scene.localfile)
        logger.info(f"Scene downloaded - {self.scene.localfile}")
        if not self.scene.localfile.is_file():
            raise Exception("Local file does not exists")

        max_cmd = Path(os.environ['ADSK_3DSMAX_x64_2018']) / '3dsmaxcmd'
        args = [
            str(max_cmd),
            "-continueOnError",
            "-batchRender",
            f'-outputName:{str(self.scene.workdir / f"0.{extension}")}',
        ]
        if self.texture:
            logger.debug(f"Using textures: {list(self.texture.dst.glob('*'))}")
            args.append(f'-bitmapPath:{self.texture.dst}')
        args.append(str(self.scene.localfile))
        logger.debug(f"Params = {args}")

        process = Popen(args, stderr=STDOUT, stdout=PIPE, bufsize=1)
        follow = FollowLog(self.scene.workdir, extension)
        for file in follow.iterate_files(process.stdout):
            view = file.parent.name
            self.client.upload_file(
                self.scene.task_id / 'result' / view / file.name,
                file
            )
            logger.info(f"Artifact is uploaded - {file}")
        process.wait()
        return process.returncode


def record_time(f):
    def wrapper(*args, **kwargs):
        begin = datetime.now()
        logger.info(f"Rendering is started!")
        try:
            return f(*args, **kwargs)
        finally:
            end = datetime.now()
            logger.info(f"Rendering is finished!")
            logger.info(f"Took: {str(end - begin).split('.')[0]}")

    return wrapper


def collect_logs(scene: Key, client: S3):
    logger.info("Collecting log files...")
    for file in itertools.chain(
            # additional logs could be appended here
            glob.glob(str(LOG_DIR / '*.log')),
            glob.glob(str(scene.workdir / '*.log')),
    ):
        logger.info(f"Found log {file}")
        client.upload_file(
            scene.task_id / 'logs' / os.path.basename(file),
            file
        )


def run(scene_key, texture=None):
    assert os.environ['ADSK_3DSMAX_x64_2018'], "ADSK_3DSMAX_x64_2018 must be defined"

    s3 = AWS_S3()
    scene = Key(scene_key)
    # configure current logger for the specific scene
    configure_logger(scene.workdir / 'task.log')

    render = Render(scene, s3, texture)
    try:
        rc = record_time(render.run)()
        if rc > 0:
            raise Exception(f"3dsmax returned non zero code {rc}")
    except Exception as e:
        logger.exception(e)
        raise
    finally:
        collect_logs(scene, s3)
        collect_instance_logs(s3)


celery.task(name="run")(run)
