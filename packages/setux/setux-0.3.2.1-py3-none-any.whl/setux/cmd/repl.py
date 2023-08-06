from cmd import Cmd

from setux import banner
from . import commands


def safe(cmd, target):
    def do_cmd(arg):
        try:
            cmd(target, arg)
        except Exception as x:
            print(type(x).__name__, x)
    return do_cmd


class Repl(Cmd):
    def __init__(self, target):
        super().__init__()
        user = 'sudo' if target.sudo else target.distro.Login.name
        self.prompt = f'{target.name}:{user} > '
        for name, cmd in commands.items():
            setattr(self, f'do_{name}', safe(cmd, target))

    def preloop(self):
        print(banner)
        self.onecmd('infos')
        print()

    def default(self, line):
        self.onecmd(f'run {line}')

    def do_EOF(self, arg):
        return True


def repl(target):
    Repl(target).cmdloop()
