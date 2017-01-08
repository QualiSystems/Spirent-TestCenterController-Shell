
import logging

from cloudshell.shell.core.driver_context import AutoLoadDetails

from testcenter.stc_app import StcApp
from testcenter.api.stc_tcl import StcTclWrapper


class StcHandler(object):

    def initialize(self, context):
        """
        :type context: cloudshell.shell.core.driver_context.InitCommandContext
        """

        client_install_path = context.resource.attributes['Client Install Path']
        self.logger = logging.getLogger('log')
        self.logger.setLevel('DEBUG')
        self.stc = StcApp(self.logger, StcTclWrapper(self.logger, client_install_path))
        address = context.resource.address
        if address.lower() in ('na', 'localhost'):
            address = None
        self.stc.connect(lab_server=address)

    def get_inventory(self, context):
        """
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        return AutoLoadDetails([], [])

    def load_config(self, context, stc_config_file_name):
        """
        :param str stc_config_file_name: full path to STC configuration file (tcc or xml)
        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        self.stc.load_config(stc_config_file_name)
        self.ports = self.stc.project.get_ports()
        self.ports['Logical name'].reserve('physical location in the form ip/module/port')

    def send_arp(self, context):
        """
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        self.stc.send_arp_ns()

    def start_devices(self, context):
        """
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        self.stc.start_devices()

    def stop_devices(self, context):
        """
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        self.stc.stop_devices()

    def start_traffic(self, context):
        """
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        self.stc.start_traffic()

    def stop_traffic(self, context):
        """
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        self.stc.stop_traffic()
