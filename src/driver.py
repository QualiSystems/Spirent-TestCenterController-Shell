
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface

from stc_handler import StcHandler
import sys
from cloudshell.shell.core.driver_context import CancellationContext
from cloudshell.shell.core.context_utils import get_resource_name

class TestCenterControllerDriver(ResourceDriverInterface):

    def __init__(self):
        self.handler = StcHandler()


    def initialize(self, context):
        """
        :param context: ResourceCommandContext,ReservationContextDetailsobject with all Resource Attributes inside
        :type context:  context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        self.handler.initialize(context)




    def get_inventory(self, context):
        """ Return device structure with all standard attributes

        :type context: cloudshell.shell.core.driver_context.AutoLoadCommandContext
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """

        return self.handler.get_inventory(context)

    def load_config(self, context, stc_config_file_name, get_data_from_config):
        """ Load STC configuration file and reserve ports.
        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        :param stc_config_file_name: full path to STC configuration file (tcc or xml)
        :param get_data_from_config: True - reserve physical ports saved in the configuration file
                                     False - reserve physical ports from sandbox.
        """

        my_api = self.handler.get_api(context)
        reservation_id = context.reservation.reservation_id
        resource_name = get_resource_name(context=context)
        my_api.EnqueueCommand(reservationId=reservation_id,targetName=resource_name,commandName="keep_alive", targetType="Resource")

        self.handler.load_config(context, stc_config_file_name, get_data_from_config)
        return ""

    def send_arp(self, context):
        """ Send ARP for all objects (ports, devices, streams)
        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        self.handler.send_arp(context)
        return ""

    def start_devices(self, context):
        """
        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        self.handler.start_devices(context)
        return ""

    def stop_devices(self, context):
        """
        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        self.handler.stop_devices(context)

    def start_traffic(self, context):
        """
        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        self.handler.start_traffic(context)

    def stop_traffic(self, context):
        """
        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        self.handler.stop_traffic()

    def get_statistics(self, context, view_name, output_type):
        self.handler.get_statistics(context, view_name, output_type)
        return ""

    def cleanup(self):

        pass
        #self.handler.tearDown()

    def keep_alive(self, context, cancellation_context):

        while not cancellation_context.is_cancelled:
            pass
        if cancellation_context.is_cancelled:
            self.handler.tearDown()
            sys.exit(0)



