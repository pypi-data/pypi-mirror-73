from argparse import ArgumentParser
from os import getenv
from json import loads
from .type import Proc, ProcSet, Machine
from .action import sync
from .logger import logger
from logging import StreamHandler, INFO

WEB_PROC = "web"

parser = ArgumentParser()
parser.add_argument("-f", "--procs_f", default = "procs.json")
parser.add_argument("-c", "--cluster", default = getenv("CLUSTER"))
parser.add_argument("-s", "--security_group", default = getenv("SECURITY_GROUP"))
parser.add_argument("-i", "--image", default = getenv("IMAGE"))
parser.add_argument("-a", "--subnet_a", default = getenv("SUBNET_A"))
parser.add_argument("-b", "--subnet_b", default = getenv("SUBNET_B"))
parser.add_argument("-r", "--role", default = getenv("ROLE"))
parser.add_argument("-n", "--namespace", default = "lonny-procs-")
parser.add_argument("-t", "--target_group", default = getenv("TARGET_GROUP"))
parser.add_argument("-p", "--port", default = int(getenv("PORT", 8080)))
parser.add_argument("-e", "--env", action = "append", default = list())

logger.setLevel(INFO)
logger.addHandler(StreamHandler())

args = parser.parse_args()

env_dict = dict()
for env in args.env:
    split = env.split("=")
    if len(split) == 1:
        raise ValueError("Invalid env argument specified")
    env_dict[split[0]] = env[len(split[0]) + 1:]

proc_set = ProcSet(
    cluster = args.cluster,
    security_group = args.security_group,
    subnet_a = args.subnet_a,
    subnet_b = args.subnet_b,
    role = args.role,
    environment = env_dict
)

with open(args.procs_f) as f:
    for name, proc_def in loads(f.read()).items():
        proc_set.add_proc(Proc(
            name = f"{args.namespace}{name}",
            machine = Machine[proc_def["machine"]],
            image = args.image,
            instances = proc_def["instances"],
            log_group = proc_def.get("log_group"),
            target_group = args.target_group,
            port = args.port,
            entry = proc_def["entry"]
        ))

sync(proc_set)

