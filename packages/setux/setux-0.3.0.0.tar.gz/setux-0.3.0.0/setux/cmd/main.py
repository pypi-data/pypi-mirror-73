from sys import path, argv
from os import getcwd

from . import commands
from .repl import repl
from .target import get_target
from .usage import usage


def main():
    path.insert(0, getcwd())

    if len(argv)>1:
        name = argv[1]
        if name in ('usage', 'help', '?'): return usage()
        if name.startswith('-'): return usage()
        cmd = commands.get(name)
    else:
        cmd = None

    if cmd:
        target, args = None, argv[2:]
        if args:
            target = get_target(args[-1])
            if target:
                args = args[:-1]
        if not target:
            target = get_target()
        cmd(target, ' '.join(args))
    else:
        target = get_target(argv[1] if len(argv)>1 else None)
        repl(target)
