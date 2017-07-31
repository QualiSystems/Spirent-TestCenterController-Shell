#!/usr/bin/env python
# encoding: utf-8

import xml.etree.ElementTree as ET
import yaml
from git import Repo

# Write new version

new_version = '1.2.1'

with open("shell.yml", 'r') as f:
    shell = yaml.safe_load(f)
shell['shell']['version'] = new_version
with open("shell.yml", 'w') as f:
    yaml.safe_dump(shell, f, default_flow_style=False)

with open("version.txt", 'w') as f:
    f.write(new_version)

drivermetadata = ET.parse('src/drivermetadata.xml')
driver = drivermetadata.getroot()
driver.attrib['Version'] = new_version
drivermetadata.write('src/drivermetadata.xml')

# git

repo = Repo('.')
repo.git.add('.')
repo.git.commit('-m version {}'.format(new_version))
repo.git.push()

# git push . development:master
# git push origin master:master
