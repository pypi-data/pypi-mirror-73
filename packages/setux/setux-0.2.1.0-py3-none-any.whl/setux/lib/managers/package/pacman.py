from setux.logger import debug, error, exception, info

from setux.core.package import Packager


class Pacman(Packager):

    def do_init(self):
        # self.do_cleanup()
        self.do_update()
        self.run(f'pacman --no-confirm -Sq yay')

    def do_installed(self):
        ret, out, err = self.run(f'pacman -Qe', report='quiet')
        for line in out:
            try:
                name, ver = line.split()
                yield name, ver
            except: pass

    def do_available(self):
        ret, out, err = self.run(f'pacman -Ssq', report='quiet')
        for line in out:
            try:
                name, ver = line.split()
                yield name, ver
            except: pass

    def do_remove(self, pkg):
        self.run(f'pacman --no-confirm -Rs {pkg}')

    def do_cleanup(self):
        self.run('pacman --noconfirm -Rcsun $(pacman -Qdtq)')
        self.run('pacman --noconfirm -Scc')

    def do_update(self):
        self.run('pacman -Syu')

    def do_install(self, pkg, ver=None):
        # self.run(f'pacman -S --needed --noconfirm {pkg}')
        ret, out, err = self.run(f'yay -S --needed --noconfirm {pkg}')
        if err:
            msg = '\n'.join(err)
            debug(msg) if ret==0 else error(msg)

