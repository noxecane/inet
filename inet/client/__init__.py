import logging
from inet.utils.modpath import ModulePath

logger = logging.getLogger('inet.client')


class InetPath(ModulePath):

    def __call__(self, data):
        print(self.path)
