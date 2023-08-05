#!/usr/bin/env python3
# coding: utf-8

import gettext
import json
from pathlib import Path

HOME = Path.home() / '.config/mpkg'

if not HOME.exists():
    HOME.mkdir(parents=True)


def SetConfig(key: str, value=True, path='', filename='config.json', abspath=''):
    if GetConfig(key, path, filename, abspath) == value:
        return
    path_ = HOME / 'config' / path if not abspath else Path(abspath)
    file = path_ / filename
    if not path_.exists():
        path_.mkdir(parents=True)
    if not file.exists():
        with file.open('w') as f:
            f.write('{}')
    with file.open('r') as f:
        data = json.loads(f.read())
    data[key] = value
    with file.open('w') as f:
        f.write(json.dumps(data))


def GetConfig(key: str, path='', filename='config.json', abspath=''):
    path_ = HOME / 'config' / path if not abspath else Path(abspath)
    file = path_ / filename
    if not file.exists():
        return
    with file.open('r') as f:
        data = json.loads(f.read())
    return data.get(key)
