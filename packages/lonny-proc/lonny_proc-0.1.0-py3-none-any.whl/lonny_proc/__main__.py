from .manager import Manager, RestartPolicy
from .logger import logger
from logging import StreamHandler, INFO
from argparse import ArgumentParser
from importlib import import_module
from time import sleep 
from signal import signal, SIGINT, SIGTERM

MONITOR_CYCLE = 0.5

class Context:
    terminate = False

logger.addHandler(StreamHandler())
logger.setLevel(INFO)

parser = ArgumentParser()
parser.add_argument("targets", nargs = "+", type = str)
parser.add_argument("-p", "--policy", 
    type = str, 
    choices = list(x.name for x in RestartPolicy),
    default = RestartPolicy.never.name
)

args = parser.parse_args()

def handler(_sig, _frame):
    Context.terminate = True

signal(SIGINT, handler)
signal(SIGTERM, handler)

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

with Manager(* targets, restart_policy = RestartPolicy[args.policy]) as mgr:
    while not Context.terminate:
        sleep(MONITOR_CYCLE)
        mgr.monitor()