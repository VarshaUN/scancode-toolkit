#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/scancode-toolkit for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#


import os
import logging
import re
import fnmatch
import saneyaml
from packageurl import PackageURL
from packagedcode import models

logger = logging.getLogger(__name__)

class LuaRocksHandler(models.DatafileHandler):
    lockfile_names = {'*.rockspec'}

    @classmethod
    def recognize(cls, location):
        return any(fnmatch.fnmatch(location, pattern) for pattern in cls.lockfile_names)

    @classmethod
    def parse(cls, location):
        with open(location, 'r') as file:
            try:
                data = saneyaml.load(file.read())
            except Exception as e:
                logger.error(f"Failed to parse {location}: {e}")
                return

      
        package_data = {
            'type': 'luarocks',
            'name': data.get('package', ''),
            'version': data.get('version', ''),
            'dependencies': []
        }

       
        dependencies = data.get('dependencies', [])
        for dep in dependencies:
            if isinstance(dep, str):
                dep_name_version = dep.split()
                if len(dep_name_version) == 2:
                    package_data['dependencies'].append({
                        'name': dep_name_version[0].strip('"'),
                        'version': dep_name_version[1].strip('"')
                    })
            elif isinstance(dep, dict):
                for dep_name, dep_version in dep.items():
                    package_data['dependencies'].append({
                        'name': dep_name.strip('"'),
                        'version': dep_version.strip('"')
                    })

       

        return models.PackageData(**package_data)


