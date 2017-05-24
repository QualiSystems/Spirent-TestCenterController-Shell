
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface

from stc_handler import StcHandler

import tg_helper


class TestCenterControllerDriver(ResourceDriverInterface):

    def __init__(self):
        self.status = "keep_alive"
        self.handler = StcHandler()

    def initialize(self, context):
        """
        :type context:  context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        self.handler.initialize(context.resource.attributes['Client Install Path'],
                                context.resource.attributes['Controller Address'])

    def load_config(self, context, stc_config_file_name):
        """ Load STC configuration file and reserve ports.

        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        :param stc_config_file_name: Full path to STC configuration file name - tcc or xml
        """

        tg_helper.enqueue_keep_alive(context)
        self.handler.load_config(context, stc_config_file_name)
        return stc_config_file_name + ' loaded, ports reserved'

    def send_arp(self, context):
        """ Send ARP/ND for all devices and streams

        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        self.handler.send_arp()

    def start_devices(self, context):
        """ Start all emulations on all devices

        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        self.handler.start_devices()

    def stop_devices(self, context):
        """ Stop all emulations on all devices

        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        self.handler.stop_devices()

    def start_traffic(self, context, blocking):
        """ Start traffic on all ports.

        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        :param blocking: True - return after traffic finish to run, False - return immediately.
        """

        self.handler.start_traffic(blocking)
        return 'traffic started in {} mode'.format(blocking)

    def stop_traffic(self, context):
        """ Stop traffic on all ports.

        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        self.handler.stop_traffic()

    def get_statistics(self, context, view_name, output_type):
        """ Get view statistics.

        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        :param view_name: generatorPortResults, analyzerPortResults etc.
        :param output_type: CSV or JSON.
        """

        return self.handler.get_statistics(context, view_name, output_type)

    def cleanup(self):
        self.handler.tearDown()

    def keep_alive(self, context, cancellation_context):
        while not cancellation_context.is_cancelled:
            pass
        if cancellation_context.is_cancelled:
            self.handler.tearDown()
