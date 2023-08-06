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

    def do_restart(self, svc):
        ret, out, err = self.run(f'systemctl restart {svc}')
