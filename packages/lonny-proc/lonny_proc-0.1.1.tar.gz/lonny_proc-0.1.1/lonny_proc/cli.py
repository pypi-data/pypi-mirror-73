from .manager import Manager, RestartPolicy
from .logger import logger
from logging import StreamHandler, INFO
from argparse import ArgumentParser
from importlib import import_module
from time import sleep 
from signal import signal, SIGINT, SIGTERM, SIG_IGN

MONITOR_CYCLE = 0.5

logger.addHandler(StreamHandler())
logger.setLevel(INFO)

parser = ArgumentParser()
parser.add_argument("targets", nargs = "+", type = str)
parser.add_argument("-p", "--policy", 
    type = str, 
    choices = list(x.name for x in RestartPolicy),
    default = RestartPolicy.never.name
)

class Handler:
    def __init__(self):
        self._terminate = False

    def __call__(self, _sig, _frame):
        self._terminate = True

    @property
    def terminate(self):
        return self._terminate

def _build_targets(args):
    targets = list()
    for target in args.targets:
        split = target.split(":")
        if len(split) == 2:
            module, fn = split
            copies = "1"
        elif len(split) == 3:
            module, fn, copies = split
        else:
            raise ValueError(f"{target} is not a valid target")
        target_fn = import_module(module).__getattribute__(fn)
        for _ in range(int(copies)):
            targets.append(target_fn)
    return targets

def run():
    hdlr = Handler()
    args = parser.parse_args()
    targets = _build_targets(args)
    # Child processes inherit the handlers of their parents. We want child
    # processes to ignore SIGINTs so we must set the parent handler as such
    # before the children are spawned.
    signal(SIGINT, SIG_IGN)
    with Manager(* targets, restart_policy = RestartPolicy[args.policy]) as mgr:
        # Now that the children are spawned, we can set the parent handlers to
        # whatever we want.
        signal(SIGINT, hdlr)
        signal(SIGTERM, hdlr)
        while not hdlr.terminate:
            sleep(MONITOR_CYCLE)
            mgr.monitor()