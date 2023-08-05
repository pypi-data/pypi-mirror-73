from time import sleep

from setux.util import todo
from setux.logger import info
from setux.core.manage import Manager


class Service(Manager):
    def __init__(self, distro):
        super().__init__(distro)
        self.host = distro.Host.name
        self.svcmap = distro.svcmap

    def status(self, svc):
        name = self.svcmap.get(svc, svc)
        up = self.do_status(name)
        info(f'\tservice {svc} {"." if up else "X"}')
        return up

    def wait(self, svc):
        while not self.status(svc): sleep(2)

    def enable(self, svc):
        info(f'\tenable {svc}')
        name = self.svcmap.get(svc, svc)
        self.do_enable(svc)

    def disable(self, svc):
        info(f'\tdisable {svc}')
        name = self.svcmap.get(svc, svc)
        self.do_disable(svc)

    def start(self, svc):
        if not self.status(svc):
            info(f'\tstart {svc}')
            name = self.svcmap.get(svc, svc)
            self.do_start(svc)
            self.wait(svc)

    def stop(self, svc):
        if self.status(svc):
            info(f'\tstop {svc}')
            name = self.svcmap.get(svc, svc)
            self.do_stop(svc)

    def restart(self, svc):
        if self.status(svc):
            info(f'\trestart {svc}')
            name = self.svcmap.get(svc, svc)
            self.do_restart(svc)
            self.wait(svc)
        else:
            self.start(svc)

    def do_status(self, svc): todo(self)
    def do_enable(self, svc): todo(self)
    def do_disable(self, svc): todo(self)
    def do_start(self, svc): todo(self)
    def do_stop(self, svc): todo(self)
    def do_restart(self, svc): todo(self)
