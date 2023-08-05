def infos(target, arg):
    target.deploy('.infos')

def add(target, arg):
    target.modules.add(arg)

def deploy(target, arg):
    target.deploy(arg)

def remote(target, arg):
    target.remote(arg)

def run(target, arg):
    target(arg)

def install(target, arg):
    target.Package.install(arg)

def remove(target, arg):
    target.Package.remove(arg)

def start(target, arg):
    target.Service.start(arg)

def stop(target, arg):
    target.Service.stop(arg)

def restart(target, arg):
    target.Service.restart(arg)
