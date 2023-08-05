#!/usr/bin/env python3

"""
Module: taz

Trivial Azure API

Subpackages:
    - taz[storage]
    - taz[dev]
    - taz[dls]
    - taz[aci]
    - taz[auth]

to include in requirements.txt use notation: taz[storage,dls] for example
keyvault support is not optionnal

Submodules:
    - taz.keyvault
    - taz.auth
    - taz.acr
    - taz.aci
    - taz.blob (use Azure storage SDK v12)
    - taz.dls
    - taz.table
    - taz.databricks

Copyright (C) 2018-2020, Christophe Fauchard
"""

import sys
from taz._version import __version__, __version_info__

__author__ = "Christophe Fauchard <christophe.fauchard@gmail.com>"

if sys.version_info < (3, 6):
    raise RuntimeError("You need Python 3.6+ for this module.")
