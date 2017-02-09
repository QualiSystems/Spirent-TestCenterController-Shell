
import logging
import sys
from cloudshell.shell.core.driver_context import AutoLoadDetails

from testcenter.stc_app import StcApp
from trafficgenerator.tgn_tcl import TgnTkMultithread
from testcenter.api.stc_tcl import StcTclWrapper
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext
import re
import json
import csv
import io
from testcenter.stc_statistics_view import StcStats
import os


class StcHandler(object):

    def initialize(self, context):
        """
        :type context: cloudshell.shell.core.driver_context.InitCommandContext
        """
        curr_dir = os.getcwd()
        log_dir = curr_dir+'/Logs'
        log_file = 'STC_logger.log'
        client_install_path = context.resource.attributes['Client Install Path']
        logging.basicConfig(filename= log_file, level=logging.DEBUG)
        self.logger = logging.getLogger('root')
        self.logger.addHandler(logging.FileHandler(log_file))
        self.logger.setLevel('DEBUG')

        self.tcl_interp = TgnTkMultithread()
        self.tcl_interp.start()
        api_wrapper = StcTclWrapper(self.logger, client_install_path, self.tcl_interp)

        self.stc = StcApp(self.logger, api_wrapper)

        address = context.resource.address
        if address.lower() in ('na', 'localhost'):
            address = None
        self.logger.info("connecting to address {}".format(address))
        self.stc.connect(lab_server=address)

    def tearDown(self):
        self.tcl_interp.stop()

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
        try:
            self.stc.load_config(stc_config_file_name)
            self.ports = self.stc.project.get_ports()

            if get_data_from_config.lower() == 'false':
                reservation_id = context.reservation.reservation_id
                my_api = self.get_api(context)
                response = my_api.GetReservationDetails(reservationId=reservation_id)

                search_chassis = "Traffic Generator Chassis"
                search_port = "Port"
                chassis_objs_dict = dict()
                ports_obj = []

                for resource in response.ReservationDescription.Resources:
                    if resource.ResourceFamilyName == search_chassis:
                        chassis_objs_dict[resource.FullAddress] = {'chassis':resource,'ports':list()}
                for resource in response.ReservationDescription.Resources:
                    if resource.ResourceFamilyName == search_port:
                            chassis_adr = resource.FullAddress.split('/')[0]
                            if chassis_adr in chassis_objs_dict:
                                chassis_objs_dict[chassis_adr]['ports'].append(resource)
                                ports_obj.append(resource)

                ports_obj_dict = dict()
                for port in ports_obj:
                        val = my_api.GetAttributeValue(resourceFullPath=port.Name, attributeName="Logical Name").Value
                        if val:
                            port.logic_name = val
                            ports_obj_dict[val.lower().strip()] = port
                if not ports_obj_dict:
                    self.logger.error("You should add logical name for ports")
                    raise Exception("You should add logical name for ports")

                for port_name, port in self.ports.items():
                    # 'physical location in the form ip/module/port'
                    port_name = port_name.lower().strip()
                    if port_name in ports_obj_dict:
                        FullAddress = re.sub(r'PG.*?[^a-zA-Z0-9 ]', r'', ports_obj_dict[port_name].FullAddress)
                        physical_add = re.sub(r'[^./0-9 ]', r'', FullAddress)
                        self.logger.info("Logical Port %s will be reserved now on Physical location %s" %
                                         (str(port_name), str(physical_add)))
                        port.reserve(physical_add,force=True,wait_for_up=False)

            else:
                for port_name, port in self.ports.items():
                    # 'physical location in the form ip/module/port'
                    port.reserve(force=True,wait_for_up=False)

            self.logger.info("Port Reservation Completed")
        except Exception as e:
            self.tearDown()
            self.logger.error("Port Reservation Failed " + str(e))

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

    def start_traffic(self, context,blocking):
        """
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """
        blocking = bool(blocking) if blocking in ["true", "True"] else False
        self.stc.start_traffic(blocking)

    def stop_traffic(self, context):
        """
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """

        self.stc.stop_traffic()


    def get_statistics(self, context, view_name, output_type):
        output_file = output_type.lower().strip()
        if output_file != 'json' and output_file != 'csv':
            raise Exception("The output format should be json or csv")
        gen_stats = StcStats(view_name)
        gen_stats.read_stats()
        statistics = gen_stats.statistics
        reservation_id = context.reservation.reservation_id
        my_api = self.get_api(context)
        if output_file.lower() == 'json':
            statistics = json.dumps(statistics, indent=4, sort_keys=True,ensure_ascii=False)
            # print statistics
            my_api.WriteMessageToReservationOutput(reservation_id, statistics)
        elif output_file.lower() == 'csv':
            output = io.BytesIO()
            w = csv.DictWriter(output, statistics.keys())
            w.writeheader()
            w.writerow(statistics)

            my_api.WriteMessageToReservationOutput(reservation_id,output.getvalue().strip('\r\n'))


