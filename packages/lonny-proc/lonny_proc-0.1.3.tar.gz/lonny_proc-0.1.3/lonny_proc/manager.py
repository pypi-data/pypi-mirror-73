from enum import Enum, auto
from .logger import logger
from multiprocessing import Process

class RestartPolicy(Enum):
    never = auto()
    unless_error = auto()
    always = auto()

class CannotRecoverError(Exception):
    pass

class Manager:
    def __init__(self, * targets, restart_policy = RestartPolicy.never):
        self._targets = targets
        self._restart_policy = restart_policy
        self._procs = None

    def start(self):
        if self._procs is not None:
            return
        logger.info("Starting processes")
        self._procs = [Process(target = x, args = ()) for x in self._targets]
        for proc in self._procs:
            proc.start()

    def stop(self):
        if self._procs is None:
            return
        logger.info("Stopping processes")
        for proc in self._procs:
            proc.terminate()
        for proc in self._procs:
            proc.join()
        self._procs = None

    def _can_restart(self, code):
        if self._restart_policy == RestartPolicy.always:
            return True
        return self._restart_policy == RestartPolicy.unless_error and code == 0

    def monitor(self):
        for ix, target in enumerate(self._targets):
            proc = self._procs[ix]
            if proc.is_alive():
                continue
            if self._can_restart(proc.exitcode):
                logger.info(f"Process: {ix} failed but can recover")
                proc = Process(target = target, args = ())
                proc.start()
                self._procs[ix] = proc
                continue
            logger.error(f"Process: {ix} failed and cannot recover")
            raise CannotRecoverError()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.stop()