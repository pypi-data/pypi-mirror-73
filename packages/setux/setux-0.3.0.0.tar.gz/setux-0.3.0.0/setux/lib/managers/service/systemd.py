from setux.core.service import Service


class SystemD(Service):

    def do_status(self, svc):
        ret, out, err = self.run(
            f'systemctl -q --no-pager show {svc}',
            report='quiet',
        )
        rows = (i.split('=', 1) for i in out)
        data = dict(i for i in rows if len(i)==2)
        active = data['ActiveState']=='active'
        running = data['SubState']=='running'
        return active and running

    def do_start(self, svc):
        ret, out, err = self.run(f'systemctl start {svc}')

    def do_stop(self, svc):
        ret, out, err = self.run(f'systemctl stop {svc}')

    def do_restart(self, svc):
        ret, out, err = self.run(f'systemctl restart {svc}')

    def do_enable(self, svc):
        ret, out, err = self.run(f'systemctl enable {svc}')

    def do_disable(self, svc):
        ret, out, err = self.run(f'systemctl disable {svc}')

