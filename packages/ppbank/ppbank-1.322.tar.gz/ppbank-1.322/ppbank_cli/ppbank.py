#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

from __future__ import print_function
# import os
# import re
import requests
import os
import json
import csv
# import pandas as pd
import typer

app = typer.Typer()


import configparser
config = configparser.ConfigParser()
from os.path import expanduser
home = expanduser("~")
config.read(os.path.join(home,'.ppbank/config'))

try: 
    API_ADDRESS = config['global'].get('API_ADDRESS',"http://api.dev.databank.localhost/")
except:
    API_ADDRESS = "http://api.dev.databank.localhost/"
INF = 999999999
print(API_ADDRESS)


############################################

def json_to_csv(ans, csv_filename):
    data_file = open(csv_filename, 'w')
    csv_writer = csv.writer(data_file)
    count = 0
    for item in ans:
        if count == 0:
            # Writing headers of CSV file
            header = item.keys()
            csv_writer.writerow(header)
            count += 1
        # Writing data of CSV file
        csv_writer.writerow(item.values())
    data_file.close()


def parse_folder_name(molecule_folder):
    dirname = os.path.dirname(molecule_folder)
    basename = os.path.basename(molecule_folder)
    return (dirname, basename)


@app.command()
def get_conformers_by_energy(mole_name_folder: str, energy_level: float):
    folder = os.path.exists(mole_name_folder)
    if not folder:
        os.makedirs(mole_name_folder)
    else:
        print("Folder "+mole_name_folder+" already exists, stoped")
        # exit(-1)
        return "error"

    (dirname, basename) = parse_folder_name(mole_name_folder)
    payload = {'mole_name': basename, 'energy_level': energy_level}
    r = requests.get(API_ADDRESS+'/get_conformers/', params=payload)
    if r.text == 'error':
        print("molecule " + basename +
              " does not exist in database or have no matching result")
        return "error"

    ans = json.loads(r.text)

    os.makedirs(os.path.join(mole_name_folder, 'xyzfiles'))
    for i in ans:
        xyz = i.pop('xyz', None)
        open(os.path.join(mole_name_folder,
                          'xyzfiles', i['conf_name']), 'w').write(xyz)
        i.pop('id', None)

        i.pop('mole_name', None)
        i.pop('residue_num', None)
        i.pop('seq', None)
        i.pop('modification', None)

    json_to_csv(ans, os.path.join(mole_name_folder, 'conformers.csv'))


@app.command()
def get_conformers(mole_name_folder: str):
    folder = os.path.exists(mole_name_folder)
    if not folder:
        os.makedirs(mole_name_folder)
    else:
        print("Folder "+mole_name_folder+" already exists, stoped")
        # exit(-1)
        return "error"

    (dirname, basename) = parse_folder_name(mole_name_folder)
    payload = {'mole_name': basename}
    r = requests.get(API_ADDRESS+'/get_conformers/', params=payload)
    if r.text == 'error':
        print("molecule " + basename+" does not exist in database")
        return "error"

    ans = json.loads(r.text)

    os.makedirs(os.path.join(mole_name_folder, 'xyzfiles'))
    for i in ans:
        xyz = i.pop('xyz', None)
        open(os.path.join(mole_name_folder,
                          'xyzfiles', i['conf_name']), 'w').write(xyz)
        i.pop('id', None)

        i.pop('mole_name', None)
        i.pop('residue_num', None)
        i.pop('seq', None)
        i.pop('modification', None)

    json_to_csv(ans, os.path.join(mole_name_folder, 'conformers.csv'))


@app.command()
def del_conformers(basename: str):
    payload = {'mole_name': basename}
    r = requests.get(API_ADDRESS+'/del_conformers/', params=payload)
    if r.text == 'ok':
        # print("molecule "+basename+" deleted.")
        return "ok"
    else:
        print("delete failed.")


@app.command()
def replace_conformers(folder: str):
    del_conformers(os.path.basename(folder))
    put_conformers(folder)


@app.command()
def put_conformers(folder: str):
    mole_name = os.path.basename(folder)
    conf_list = []
    file = os.path.join(folder, 'conformers.csv')
    csvfile = open(file, 'r')

    fieldnames = ('conf_name', 'dih', 'dih_pattern', 'energy', 'free_energy')
    # fieldnames = ('mole_name','residue_num','seq','modification','conf_name','dih','dih_pattern','energy', 'free_energy')

    reader = csv.DictReader(csvfile, fieldnames)
    out = [row for row in reader][1:]
    # print(out)
    for i in out:
        conf_name = i['conf_name'].strip()
        if i['energy'].strip() != '':
            energy = float(i['energy'])
        else:
            energy = INF
        if i['free_energy'].strip() != '':
            free_energy = float(i['free_energy'])
        else:
            free_energy = INF
        file = os.path.join(folder, 'xyzfiles', conf_name)
        conformer = {
            "mole_name": mole_name,
            "residue_num": int(mole_name.split('-')[0]),
            "seq": mole_name.split('-')[1],
            "modification": mole_name.split('-')[2],
            "conf_name": conf_name,
            "dih": i['dih'],
            "dih_pattern": i['dih_pattern'],
            "energy": energy,
            "free_energy": free_energy,
        }
        if os.path.exists(file):
            conformer["xyz"] = open(file).read()
        # else:
            # conformer["xyz"] = ''

        conf_list.append(conformer.copy())

    payload = {
        "conf_list": conf_list,
        "file_type": "xyz",
    }

    r = requests.post(API_ADDRESS+'/put_conformers/', data=json.dumps(payload))
    if r.text == 'ok':
        return "ok"
    else:
        print("molecule "+mole_name + " already exists")
        return "error"


