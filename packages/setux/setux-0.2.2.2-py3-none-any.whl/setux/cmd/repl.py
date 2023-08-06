from cmd import Cmd
from functools import partial

from setux import banner
from . import commands


class Repl(Cmd):
    def __init__(self, target):
        super().__init__()
        user = 'sudo' if target.sudo else target.distro.Login.name
        self.prompt = f'{target.name}:{user} > '
        for name, cmd in commands.items():
            setattr(self, f'do_{name}', partial(cmd, target))

    def preloop(self):
        print(banner)
        self.onecmd('infos')
        print()

    def default(self, line):
        self.onecmd(f'run {line}')


def repl(target):
    Repl(target).cmdloop()
