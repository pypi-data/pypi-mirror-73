from .manager import Manager, RestartPolicy
from .logger import logger
from logging import StreamHandler, INFO
from argparse import ArgumentParser
from importlib import import_module
from time import sleep 
from signal import signal, SIGINT
import sys

MONITOR_CYCLE = 0.5

logger.addHandler(StreamHandler())
logger.setLevel(INFO)

parser = ArgumentParser()
parser.add_argument("target")
parser.add_argument("-w", "--workers", default = 1, type = int)
parser.add_argument("-p", "--preload", action="store_true")
parser.add_argument("-r", "--restart_policy", 
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

def run():
    hdlr = Handler()
    signal(SIGINT, hdlr)
    sys.path.insert(0, "")
    args = parser.parse_args()
    module = args.target.split(":")[0]
    if args.preload:
        import_module(module)
    with Manager(args.target, workers = args.workers, restart_policy = RestartPolicy[args.restart_policy]) as mgr:
        while not hdlr.terminate:
            sleep(MONITOR_CYCLE)
            mgr.monitor()

if __name__ == "__main__":
    run()