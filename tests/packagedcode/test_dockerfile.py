#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/scancode-toolkit for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

from packagedcode import dockerfile
import pytest
import os.path
import json
from pathlib import Path
from packagedcode.dockerfile import DockerfileHandler

class TestDockerfileHandler:

    def get_test_loc(self, path):
        return Path(os.path.join(os.path.dirname(__file__), 'data'))

    def load_expected(self, expected_file):
        with open(expected_file) as f:
            return json.load(f)

    def test_is_datafile(self):
        dockerfiles = [
            'test.dockerfile',
            'test.containerfile',
            'psql.dockerfile'
        ]
        for dockerfile in dockerfiles:
            test_file = self.get_test_loc(f'data/docker/{dockerfile}')
            assert DockerfileHandler.is_datafile(str(test_file))

    def test_parse_dockerfile(self):
        test_files = [
            ('test.dockerfile', 'test-dockerfile-expected.json'),
            ('test.containerfile', 'containerfile-expected.json'),
            ('psql.dockerfile', 'psql-expected.json')
        ]
        for dockerfile, expected in test_files:
            test_file = self.get_test_loc(f'data/docker/{dockerfile}')
            expected_loc = self.get_test_loc(f'data/docker/{expected}')
            packages = list(DockerfileHandler.parse(str(test_file)))
            expected_packages = self.load_expected(expected_loc)
            assert packages == expected_packages

    def test_extract_oci_labels_from_dockerfile(self, mocker):
        dockerfiles = [
            'test.dockerfile',
            'test.containerfile',
            'psql.dockerfile'
        ]
        for dockerfile in dockerfiles:
            dockerfile_path = self.get_test_loc(f'data/docker/{dockerfile}')
            labels = DockerfileHandler.extract_oci_labels_from_dockerfile(str(dockerfile_path))
            expected_loc = self.get_test_loc(f'data/docker/{dockerfile.replace(".dockerfile", "-expected.json").replace(".containerfile", "-expected.json")}')
            expected_labels = self.load_expected(expected_loc)[0]['labels']
            assert labels == expected_labels
