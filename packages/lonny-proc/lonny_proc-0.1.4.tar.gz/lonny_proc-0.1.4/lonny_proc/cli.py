from .manager import Manager, RestartPolicy
from .logger import logger
from logging import StreamHandler, INFO
from argparse import ArgumentParser
from importlib import import_module
from time import sleep 
from signal import signal, SIGINT, SIGTERM, SIG_IGN
import sys

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
        split = f"{target}:1".split(":")
        fn = import_module(split[0]).__getattribute__(split[1])
        for _ in range(int(split[2])):
            targets.append(fn)
    return targets

def run():
    sys.path.insert(0, "")
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