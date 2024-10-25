#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/scancode-toolkit for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#



import io
from pathlib import Path
from dockerfile_parse import DockerfileParser  
from packagedcode import models
from packagedcode import utils
import fnmatch


class DockerfileHandler(models.DatafileHandler):
    datasource_id = 'dockerfile_oci_labels'

    @classmethod 
    def is_datafile(cls, path): 
        patterns = ['Dockerfile', 'containerfile', '*.dockerfile'] 
        filename=os.path.basename(path)
        for pattern in patterns: 
            if fnmatch.fnmatch(filename, pattern): 
                return True 
        return False
    
    @classmethod
    def parse(cls, location, package_only=False):
        """
        Parse a Dockerfile and yield one or more PackageData objects with OCI labels and metadata.
        """
        labels = cls.extract_oci_labels_from_dockerfile(location)
        package_data = {
            'datasource_id': cls.datasource_id,
            'type': cls.default_package_type,
            'name': labels.get('name', 'None'),  
            'version': labels.get('version', 'None'),  
            'license_expression': labels.get('license', 'None'),
            'labels': labels,  
        }

        yield models.PackageData.from_data(package_data, package_only)

    @classmethod
    def extract_oci_labels_from_dockerfile(cls, dockerfile_path):
        """
        Extract OCI labels from the Dockerfile using DockerfileParser.
        """
        labels = {}
        parser = DockerfileParser()
        with open(dockerfile_path, 'r') as dockerfile:
          parser.content = dockerfile.read() 
          labels = parser.labels
        return labels
