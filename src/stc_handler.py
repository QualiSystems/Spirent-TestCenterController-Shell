
import re
import json
import csv
import io
from collections import OrderedDict

from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext

from trafficgenerator.tgn_tcl import TgnTkMultithread
from testcenter.stc_app import StcApp
from testcenter.api.stc_tcl import StcTclWrapper
from testcenter.stc_statistics_view import StcStats

import tg_helper


class StcHandler(object):

    def initialize(self, client_install_path, lab_server=''):
        """
        :param client_install_path: full path to STC client installation directory (up to, including, version number)
        :param lab_server: lab server address (if required)
        """

        self.logger = tg_helper.create_logger('c:/temp/stc_controller_logger.txt')

        self.tcl_interp = TgnTkMultithread()
        self.tcl_interp.start()
        self.logger.debug('client_install_path = ' + client_install_path)
        api_wrapper = StcTclWrapper(self.logger, client_install_path, self.tcl_interp)
        self.stc = StcApp(self.logger, api_wrapper)
        self.stc.connect(lab_server=lab_server)

    def tearDown(self):
        self.tcl_interp.stop()

    def load_config(self, context, stc_config_file_name):
        """
        :param stc_config_file_name: full path to STC configuration file (tcc or xml)
        """

        self.stc.load_config(stc_config_file_name)
        config_ports = self.stc.project.get_ports()

        reservation_id = context.reservation.reservation_id
        my_api = CloudShellSessionContext(context).get_api()

        reservation_ports = {}
        for port in tg_helper.get_reservation_ports(my_api, reservation_id):
            reservation_ports[my_api.GetAttributeValue(port.Name, 'Logical Name').Value.strip()] = port

        for name, port in config_ports.items():
            if name in reservation_ports:
                address = tg_helper.get_address(reservation_ports[name])
                self.logger.debug('Logical Port {} will be reserved on Physical location {}'.format(name, address))
                port.reserve(address, force=True, wait_for_up=False)
            else:
                self.logger.error('Configuration port "{}" not found in reservation ports {}'.
                                  format(port, reservation_ports.keys()))
                raise Exception('Configuration port "{}" not found in reservation ports {}'.
                                format(port, reservation_ports.keys()))

        self.logger.info("Port Reservation Completed")

    def send_arp(self):
        self.stc.send_arp_ns()

    def start_devices(self):
        self.stc.start_devices()

    def stop_devices(self):
        self.stc.stop_devices()

    def start_traffic(self, blocking):
        """
        :param blocking: "True"/"False" - whether to run traffic in blocking mode or not.
        """
        self.stc.start_traffic(tg_helper.is_blocking(blocking))

    def stop_traffic(self):
        self.stc.stop_traffic()

    def get_statistics(self, context, view_name, output_type):
        """
        :param view_name: name of statistics view.
        :param output_type: "JSON"/"CSV"
        """

        stats_obj = StcStats(view_name)
        stats_obj.read_stats()
        statistics_ = stats_obj.statistics

        if output_type.strip().lower() == 'json':
            statistics_str = json.dumps(statistics_, indent=4, sort_keys=True, ensure_ascii=False)
            return json.loads(statistics_str)
        elif output_type.strip().lower() == 'csv':
            statistics = OrderedDict()
            for obj_name in statistics_['topLevelName']:
                statistics[obj_name] = stats_obj.get_object_stats(obj_name)
            captions = statistics[statistics_['topLevelName'][0]].keys()
            output = io.BytesIO()
            w = csv.DictWriter(output, captions)
            w.writeheader()
            for obj_name in statistics:
                w.writerow(statistics[obj_name])
            tg_helper.attach_stats_csv(context, self.logger, view_name, output.getvalue().strip())
            return output.getvalue().strip()
        else:
            raise Exception('Output type should be CSV/JSON - got "{}"'.format(output_type))
