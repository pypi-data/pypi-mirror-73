from iotile.core.hw.proxy.proxy import TileBusProxyObject
from iotile.core.dev.semver import SemanticVersionRange
from typedargs.annotate import context, annotated
from iotile_support_lib_controller_4.remotebridge import RemoteBridgePlugin

@context("Boot52SafeMode")
class Boot52SafeMode(TileBusProxyObject):
    def __init__(self, stream, addr):
        super(Boot52SafeMode, self).__init__(stream, addr)
        self._trub = RemoteBridgePlugin(self)

    @classmethod
    def ModuleName(cls):
        return 'boot52'

    @classmethod
    def ModuleVersion(cls):
        return SemanticVersionRange.FromString('^3.1.0')

    @annotated
    def remote_bridge(self):
        return self._trub
