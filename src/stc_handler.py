
import logging

from cloudshell.shell.core.driver_context import AutoLoadDetails

from testcenter.stc_app import StcApp
from testcenter.api.stc_tcl import StcTclWrapper
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext
import re,json,csv,io
from testcenter.stc_statistics_view import StcStats

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

    def get_api(self, context):
        """

        :param context:
        :return:
        """

        return CloudShellSessionContext(context).get_api()

    def load_config(self, context, stc_config_file_name, get_data_from_config=False):
        """
        :param str stc_config_file_name: full path to STC configuration file (tcc or xml)
        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """
        self.stc.load_config(stc_config_file_name)
        self.ports = self.stc.project.get_ports()

        if not get_data_from_config:
            reservation_id = context.reservation.reservation_id
            my_api = self.get_api(context)
            response = my_api.GetReservationDetails(reservationId=reservation_id)

            search_chassis = "Traffic Generator Chassis"
            search_port = "Port"
            chassis_obj = None
            ports_obj = []

            for resource in response.ReservationDescription.Resources:
                if resource.ResourceFamilyName == search_chassis:
                    chassis_obj = resource
                if resource.ResourceFamilyName == search_port:
                    ports_obj.append(resource)

            ports_obj_dict = dict()

            for port in ports_obj:
                if (chassis_obj.FullAddress in port.FullAddress):
                    val = my_api.GetAttributeValue(resourceFullPath=port.Name, attributeName="Logical Name").Value
                    if val:
                        port.logic_name = val
                        ports_obj_dict[val.lower().strip()] = port



            for port_name, port in self.ports.items():
                # 'physical location in the form ip/module/port'
                port_name = port_name.lower().strip()
                if port_name in ports_obj_dict:
                    FullAddress = re.sub(r'PG.*?[^a-zA-Z0-9 ]', r'', ports_obj_dict[port_name].FullAddress)
                    physical_add = re.sub(r'[^./0-9 ]', r'', FullAddress)
                    self.logger.info("Logical Port %s will be reserved now on Physical location %s"%(port_name,physical_add))
                    try:
                        port.reserve(physical_add)
                    except Exception as e:
                        raise("Error: %s:"%(e))
            if not ports_obj_dict:
                self.logger.error("You should add logical name for ports")
                raise ("You should add logical name for ports")
        else:
            for port_name, port in self.ports.items():
                # 'physical location in the form ip/module/port'
                try:
                    port.reserve(None)
                except Exception as e:
                    raise("Error: %s:"%(e))

        self.logger.info("Port Reservation Completed")


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

    def get_statistics(self, context,view_name,output_type):
        output_file = output_type.lower().strip()
        if (output_file!='json' and output_file!='csv'):
            raise Exception("The output format should be json or csv")
        gen_stats = StcStats(view_name)
        gen_stats.read_stats()
        statistics =  gen_stats.statistics
        my_api = self.get_api(context)
        if(output_file.lower()=='json'):
            statistics = json.dumps(statistics, ensure_ascii=False)

            my_api.WriteMessageToReservationOutput(statistics)
        elif (output_file.lower()=='csv'):
            output = io.BytesIO()
            w = csv.DictWriter(output, statistics.keys())
            w.writeheader()
            w.writerow(statistics)
            my_api.WriteMessageToReservationOutput(output.getvalue())


