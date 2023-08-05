from setux.core.service import Service


class SystemV(Service):

    def do_status(self, svc):
        ret, out, err = self.run(
            f'service {svc} status',
        )
        return 'is running' in out[0]

    def do_restart(self, svc):
        ret, out, err = self.run(f'service {svc} restart')
