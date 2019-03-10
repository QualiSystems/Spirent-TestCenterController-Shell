![](https://github.com/QualiSystems/cloudshell-shells-documentaion-templates/blob/master/cloudshell_logo.png)

# **Spirent TestCenter Controller 1G Shell**  

Release date: January 2019

Shell version: 1.5.3

Document version: A

# In This Guide

* [Overview](#overview)
* [Downloading the Shell](#downloading-the-shell)
* [Importing and Configuring the Shell](#importing-and-configuring-the-shell)
* [Updating Python Dependencies for Shells](#updating-python-dependencies-for-shells)
* [Associating a CloudShell Service to a Non-Global Domain](#associating-a-cloudShell-service-to-a-non-global-domain)
* [Typical Workflows](#typical-workflows)
* [References](#references)
* [Release Notes](#release-notes)


# Overview
A shell integrates a device model, application or other technology with CloudShell. A shell consists of a data model that defines how the device and its properties are modeled in CloudShell, along with automation that enables interaction with the device via CloudShell.

**Note:** We recommend using a 2nd gen shell where possible. Using a 1st gen shell may limit some shell management capabilities. For more information, see [Shell Overview – “Our Shell”](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/LAB-MNG/Shells.htm?Highlight=shell%20overview).

### Traffic Generator Shells
CloudShell's traffic generator shells enable you to conduct traffic test activities on Devices Under Test (DUT) or Systems Under Test (SUT) from a sandbox. In CloudShell, a traffic generator is typically modeled using a chassis resource, which represents the traffic generator device and ports, and a controller service that runs the chassis commands, such as Load Configuration File, Start Traffic and Get Statistics. Chassis and controllers are modeled by different shells, allowing you to accurately model your real-life architecture. For example, scenarios where the chassis and controller are located on different machines.

For additional information on traffic generator shell architecture, and setting up and using a traffic generator in CloudShell, see the [Traffic Generators Overiew](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/LAB-MNG/Trffc-Gens.htm?Highlight=traffic%20generator%20overview) online help topic.

### **Spirent TestCenter Controller 1G Shell**

To model a Spirent TestCenter device in CloudShell, use the following shells:

▪ [Spirent TestCenter Chassis 2G Shell](https://community.quali.com/repos/4080/spirent-test-center-chassis-2-gen-shell), which provides data model and autoload functionality to model and load the Spirent TestCenter Chassis to resource management.

▪ [Spirent TestCenter Controller 1G Shell (service)](https://community.quali.com/repos/1280/spirent-test-center-controller-shell), which provides functionality to load test configuration, run tests, get test results, etc.

For more information on **Spirent TestCenter**, see the official device manufacturer product documentation.

### Standard version

For detailed information about the shell’s structure and attributes, see the **Shells Standard: Traffic Generator Controller**.(https://github.com/QualiSystems/cloudshell-standards/blob/master/Documentation/Traffic%20Generator%20Controller%20Shell%20Standard.md) in GitHub.

### Supported OS
▪ Windows

### Requirements

Release: **Spirent TestCenter Controller 1G Shell**

▪ CloudShell version: 8.1 and above

▪ TestCenter Rest Server: Lab Server or STC web services

### Data Model

The shell's data model includes all shell metadata, families, and attributes.

#### **Spirent TestCenter Controller Attributes**

The attribute names and descriptions are listed in the following table:

|Attribute|Description|
|:---|:---|
|Controller Address|IP address of the traffic server. Relevant only if an external server is configured.|
|Controller TCP Port|TCP port of the traffic server. Relevant only if an external server is configured. If left empty, the Default TCP port should be used.|
|Test Files Location|Location for test related files|

### Automation
This section describes the automation (driver) associated with the data model. The shell’s driver is provided as part of the shell package. There are two types of automation processes, Autoload and Resource. Autoload is executed when creating the resource in the **Inventory** dashboard, while resource commands are run in the sandbox.

For Traffic Generator shells, commands are configured and executed from the controller service in the sandbox, with the exception of the Autoload command, which is executed when creating the resource.

The following table describes the process that occurrs during Autoload for the controller shell:

|Command|Description|
|:-----|:-----|
|Autoload|Discovers the chassis, its hierarchy and attributes when creating the resource. The command can be rerun in the Inventory dashboard and not in the sandbox, as for other commands.|

**User Commands**

The following table lists the commands the sandbox end-user can run from the controller service:

**Note**: For detailed information on running a traffic test in CloudShell, see [Traffic Generators Overview](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/LAB-MNG/Trffc-Gens.htm?Highlight=traffic%20generators%20overview).

|Command|Description|
|:-----|:-----|
|Load configuration|Reserves ports and loads the configuration file. <br>Set the command input as follows:<br>▪ **STC config file name** (String) (Mandatory): Full path to the STC configuration file name - tcc or xml.|
|Start ARP/ND|Sends ARP/ND for all devices and streams.|
|Start All Devices|Starts devices (these are the STC objects that emulate network devices). There are parallel commands in the STC GUI that are called start devices.|
|Stop All Devices|Stops devices (these are the STC objects that emulate network devices). There are parallel commands in STC GUI that are called stop devices.|
|Start Traffic|Sends traffic on all ports.<br>Set the command input as follows:<br>▪ **Blocking (Enum)**: **True**: Returns after traffic finishes running; **False**: Returns immediateley.|
|Stop Traffic|Stops traffic on all ports.|
|Get Statistics|Gets real time statistics of the traffic test in either JSON or CSV format. <br>Set the command's inputs as follows: <br>▪ **View Name**: (String) (Mandatory) - Type of statistics to return, such as generatorPortResults, analyzerPortResults, etc.<br>▪ **Output Type (Enum)**: **JSON** or **CSV**. JSON prints the statistics to the sandbox's output, which is useful for API calls that can then use the output, while CSV attaches a CSV file with the test's statistics to the sandbox.|
|Perform sequencer command|Set the command's inputs as follows:<br>**Command** (Enum)<br> ▪ **Start**, **Stop** or **Wai**t for sequencer to end (Blocking).|

**Hidden Commands**

The following table describes the hidden developer commands from the controller service:

|Command|Description|Parameters|
|:-----|:-----|:-----|
|get_session_id|Returns the REST session. This ID can be used to run directly any STC REST command.||
|get_children|Returns a list of all children of a specific type of requested object.<br>If *child_type* **== None**, all children will be returned.|*obj_ref*: Requested object reference<br>*child_type*: Requested child type|
|get_attributes|Returns dictionary of all <attribute: value> of the requested object attributes.|obj_ref: Requested object reference|
|set_attribute|Sets value of specific attribute of the requested object.|*obj_ref*: Requested object reference<br>*attr_name*:	Requested attribute name<br>*attr_value*: Value to set|
|perform_command|Performs any STC command.|*command*: Requested command (without the Command suffix)<br>*parameters_json*: Command parameters dict {name: value} as serialized json|

The following is a simple code snippet demonstrating the hidden commands:

The code assumes that *reservation_id* holds the reservation ID and *session* holds the CS session.

```
# Get session ID
session_id = session.ExecuteCommand(reservation_id, 'TestCenter Controller',                                                 'Service', 'get_session_id')

# Get project object reference.        
project = session.ExecuteCommand(reservation_id, 'TestCenter Controller',                                              'Service', 'get_children',
[InputNameValue('obj_ref', 'system1'),
 InputNameValue('child_type', 'project')])
project_obj = json.loads(project.Output)[0]

# Get all children of project.        
project_childs = session.ExecuteCommand(reservation_id, 'TestCenter Controller',                                                     'Service', 'get_children',
[InputNameValue('obj_ref', project_obj)])

# Get automation-options object reference.        
options = session.ExecuteCommand(reservation_id, 'TestCenter Controller',
'Service', 'get_children',                                              [InputNameValue('obj_ref', 'system1'),
 InputNameValue('child_type', 'AutomationOptions')])
options_ref = json.loads(options.Output)[0]

# Get automation-options attributes.
options_attrs = session.ExecuteCommand(reservation_id, 'TestCenter Controller',
'Service', 'get_attributes',                                                    [InputNameValue('obj_ref', options_ref)])

# Set automation-options log-level attribute.
session.ExecuteCommand(reservation_id,
'TestCenter Controller',
'Service', 'set_attribute',                                    [InputNameValue('obj_ref', options_ref),
 InputNameValue('attr_name', 'LogLevel'),
 InputNameValue('attr_value', 'INFO')])
 
# Perform subscribe command.
parameters = {'Parent': project_obj,
              'ResultParent': project_obj,
              'ConfigType': 'Generator',
              'ResultType': 'GeneratorPortResults'}
session.ExecuteCommand(reservation_id,
'TestCenter Controller',
'Service', 'perform_command',                                                    [InputNameValue('command', 'ResultsSubscribe'), InputNameValue('parameters_json',json.dumps(parameters))])
```

# Downloading the Shell
The **Spirent TestCenter Controller 1G Shell** is available from the [Quali Community Integrations](https://community.quali.com/integrations) page. 

Download the files into a temporary location on your local machine. 

The shell comprises:

|File name|Description|
|:---|:---|
|Spirent_TestCenter_controller.zip|Spirent TestCenter Controller shell package|
|Spirent_TestCenter_controller_offline_requirements.zip|Shell Python dependencies (for offline deployments only)|

# Importing and Configuring the Shell
This section describes how to import the **Spirent TestCenter Controller 1G Shell** and configure and modify the shell’s devices.

### Importing the shell into CloudShell

**To import the shell into CloudShell:**
  1. Make sure you have the shell’s zip package. If not, download the shell from the [Quali Community's Integrations](https://community.quali.com/integrations) page.
  
  2. Backup your database.
  
  3. Log in to CloudShell Portal as administrator and access the relevant domain.
  
  4. In the user menu select **Import Package**.
  
     ![](https://github.com/QualiSystems/cloudshell-shells-documentaion-templates/blob/master/import_package.png)
     
  5. Browse to the location of the downloaded shell file, select the relevant *.zip* file and Click **Open**. Alternatively, drag the shell’s .zip file into CloudShell Portal.<br><br>The Spirent TestCenter controller shell is displayed in the **App/Service>Applications** section of your blueprint, and can be used to run custom code and automation processes in the sandbox. For more information, see [Services Overview](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/LAB-MNG/Services.htm?Highlight=services). 

### Offline installation of a shell

**Note:** Offline installation instructions are relevant only if CloudShell Execution Server has no access to PyPi. You can skip this section if your execution server has access to PyPi. For additional information, see the online help topic on offline dependencies.

In offline mode, import the shell into CloudShell and place any dependencies in the appropriate dependencies folder. The dependencies folder may differ, depending on the CloudShell version you are using:

* For CloudShell version 8.3 and above, see [Adding Shell and script packages to the local PyPi Server repository](#adding-shell-and-script-packages-to-the-local-pypi-server-repository).

* For CloudShell version 8.2, perform the appropriate procedure: [Adding Shell and script packages to the local PyPi Server repository](#adding-shell-and-script-packages-to-the-local-pypi-server-repository) or [Setting the Python pythonOfflineRepositoryPath configuration key](#setting-the-python-pythonofflinerepositorypath-configuration-key).

* For CloudShell versions prior to 8.2, see [Setting the Python pythonOfflineRepositoryPath configuration key](#setting-the-python-pythonofflinerepositorypath-configuration-key).

### Adding shell and script packages to the local PyPi Server repository
If your Quali Server and/or execution servers work offline, you will need to copy all required Python packages, including the out-of-the-box ones, to the PyPi Server's repository on the Quali Server computer (by default *C:\Program Files (x86)\QualiSystems\CloudShell\Server\Config\Pypi Server Repository*).

For more information, see [Configuring CloudShell to Execute Python Commands in Offline Mode](http://help.quali.com/Online%20Help/9.0/Portal/Content/Admn/Cnfgr-Pyth-Env-Wrk-Offln.htm?Highlight=Configuring%20CloudShell%20to%20Execute%20Python%20Commands%20in%20Offline%20Mode).

**To add Python packages to the local PyPi Server repository:**
  1. If you haven't created and configured the local PyPi Server repository to work with the execution server, perform the steps in [Add Python packages to the local PyPi Server repository (offline mode)](http://help.quali.com/Online%20Help/9.0/Portal/Content/Admn/Cnfgr-Pyth-Env-Wrk-Offln.htm?Highlight=offline%20dependencies#Add). 
  
  2. For each shell or script you add into CloudShell, do one of the following (from an online computer):
      * Connect to the Internet and download each dependency specified in the *requirements.txt* file with the following command: 
`pip download -r requirements.txt`. 
     The shell or script's requirements are downloaded as zip files.

      * In the [Quali Community's Integrations](https://community.quali.com/integrations) page, locate the shell and click the shell's **Download** link. In the page that is displayed, from the Downloads area, extract the dependencies package zip file.

3. Place these zip files in the local PyPi Server repository.
 
### Setting the Python PythonOfflineRepositoryPath configuration key
Before PyPi Server was introduced as CloudShell’s Python package management mechanism, the `PythonOfflineRepositoryPath` key was used to set the default offline package repository on the Quali Server machine, and could be used on specific Execution Server machines to set a different folder. 

**To set the offline Python repository:**
1. Download the *Spirent_TestCenter_controller_offline_requirements.zip* file, see [Downloading the Shell](#downloading-the-shell).

2. Unzip it to a local repository. Make sure the execution server has access to this folder. 

3.  On the Quali Server machine, in the *~\CloudShell\Server\customer.config* file, add the following key to specify the path to the default Python package folder (for all Execution Servers):  
	`<add key="PythonOfflineRepositoryPath" value="repository 
full path"/>`

4. If you want to override the default folder for a specific Execution Server, on the Execution Server machine, in the *~TestShell\Execution Server\customer.config* file, add the following key:  
	`<add key="PythonOfflineRepositoryPath" value="repository 
full path"/>`

5. Restart the Execution Server.

### Configuring a new service

**To configure a service for the device:**
  1. In CloudShell Resource Manager, in the **Inventory** tab, click **Resource Families**. 
         
  2. In the **Traffic Generator Controller** folder, select **TestCenter Controller**.
  
     ![](https://github.com/QualiSystems/Spirent-TestCenterController-Shell/blob/master/spirent_testcenter_controller.png)
  
  3. In the **Attributes** tab, enter the **Default Values** for the Spirent TestCenter Controller service as follows:
  * **Controller Address**: IP address of the STC REST server, either lab server or the machine running stcweb.
  * **Controller TCP Port**: TCP port of the STC REST server, either lab server or the machine running stcweb.
	     
  4. Click **Save**.<br><br>CloudShell validates the device’s settings and updates the new resource with the device’s structure.

# Updating Python Dependencies for Shells
This section explains how to update your Python dependencies folder. This is required when you upgrade a shell that uses new/updated dependencies. It applies to both online and offline dependencies.

### Updating offline Python dependencies
**To update offline Python dependencies:**
1. Download the latest Python dependencies package zip file locally.

2. Extract the zip file to the suitable offline package folder(s). 

3. Terminate the shell’s instance, as explained [here](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/MNG/Mng-Exctn-Srv-Exct.htm#Terminat).

### Updating online Python dependencies
In online mode, the execution server automatically downloads and extracts the appropriate dependencies file to the online Python dependencies repository every time a new instance of the driver or script is created.

**To update online Python dependencies:**
* If there is a live instance of the shell's driver or script, terminate the shell’s instance, as explained [here](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/MNG/Mng-Exctn-Srv-Exct.htm#Terminat). If an instance does not exist, the execution server will download the Python dependencies the next time a command of the driver or script runs.

# Associating a CloudShell Service to a Non-Global Domain

In order to expose a service to users of a domain that is not the Global domain, you must associate the service to the domain. To do this, you need to associate the service to a category that is assigned to the domain.

When you import a service shell, most shells are automatically assigned a default service category which is associated with the Global domain. For custom shells, this may not be true.

**To associate the Spirent TestCenter Controller 1G service to a non-global domain:**

**Note:** The association process differs depending on the type of shell - second generation (2G) shell or first generation (1G) shell. The instructions below detail the steps for a 1G service shell.

*  (Optional) You can associate the service to a service category that already exists in CloudShell or associate the service to a new category.

	**Note:** If you do not want to change the category(s) of this shell, you can use the default category that comes out-of-the-box (if it exists).
	
	Do one of the following:
	 
	* Associate the service family to an existing category(s).
	
		1. In Resource Manager Client, open the **Resource Families** explorer and click the relevant service family.
	
		2. From the right pane, open the **Categories** tab.
	
		3. Click **Add**. The **Select Category** dialog box is displayed. 
	
		4. Select a category from the catalog and click **OK**.
	
	 or

	* Modify the 1G category(s) in the shell project’s configuration files to add a new category(s). See [Associating categories to 1st Gen Service Shells](https://devguide.quali.com/reference/9.0.0/associating-service-categories.html).

* Associate the shell’s service category to a domain.
	1. In the **Manage** dashboard, click **Categories** from the left sidebar, or **Domains** if you are a domain admin.
	
	2. Select **Services Categories**.
	
	3. Click the service category that is associated with your service shell.
	
	4. In the **Edit Category** dialog box, from the **Domains** drop-down list, select the desired domain(s).
	
	5. Click **Save**.

# Typical Workflows 

**Workflow** - *Using the Spirent controller to run TestCenter traffic* 

1. Create a new blueprint.

   a. In CloudShell Portal, in the top left section of the **Blueprint Catalog**, click **+ Create Blueprint**.
   
   b. Give the blueprint a name.
   
2. Add resources and services to the blueprint. 

   a. Click the **App/Services** tab and add the **TestCenter Controller** service.

   b. Click the **Resource** button and add the TestCenter chassis resource and all needed ports into the diagram. The number of STC ports in the blueprint should match the number of ports in the TestCenter configuration. For example, if you have a configuration with two ports:
   
     ![](https://github.com/QualiSystems/Spirent-TestCenterController-Shell/blob/master/spirent_testcenter_ports.png)
 
     ![](https://github.com/QualiSystems/Spirent-TestCenterController-Shell/blob/master/spirent_testcenter_blueprint_ports.png)

3. Reserve the blueprint to create a sandbox.

4. Edit the TestCenter Controller Service parameters if required.

   ![](https://github.com/QualiSystems/Spirent-TestCenterController-Shell/blob/master/spirent_testcenter_service_parameters.png)

   See [Configuring a new service](#configuring-a-new-service).

5. Click **Add**.

6. Map the configuration ports to the sandbox ports. For each port in the TestCenter configuration, assign a physical port from the ports in the sandbox. To do this, open the attributes tab and set the **Logical Name** to the port name in the configuration:
          
   ![](https://github.com/QualiSystems/Spirent-TestCenterController-Shell/blob/master/spirent_testcenter_port_logical_name.png)  

# References
To download and share integrations, see [Quali Community's Integrations](https://community.quali.com/integrations). 

For instructional training and documentation, see [Quali University](https://www.quali.com/university/).

To suggest an idea for the product, see [Quali's Idea box](https://community.quali.com/ideabox). 

To connect with Quali users and experts from around the world, ask questions and discuss issues, see [Quali's Community forums](https://community.quali.com/forums). 

To use traffic generator ports as abstract resources, see [CloudShell's Online Help](https://help.quali.com/Online%20Help/9.1/Portal/Content/CSP/LAB-MNG/Traffic-Gens-Abst.htm?Highlight=traffic%20generator).

# Release Notes 

### What's New

• The **Get Statistics** command does not fail, if there are no results available on the STC chassis (for example, if traffic did not start) and instead, returns an empty statistics table. 

For release updates, see the shell's [GitHub releases page](https://github.com/QualiSystems/Spirent-TestCenterController-Shell/releases). 

