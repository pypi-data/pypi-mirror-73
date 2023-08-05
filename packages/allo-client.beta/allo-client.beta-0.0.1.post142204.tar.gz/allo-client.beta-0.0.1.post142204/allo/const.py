#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

CONFIG_PATH = str(Path.home()) + "/allo-config.dict"
ALLO_URL = "allo.dev.libriciel.fr"
API_PATH = "https://{}/api/client".format(ALLO_URL)