if __name__ == "__main__":
    app()






def put_conformers_xyz(folder):
    mole_name = os.path.basename(folder)
    conf_list = []
    file = os.path.join(folder, 'xyz_info.csv')
    csvfile = open(file, 'r')
    fieldnames = ("conf_name", "energy")
    reader = csv.DictReader(csvfile, fieldnames)
    out = [row for row in reader][1:]
    # print(out)
    for i in out:
        conf_name = i['conf_name']
        energy = float(i['energy'])
        file = os.path.join(folder, 'xyzfiles', conf_name)
        conformer = {
            "mole_name": mole_name,
            "residue_num": int(mole_name.split('-')[0]),
            "seq": mole_name.split('-')[1],
            "modification": mole_name.split('-')[2],
            "conf_name": conf_name,
            "dih": '',
            "dih_pattern": '',
            "energy": energy,
            "free_energy": energy,
            "xyz": open(file).read(),
        }
        conf_list.append(conformer.copy())

    payload = {
        "conf_list": conf_list,
        "file_type": "xyz",
    }
    # print(json.dumps(payload))
    r = requests.post(API_ADDRESS+'/put_conformers/', data=json.dumps(payload))
    # print(r.text)


def csv_to_json(file):

    csvfile = open(file, 'r')
    # jsonfile_obj = tempfile.NamedTemporaryFile()
    # jsonfile = open(jsonfile_obj.name, 'w')
    fieldnames = ("mole_name", " residue_num", " seq", " type",
                  " conf_name", "dih", "dih_pattern", " energy", " free_energy")
    reader = csv.DictReader(csvfile, fieldnames)
    out = json.dumps([row for row in reader][1:])
    # out = out[1:]
    # print(out)
    return out
    # for row in reader:
    #     json.dump(row, jsonfile)
    #     jsonfile.write('\n')
    # jsonfile.close()
    # jsonfile=open(jsonfile_obj.name)
    # print(jsonfile.read())
    # conf_list=json.loads(jsonfile.read())
    # return conf_list


def csv_to_json_by_pandas(file):
    df = pd.DataFrame(pd.read_csv(file))
    df.to_json(r'new.json')


def get_conformers_xyz(name, folder):
    pass


def get_conformers_by_energy_xyz(name, folder, energy):
    pass



def get_conformers_by_energy_dih(mole_name_folder, energy):
    pass


def get_conformers_dih(mole_name_folder):
    (dirname, basename) = parse_folder_name(mole_name_folder)
    payload = {'mole_name': basename}
    r = requests.get(API_ADDRESS+'/get_conformers/', params=payload)
    ans = json.loads(r.text)
    json_to_csv(ans, 'test.csv')


def put_conformers_dih(molecule_folder):
    (dirname, basename) = parse_folder_name(molecule_folder)
    csv_file_path = os.path.join(molecule_folder, 'conformers.csv')
    conf_list = csv_to_json(csv_file_path)
    payload = {
        "conf_list": conf_list,
        "file_type": "dih",
    }
    # print(json.dumps(payload))

    r = requests.post(API_ADDRESS+'/put_conformers/', data=json.dumps(payload))

# if __name__ == "__main__":
#     TESTFILE_xyz = '/Users/lhr/@/project-databank/ppbank/apiserver/2-IG-N'
#     TESTFILE_get = '/Users/lhr/@/project-databank/ppbank/apiserver/2-IG-N'
#     TESTFILE = '/Users/lhr/@/project-databank/ppbank/apiserver/2-CC-N'

#     # put_conformers_xyz(TESTFILE_xyz)
#     # del_conformers('2-CC-N')
#     # put_conformers(TESTFILE)
#     # replace_conformers(TESTFILE)
#     # get_conformers(TESTFILE_get)
#     get_conformers_by_energy(TESTFILE_get, 2)

    # put_conformers_dih(TESTFILE)
    # get_conformers_dih(TESTFILE_get)


# 3
    # print(conf_list)
    # for row in reader:
    #     json.dump(row, jsonfile)
    #     jsonfile.write('\n')
    # jsonfile.close()
    # jsonfile=open(jsonfile_obj.name)
    # print(jsonfile.read())
    # conf_list=json.loads(jsonfile.read())
    # return conf_list
