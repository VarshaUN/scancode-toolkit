#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/scancode-toolkit for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#


import os
import pytest
from packagedcode.luarocks import LuaRocksHandler
from packagedcode.models import PackageData
from packages_test_utils import PackageTester
from scancode_config import REGEN_TEST_FIXTURES
from scancode.cli_test_utils import run_scan_click
from scancode.cli_test_utils import check_json_scan

class TestLuaRocks(PackageTester):
    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    @pytest.fixture
    def handler(self):
        return LuaRocksHandler()

    def test_recognize_rockspec(self, handler):
        assert handler.recognize('example.rockspec')
        assert not handler.recognize('example.json')

    def test_parse_rockspec_basic(self, handler):
        sample_data = """
        package = "sample"
        version = "1.0-1"
        dependencies = {
            "lua >= 5.1",
            "luafilesystem >= 1.6.3",
            {"lpeg >= 0.12"}
        }
        """
        test_file = self.get_test_loc('luarocks/sample.rockspec')
        with open(test_file, 'w') as f:
            f.write(sample_data)

        package_data = handler.parse(test_file)
        os.remove(test_file)  # Clean up the test file

        assert isinstance(package_data, PackageData)
        assert package_data.name == 'sample'
        assert package_data.version == '1.0-1'
        assert len(package_data.dependencies) == 3
        assert package_data.dependencies[0]['name'] == 'lua'
        assert package_data.dependencies[0]['version'] == '>= 5.1'
        assert package_data.dependencies[1]['name'] == 'luafilesystem'
        assert package_data.dependencies[1]['version'] == '>= 1.6.3'
        assert package_data.dependencies[2]['name'] == 'lpeg'
        assert package_data.dependencies[2]['version'] == '>= 0.12'

    def test_parse_rockspec_no_dependencies(self, handler):
        sample_data = """
        package = "sample"
        version = "1.0-1"
        """
        test_file = self.get_test_loc('luarocks/sample_no_deps.rockspec')
        with open(test_file, 'w') as f:
            f.write(sample_data)

        package_data = handler.parse(test_file)
        os.remove(test_file)  # Clean up the test file

        assert isinstance(package_data, PackageData)
        assert package_data.name == 'sample'
        assert package_data.version == '1.0-1'
        assert len(package_data.dependencies) == 0

    def test_parse_rockspec_with_dict_dependencies(self, handler):
        sample_data = """
        package = "sample"
        version = "1.0-1"
        dependencies = {
            { "luafilesystem": ">= 1.6.3" },
            { "lpeg": ">= 0.12" }
        }
        """
        test_file = self.get_test_loc('luarocks/sample_dict_deps.rockspec')
        with open(test_file, 'w') as f:
            f.write(sample_data)

        package_data = handler.parse(test_file)
        os.remove(test_file)  # Clean up the test file

        assert isinstance(package_data, PackageData)
        assert package_data.name == 'sample'
        assert package_data.version == '1.0-1'
        assert len(package_data.dependencies) == 2
        assert package_data.dependencies[0]['name'] == 'luafilesystem'
        assert package_data.dependencies[0]['version'] == '>= 1.6.3'
        assert package_data.dependencies[1]['name'] == 'lpeg'
        assert package_data.dependencies[1]['version'] == '>= 0.12'

    def test_parse_rockspec_complex(self, handler):
        sample_data = """
        package = "complex_sample"
        version = "2.0-0"
        dependencies = {
            "lua >= 5.1",
            "luasocket >= 3.0-rc1",
            { "luafilesystem": ">= 1.6.3" },
            { "lpeg": ">= 0.12" }
        }
        description = {
            summary = "A complex sample package",
            detailed = "This is a more detailed description of the complex sample package."
        }
        source = {
            url = "https://example.com/complex_sample-2.0-0.tar.gz",
            md5 = "9b8efb5f3e5d7b6a394c5a4d60b2b5ed"
        }
        """
        test_file = self.get_test_loc('luarocks/complex_sample.rockspec')
        with open(test_file, 'w') as f:
            f.write(sample_data)

        package_data = handler.parse(test_file)
        os.remove(test_file)  # Clean up the test file

        assert isinstance(package_data, PackageData)
        assert package_data.name == 'complex_sample'
        assert package_data.version == '2.0-0'
        assert len(package_data.dependencies) == 4
        assert package_data.dependencies[0]['name'] == 'lua'
        assert package_data.dependencies[0]['version'] == '>= 5.1'
        assert package_data.dependencies[1]['name'] == 'luasocket'
        assert package_data.dependencies[1]['version'] == '>= 3.0-rc1'
        assert package_data.dependencies[2]['name'] == 'luafilesystem'
        assert package_data.dependencies[2]['version'] == '>= 1.6.3'
        assert package_data.dependencies[3]['name'] == 'lpeg'
        assert package_data.dependencies[3]['version'] == '>= 0.12'
        assert package_data.extra_data['description']['summary'] == 'A complex sample package'
        assert package_data.extra_data['description']