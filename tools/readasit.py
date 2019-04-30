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


def build_var(name, objrefkind, objrefname, path):
    objref = {}
    objref["kind"] = objrefkind
    objref["name"] = objrefname
    if "Deckhand" in objrefkind:
        objref["apiVersion"] = "deckhand.airshipit.org/v1alpha1"
    if "Pegleg" in objrefkind:
        objref["apiVersion"] = "pegleg.airshipit.org/v1alpha1"
    if "Armada" in objrefkind:
        objref["apiVersion"] = "armada.airshipit.org/v1alpha1"
    if "Shipyard" in objrefkind:
        objref["apiVersion"] = "shipyard.airshipit.org/v1alpha1"
    if "Drydock" in objrefkind:
        objref["apiVersion"] = "drydock.airshipit.org/v1alpha1"
    fieldref = {}
    # fieldref["fieldpath"] = path.replace(".","/")
    fieldref["fieldpath"] = path
    var = {}
    var["name"] = name
    var["objref"] = objref
    var["fieldref"] = fieldref
    return var


def build_varref(name, objrefkind, path):
    var = {}
    var["kind"] = objectrefkkind
    var["path"] = path
    return var


def add_key(key, node, varname, thepattern):
    fullkey = key.pop(0)
    fullkey = fullkey.replace("[", " ").replace("]", "")
    keyparts = fullkey.split(" ")
    thekey = keyparts[0]
    theindex = -1
    if len(keyparts) == 2:
        theindex = int(keyparts[1])
        if thekey not in node:
            node[thekey] = []
        if not isinstance(node[thekey], list):
            print("List issue with " + varname + " " + str(theindex) + " " + thekey)
            return
        else:
            currentlen = len(node[thekey])

        if (theindex >= currentlen):
            for i in range(currentlen, theindex + 1):
                node[thekey].append({})

    if (len(key) == 0):
        if (thepattern):
            if thekey not in node:
                print("Pattern issue with " + varname + " " + thepattern + " " + thekey + " " + str(theindex))
                node[thekey] = {"pattern-boggus": thepattern, "varname-boggus": varname}
            else:
                if (theindex != -1):
                    node[thekey][theindex] = node[thekey][theindex].replace(thepattern, varname)
                else:
                    node[thekey] = node[thekey].replace(thepattern, varname)
        else:
            if (theindex != -1):
                node[thekey][theindex] = varname
            else:
                node[thekey] = varname
    else:
        if (theindex != -1):
            add_key(key, node[thekey][theindex], varname, thepattern)
        else:
            if thekey not in node:
                node[thekey] = {}
            elif not isinstance(node[thekey], dict):
                # boggus replacement
                org = node[thekey]
                node[thekey] = {"order-boggus": org}

            add_key(key, node[thekey], varname, thepattern)


def load_file(filename):
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
        for doc in docs2:
            if ("substitutions" in doc["metadata"]):
                if (doc["kind"] not in varrefs):
                    varrefs[doc["kind"]] = {}
                for entry in doc["metadata"]["substitutions"]:
                    if entry["src"]["path"] != ".":
                        varpath = "spec" + entry["src"]["path"].replace("[", "._").replace("]", "_")
                        varname = ".".join([entry["src"]["kind"], entry["src"]["name"], varpath])
                    else:
                        varpath = "spec"
                        varname = ".".join([entry["src"]["kind"], entry["src"]["name"], varpath])
                    vars[varname] = build_var(varname, entry["src"]["kind"], entry["src"]["name"], varpath)

                    dest = entry["dest"]["path"].split(".")
                    dest[0] = "spec"
                    thepattern = None
                    if ("pattern" in entry["dest"]):
                        thepattern = entry["dest"]["pattern"]

                    varrefs[doc["kind"]]["/".join(dest).replace("[","/_").replace("]","_")] = doc["kind"]
                    add_key(dest, doc, "$(" + varname + ")", thepattern)

    # Save the list of vars to add to the kustomization.yaml
    varlist = []
    for key, value in vars.items():
        varlist.append(value)
    sortedlist = sorted(varlist, key=lambda k: k['name'])
    with open("kustomization.vars.yaml", 'w') as stream:
        yaml.dump(sortedlist, stream, default_flow_style=False)

    # Save the list of varref to add to the kustomizeconfig/crd.yaml
    for key, value in varrefs.items():
        with open("res/"+key+".yaml", 'w') as stream:
            varlist = []
            for key2, value2 in value.items():
                varlist.append({"path":key2,"kind":value2})
            sortedlist = sorted(varlist, key=lambda k: k['path'])
            yaml.dump(sortedlist, stream, default_flow_style=False)

    return docs2


def save_file(filename, docs):
    with open(filename, 'w') as stream:
        yaml.dump_all(docs, stream, default_flow_style=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--command',
                        help="Command to run",
                        type=str, choices=["extract_subst"],
                        default="extract_subst")
    parser.add_argument('-f', '--filename',
                        help="filename",
                        type=str,
                        default="airship.yaml")

    args = parser.parse_args()

    if (args.command == "extract_subst"):
        docs = load_file(args.filename)
        save_file(args.filename + ".new", docs)
    else:
        pass
