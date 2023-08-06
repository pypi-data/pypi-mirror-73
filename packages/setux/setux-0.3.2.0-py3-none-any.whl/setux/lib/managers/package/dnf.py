from setux.logger import error
from setux.core.package import Packager


class Dnf(Packager):

    def parse(self, line):
        name, ver, _ = line.split()
        name = name.split('.')[0]
        return name, ver

    def do_init(self):
        self.do_update()

    def do_installed(self):
        ret, out, err = self.run('dnf list --installed', report='quiet')
        for line in out:
            try:
                yield self.parse(line)
            except: pass

    def do_available(self):
        ret, out, err = self.run('dnf list --available', report='quiet')
        for line in out:
            try:
                yield self.parse(line)
            except: pass

    def do_remove(self, pkg):
        self.run(f'dnf -y remove {pkg}')

    def do_cleanup(self):
        self.run('dnf clean all')

    def do_update(self):
        self.run('dnf update -y')

    def do_upgrade(self):
        self.run('dnf upgrade -y')

    def do_install(self, pkg, ver=None):
        ver = f' ={ver}' if ver else ''
        ret, out, err = self.run(f'dnf -y -C install {pkg}{ver}')
        if ret==1:
            ret, out, err = self.run(f'dnf -y install {pkg}{ver}')
        if err: error('\n'.join(err))
