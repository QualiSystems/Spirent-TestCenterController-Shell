
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface

from stc_handler import StcHandler

import sys
sys.path.append('E:/eclipse64/plugins/org.python.pydev_3.1.0.201312121632/pysrc')


class TestCenterControllerDriver(ResourceDriverInterface):

    def __init__(self):
        self.handler = StcHandler()

    def initialize(self, context):
        """
        :param ResourceCommandContext ,ReservationContextDetails context: ResourceCommandContext,ReservationContextDetailsobject with all Resource Attributes inside
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """
        self.handler.initialize(context)

    def get_inventory(self, context):
        """ Return device structure with all standard attributes

        :type context: cloudshell.shell.core.driver_context.AutoLoadCommandContext
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """
        return self.handler.get_inventory(context)

    def load_config(self, context, stc_config_file_name,get_data_from_config):
        """ Load STC configuration file and reserve ports.

        :param str stc_config_file_name: full path to STC configuration file (tcc or xml)
        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """
        self.handler.load_config(context, stc_config_file_name,get_data_from_config)

    def send_arp(self, context):
        """ Send ARP for all objects (ports, devices, streams)

        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """
        self.handler.send_arp(context)
        return "send_arp Success"

    def start_devices(self, context):
        """
        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """
        self.handler.start_devices(context)

    def stop_devices(self, context):
        """
        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        self.handler.stop_devices()

    def start_traffic(self, context):
        """
        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        self.handler.start_traffic()

    def stop_traffic(self, context):
        """
        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        self.handler.stop_traffic()

    def cleanup(self):
        pass
