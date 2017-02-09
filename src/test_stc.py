#!/usr/bin/python
# -*- coding: utf-8 -*-
from cloudshell.shell.core.context import ResourceCommandContext, ResourceContextDetails, ReservationContextDetails,ConnectivityContext
from driver import TestCenterControllerDriver
import thread



def create_context():
    context = ResourceCommandContext()
    context.resource = ResourceContextDetails()
    context.resource.name = 'TestCenter Controller 1'
    context.reservation = ReservationContextDetails()
    context.reservation.reservation_id = 'bc3aa7d1-7d66-4365-b419-65b90ece4d0f'
    context.reservation.owner_user = 'admin'
    context.reservation.owner_email = 'fake@qualisystems.com'
    context.reservation.environment_path ='config1'
    context.reservation.environment_name = 'config1'
    context.reservation.domain = 'Global'
    context.resource.attributes = {}
    context.resource.attributes['Client Install Path'] = 'C:\Program Files (x86)\Spirent Communications\Spirent TestCenter 4.52'
    context.resource.address = 'localhost'
    return context


'''
    context.connectivity = ConnectivityContext()
    context.connectivity.admin_auth_token = 'T1dkw4LLJUSmWDpolusJdw=='
    context.connectivity.cloudshell_api_port = '8029'
    context.connectivity.quali_api_port= '9000'

    context.connectivity.server_address='localhost'
    context.description ={}
    context.description['family'] = 'Router'
    context.description['fullname'] = 'Huawei37'
    context.description['id'] = 'b476fa1f-379e-435a-b35c-65e892e1c306'
    context.description['model'] = 'Huaewi VRP Router'
    context.description['name'] = 'Huawei37'

    context.description['type'] = 'Resource'

'''

#Access
request = """{
	"driverRequest": {
		"actions": [{
			"connectionId": "8ccac528-2ff9-4b6d-9415-9dd68ac390c6",
			"connectionParams": {
				"vlanId": "23",
				"mode": "Trunk",
				"vlanServiceAttributes": [{
					"attributeName": "QnQ",
					"attributeValue": "False",
					"type": "vlanServiceAttribute"
				}, {
					"attributeName": "CTag",
					"attributeValue": "",
					"type": "vlanServiceAttribute"
				}, {
					"attributeName": "Isolation Level",
					"attributeValue": "Shared",
					"type": "vlanServiceAttribute"
				}, {
					"attributeName": "Access Mode",
					"attributeValue": "Access",
					"type": "vlanServiceAttribute"
				}, {
					"attributeName": "VLAN ID",
					"attributeValue": "23",
					"type": "vlanServiceAttribute"
				}, {
					"attributeName": "Pool Name",
					"attributeValue": "",
					"type": "vlanServiceAttribute"
				}, {
					"attributeName": "Virtual Network",
					"attributeValue": "23",
					"type": "vlanServiceAttribute"
				}],
				"type": "setVlanParameter"
			},
			"connectorAttributes": [],
			"actionId": "8ccac528-2ff9-4b6d-9415-9dd68ac390c6_ef6ea31d-40fc-4044-ae80-82fa74dfa695",
			"actionTarget": {
				"fullName": "Huawei37/Chassis 1/Module 0/GigabitEthernet1-0-0",
				"fullAddress": "172.19.47.74/1/0/0",
				"type": "actionTarget"
			},
			"customActionAttributes": [],
			"type": "removeVlan"
		}]
	}
}"""




if __name__ == '__main__':
    import time
    import threading
    context = create_context()
    driver = TestCenterControllerDriver()

    #response = driver.get_inventory(context)
    #res = driver.save(context, 'tftp://82.80.35.226/test', 'startup')
    #
    #res = driver.save(context, 'flash:/config_backup/','startup')
    #C:/Users/Administrator/Desktop/test
    #tftp://12.30.245.98/test/test.txt
    #res = driver.restore(context,'flash:/config_backup/vrpcfg.zip', 'startup', 'override')
    driver.initialize(context)
    #response = driver.get_inventory(context)
    #response = driver.ApplyConnectivityChanges(context,request)
    #response = driver.restore(context, 'cfcard:/config_backup/vrpcfg.zip', 'startup', 'override')
    #response = driver.save(context, 'tftp://172.19.107.44/test', 'startup')
    #response = driver.restore(context, 'cfcard:/config_backup/vrpcfg.zip', 'startup', 'override')
    #res = driver.ApplyConnectivityChanges(context, request)



    #t3 = threading.Thread(target=driver.send_arp, args=[context]).start()

    #threading.Thread(target=driver.get_statistics, args=[context,'generatorportresults', "json"]).start()



    response = driver.load_config(context,"C:\Users\luiza.n\Documents\configurationtest1.tcc","False")
    print "1"
    response = driver.start_devices(context)
    print "2"
    driver.start_traffic(context)
    print "5"
    response = driver.send_arp(context)
    print "3"
    response = driver.send_arp(context)
    print "4"

    driver.get_statistics(context,'generatorportresults', "json")
    print "5"
    #print response
    #res=driver.update_firmware(context,'1.1.1.1','flash:/config_backup/')
    #print driver.send_custom_command(context, "display version")
    # print response


'''context:



resource.attributes=
{'CLI Connection Type': 'SSH', 'Enable Password': 'PgkOScppedeEbHGHdzpnrw==', 'NAT_Value_ManagementNetwork': '',
'System Name': '172.19.0.36', 'Console User': '', 'Location': 'Beijing China', 'OS Version': '5.160', 'Console Password': '3M3u7nkDzxWb0aJ/IZYeWw==',
'Power Management': 'False', 'Vendor': 'huawei', 'AdminUser': 'admin', 'Backup Location': '', 'Sessions Concurrency Limit': '1', 'User': 'telnet',
 'Password': 'PgkOScppedeEbHGHdzpnrw==', 'SNMP Version': '2', 'BaselineGroup': '0', 'Contact Name': 'R&D Beijing, huawei Technologies co.,Ltd.', 'SNMP V3 Private Key': '',
 'SNMP Read Community': 'esdkr0key', 'SNMP V3 Password': '', 'Model': 'Enterprises.2011.2.23.339', 'Console Port': '0', 'GuacServer': '', 'AdminPassword': 'DxTbqlSgAVPmrDLlHvJrsA==',
 'Console Server IP Address': '', 'BaselineConfigFilename': '', 'SNMP V3 User': '', 'SNMP Write Community': 'esdkw0key'}


reservation=
 reservation_id = {str} '5695cf87-a4f3-4447-a08a-1a99a936010e'
owner_user = {str} 'admin'
owner_email = {str} 'fake@qualisystems.com'
environment_path = {str} 'Environment-6-7-2016 15-25'
environment_name = {str} 'Environment-6-7-2016 15-25'
domain = {str} 'Global'
description = {NoneType} None

connectivity=

admin_auth_token = {str} 'T1dkw4LLJUSmWDpolusJdw=='
cloudshell_api_port = {str} '8029'
quali_api_port = {str} '9000'
server_address = {str} 'localhost'

description=
description = {NoneType} None
family = {str} 'Router'
fullname = {str} 'Huawei37'
id = {str} 'b476fa1f-379e-435a-b35c-65e892e1c306'
model = {str} 'Huaewi VRP Router'
name = {str} 'Huawei37'
type = {str} 'Resource'
'''