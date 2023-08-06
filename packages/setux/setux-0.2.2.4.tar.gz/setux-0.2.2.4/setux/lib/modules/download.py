from . import Module


class Distro(Module):
    def deploy(self, target, **kw):
        url, dst = kw['url'], kw['dst']
        try:
            target.run(f'curl -sfL {url} -o {dst}')
        except:
            target.run(f'wget -q {url} -O {dst}')
        return True

