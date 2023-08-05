#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from tests.config import *


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.template_file = "config_template.py"
        self.dicts = ["keyvault", "auth", "blob", "acr", "aci", "dls", "dls_glob"]

    def test_010_mktemplate(self):
        self.fd = open(self.template_file, "w")
        for dict in self.dicts:
            self.fd.write(f"{dict} = " + "{\n")
            for key in globals()[dict]:
                self.fd.write(f'    "{key}": "xxxxxxxxx"\n')
            self.fd.write("}\n")
        self.fd.close()


if __name__ == "__main__":
    sys.argv.append("-v")
    unittest.main()
