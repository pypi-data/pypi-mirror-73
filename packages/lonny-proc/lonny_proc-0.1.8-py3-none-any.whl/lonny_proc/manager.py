from enum import Enum, auto
from .logger import logger
from multiprocessing import Process
from importlib import import_module
from signal import signal, SIG_IGN, SIGINT

class RestartPolicy(Enum):
    never = auto()
    unless_error = auto()
    always = auto()

class CannotRecoverError(Exception):
    pass

def _build_target(target):
    def wrapped_target():
        signal(SIGINT, SIG_IGN)
        if isinstance(target, str):
            module, fn = target.split(":")
            import_module(module).__getattribute__(fn)()
        else:
            target()
    return wrapped_target

class Manager:
    def __init__(self, target, *, workers = 1, restart_policy = RestartPolicy.never):
        self._target = target
        self._workers = workers
        self._restart_policy = restart_policy
        self._procs = None

    def start(self):
        if self._procs is not None:
            return
        logger.info("Starting processes")
        target = _build_target(self._target)
        self._procs = [Process(target = target, args = ()) for _ in range(self._workers)]
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
        for ix, proc in enumerate(self._procs):
            if proc.is_alive():
                continue
            if self._can_restart(proc.exitcode):
                logger.info(f"Process: {ix} failed but can recover")
                target = _build_target(self._target)
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