import pkgutil

from cmp_ipproxy_lib import http_plugins

def install():
    for importer, modname, ispkg in pkgutil.iter_modules(http_plugins.__path__):
        plugin = importer.find_module(modname).load_module(modname)
        plugin.install()
