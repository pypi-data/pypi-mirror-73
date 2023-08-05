import asyncio
import os.path
import logging
import shutil
import typing

from jinja2 import (
    Environment, FileSystemLoader, select_autoescape, sandbox
)
from time import monotonic

Env = typing.TypeVar("Env", Environment, sandbox.SandboxedEnvironment)
logger = logging.getLogger(__name__)


class Skeleton():
    """ A skeleton directory to create directories from.

    This supports copying and templating files.
    """

    def __init__(
        self,
        path: str,
        template_extensions: typing.List[str] = ["j2"],
        raw_paths: typing.Sequence[str] = [],
        excluded_paths: typing.Sequence[str] = [],
        variables: typing.Dict[str, typing.Any] = {},
        dir_mode: str = "0o1700",
        workers: int = 8,
        environment: Env = None,
    ):

        self.root = os.path.realpath(path)
        self.raw_paths = frozenset(raw_paths)
        self.excluded_paths = frozenset(excluded_paths)
        self.dir_mode = int(dir_mode, 8)
        self.workers = workers

        if not environment:
            # TODO: Use sandbox
            environment = Environment(
                loader=FileSystemLoader(self.root),
                autoescape=select_autoescape(["html", "xml"]),

            )

        if variables:
            environment.globals.update(variables)

        self.environment = environment
        self.template_extensions = tuple(map(
            lambda ext: ext if ext.startswith(".") else f".{ext}",
            template_extensions
        ))

    def render_source(
        self,
        source: str,
        target: str,
        variables: typing.Dict[str, typing.Any] = {},
        force: bool = False
    ) -> str:
        """ Render and write a template to a target file.
        """

        if os.path.exists(target) and not force:
            return

        template = self.environment.get_template(source)

        with open(target, "wb") as outfile:
            for line in template.generate(variables):
                outfile.write(line.encode("utf-8"))

        return target

    def copy_source(
        self,
        source: str,
        target: str,
        force: bool = False
    ) -> str:
        """ Copy a file from the skeleton directory to the target directory.
        """

        if os.path.exists(target) and not force:
            return

        shutil.copy(os.path.join(self.root, source), target)

        return target

    def mkdir(
        self,
        target: str,
        mode: str = None
    ):
        if os.path.exists(target):
            return

        if mode is None:
            mode = self.dir_mode

        # TODO: Set exist_ok=True to avoid failing on race conditions?
        os.makedirs(target, mode=mode)

    def process_source_file(
        self,
        source: str,
        target_root: str,
        variables: typing.Dict[str, typing.Any] = {},
        force: bool = False
    ) -> str:
        """ Create a file under `target_root` from a template or raw file.
        """

        target = os.path.join(target_root, source)

        if source in self.excluded_paths:
            logger.debug(f"excluding {os.path.join(self.root, source)}")
            return

        self.mkdir(os.path.dirname(target))

        result = None

        if source in self.raw_paths or \
                os.path.splitext(source)[1] not in self.template_extensions:
            result = self.copy_source(source, target, force)
        else:
            result = self.render_source(
                source, os.path.splitext(target)[0], variables, force
            )

        return result

    async def _worker(
        self,
        work_queue: asyncio.Queue,
        target_root: str,
        variables: typing.Dict[str, typing.Any] = {},
        force: bool = False
    ):
        while True:
            source = await work_queue.get()
            try:

                result = self.process_source_file(
                    source, target_root, variables, force
                )

                if result is not None:
                    logger.debug(
                        f"created {result} "
                        f"(source: {os.path.join(self.root, source)})"
                    )

            finally:
                work_queue.task_done()

    async def create_async(
        self,
        target_root: str,
        variables: typing.Dict[str, typing.Any] = {},
        workers: int = None,
        force: bool = False
    ) -> str:

        if workers is None:
            workers = self.workers

        if workers < 1:
            raise ValueError("there must be at least one worker.")

        target_path = os.path.realpath(target_root)
        logger.debug(f"creating {target_root} (workers: {workers})")

        queue = asyncio.Queue(workers)
        workers = tuple([
            asyncio.create_task(
                self._worker(queue, target_root, variables, force)
            ) for _ in range(workers)
        ])

        for source in self.environment.list_templates(
            filter_func=lambda path: True
        ):
            await queue.put(source)

        await queue.join()

        for worker in workers:
            worker.cancel()

        await asyncio.gather(*workers, return_exceptions=True)

        return target_path

    def create(
        self,
        target_root: str,
        variables: typing.Dict[str, typing.Any] = {},
        workers: int = None,
        force: bool = False
    ) -> str:
        """ Create the `target` directory from this Skeleton instance.

        """

        start_ts = monotonic()
        target = asyncio.run(
            self.create_async(target_root, variables, workers, force)
        )
        logger.info(f"created {target} in {monotonic() - start_ts} seconds")
        return target
