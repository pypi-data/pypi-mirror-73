from setux.core.service import Service


class SystemV(Service):

    def do_status(self, svc):
        ret, out, err = self.run(
            f'service {svc} status',
        )
        return 'is running' in out[0]

    def do_start(self, svc):
        ret, out, err = self.run(f'service {svc} start')

    def do_stop(self, svc):
        ret, out, err = self.run(f'service {svc} stop')

    def do_restart(self, svc):
        ret, out, err = self.run(f'service {svc} restart')

    def do_enable(self, svc):
        ret, out, err = self.run(f'update-rc.d {svc} enable')

    def do_disable(self, svc):
        ret, out, err = self.run(f'update-rc.d {svc} disable')
