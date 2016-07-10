import logging
from inet.client import ns
from inet.utils.modpath import ModulePath

logger = logging.getLogger('inet.client')


class InetPath(ModulePath):

    def __call__(self, data):
        print(ns.get_address(self.path))
