
from stc_handler import StcHandler

from cloudshell.traffic.driver import TrafficControllerDriver


class TestCenterControllerDriver(TrafficControllerDriver):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.handler = StcHandler()

    def load_config(self, context, stc_config_file_name):
        """ Load STC configuration file and reserve ports.

        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        :param stc_config_file_name: Full path to STC configuration file name - tcc or xml
        """

        super(self.__class__, self).load_config(context)
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

    def sequencer_command(self, context, command):
        """ Get view statistics.

        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        :param command: from GUI - Start/Stop/Wait, from API also available Step/Pause.
        """

        self.handler.sequencer_command(command)

    #
    # Parent commands are not visible so we re define them in child.
    #

    def initialize(self, context):
        super(self.__class__, self).initialize(context)

    def cleanup(self):
        super(self.__class__, self).cleanup()

    def keep_alive(self, context, cancellation_context):
        super(self.__class__, self).keep_alive(context, cancellation_context)

    #
    # Hidden commands for developers only.
    #

    def get_session_id(self, context):
        """ Returns the REST session ID.

        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        return self.handler.get_session_id()

    def get_children(self, context, obj_ref, children_type=''):
        """ Returns all children of object.

        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        :param obj_ref: valid STC object reference.
        :param children_type: requested children type. If None returns all children.
        :return: list of children.
        """

        return self.handler.get_children(obj_ref, children_type)

    def get_attributes(self, context, obj_ref):
        """ Returns all children of object.

        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        :param obj_ref: valid STC object reference.
        :return: list of <attribute, value>.
        """

        return self.handler.get_attributes(obj_ref)

    def set_attribute(self, context, obj_ref, attr_name, attr_value):
        """ Set object attribute.

        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        :param obj_ref: valid STC object reference.
        :param attr_name: STC attribue name.
        :param attr_value: STC attribue value.
        """

        self.handler.set_attribute(obj_ref, attr_name, attr_value)

    def perform_command(self, context, command, parameters_json):
        """ Set object attribute.

        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        :param command: valid STC object reference.
        :param parameters_json: parameters dict {name: value} as serialized json.
        """

        return self.handler.perform_command(command, parameters_json)
