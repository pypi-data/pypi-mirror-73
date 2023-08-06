def run(target, arg):
    target(arg)

def infos(target, arg):
    target.deploy('.infos')

def add(target, arg):
    target.modules.add(arg)

def deploy(target, arg):
    target.deploy(arg)

def remote(target, arg):
    target.remote(arg)

def update(target, arg):
    target.Package.update()

def installed(target, arg):
    target.Package.installed(arg)

def available(target, arg):
    target.Package.available(arg)

def install(target, arg):
    target.Package.install(arg)

def remove(target, arg):
    target.Package.remove(arg)

def status(target, arg):
    target.Service.status(arg)

def start(target, arg):
    target.Service.start(arg)

def stop(target, arg):
    target.Service.stop(arg)

def restart(target, arg):
    target.Service.restart(arg)

def enable(target, arg):
    target.Service.enable(arg)

def disable(target, arg):
    target.Service.disable(arg)

