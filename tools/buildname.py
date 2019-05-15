#!/usr/bin/python3

# Copyright 2018 AT&T Network Cloud Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import yaml
import requests
import sys
import json
import logging
import os
import argparse
import copy
import yaml
import glob
import csv
import re
from collections import OrderedDict


def load_file(filename, dirname):
    """
    TBD
    Args:
       tbd
    Returns:
       tbd
    """
    docs2 = []
    vars = {}
    varrefs = {}
    with open(filename, 'r') as stream:
        try:
            docs = yaml.load_all(stream)
        except yaml.YAMLError as exc:
            print(exc)

        docs2 = list(docs)

        fullnames = []
        for doc in docs2:
            apiversion = doc["apiVersion"].replace("/","_")
            kind = doc["kind"].lower()
            name = doc["metadata"]["name"]
            sepname = "{}/{}".format(dirname,"sepfile")
            fullnames.append(sepname)
            fullname = "{}/{}_{}_{}.yaml".format(dirname,apiversion,kind,name)
            fullnames.append(fullname)

        print("cat {} > {}.new".format(" ".join(fullnames), filename))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--filename',
                        help="filename",
                        type=str,
                        default="airship.yaml")

    parser.add_argument('-d', '--dirname',
                        help="dirname",
                        type=str,
                        default="tmp")

    args = parser.parse_args()

    docs = load_file(args.filename, args.dirname)
