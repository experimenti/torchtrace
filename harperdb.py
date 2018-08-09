# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import http.client as http
import json
import urllib.request
import base64
import requests
import sys
import os
import time
import uuid


def frameToExcel(self, narray, label):
    df = pd.DataFrame(narray)
    df.to_excel(writer, sheet_name=label)


def connect(url="http://localhost:9925", user="harperdb", password="harperdb"):

    # validate that the server is up and running
    ping(url, user, password)


def ping(url="http://localhost:9925", user="harperdb", password="harperdb"):

    op_dict = {
        'operation': 'describe_all'
    }

    response_json = postToHarper(op_dict, url, 'harperdb', 'harperdb')

    if(not response_json):
        print("Ping Failed")
    else:
        print(json.dumps(response_json))


def printResponse(response):
    print(response)


def validateSchema(user, password, url="http://localhost:9925", schema_name="torchtrace"):

    op_dict = {
        'operation': 'create_schema',
        'schema': schema_name
    }
    postToHarper(op_dict, url, 'harperdb', 'harperdb')


def createSchema(user, password, url="http://localhost:9925", schema_name="torchtrace"):

    op_dict = {
        'operation': 'create_schema',
        'schema': schema_name
    }

    postToHarper(op_dict, url, 'harperdb', 'harperdb')


def createTable(table, schema="torchtrace", hash_value="id"):

    op_dict = {
        'operation': 'create_table',
        'schema': schema,
        'table': table,
        'hash_attribute': hash_value
    }

    print(postToHarper(op_dict))


def postToHarper(data, url="http://localhost:9925", user='harperdb', password='harperdb'):

    username_password_string = "{0}:{1}".format(user, password).encode()
    username_password_b64_encoded = base64.b64encode(username_password_string)

    encoded_username_password = 'Basic {0}'.format(
        username_password_b64_encoded.decode("utf-8"))

    headers = {
        'Content-Type': "application/json",
        'Authorization': encoded_username_password
    }

    response = requests.request(
        "POST", url, data=json.dumps(data), headers=headers)

    print(response.text)

    return response.json()


def insertTensor():

    D_in, D_out = 10, 10

    # Create random input and output data
    x = np.random.randn(D_in, D_out)

    size = sys.getsizeof(x)

    data_x = [
        {
            "id": 4,
            "time": time.time(),
            "size": size,
            "tensor": x.tolist()
        }
    ]

    op_dict = {
        'operation': 'insert',
        'schema': 'torchtrace',
        'table': 'x',
        'records': data_x
    }

    print(postToHarper(op_dict))


def getDirectorySize():
    path = '/home/john/hdb'
    folder = sum([sum(map(lambda fname: os.path.getsize(os.path.join(
        directory, fname)), files)) for directory, folders, files in os.walk(path)])
    MB = 1024*1024.0

    print("{0}".format(folder/MB))

    return folder/MB


payload = "{\n\"operation\":\"read_log\",\n\"limit\":1000,\n\"start\":0,\n\"from\":\"2017-07-10\",\n\"until\":\"2019-07-11\",\n\"order\":\"desc\"\n}"


def exportTableToCSV():

    query = "SELECT * FROM {0}".format("torchtrace.x")

    print(query)

    op_dict = {
        "operation": "export_local",
        "format": "csv",
        #"path":  "/mnt/c/Users/MYCOS-PC/code/exports/batchperf.csv",
        "path":  "/home/batchperf.csv",
        "search_operation": {
            "operation": "sql",
                "sql": query 
        }
    }

    postToHarper(op_dict)

def batchInsertTensors(iterations=1):

    for k in range(0, iterations):

        D_in, D_out = 10 + k, 10 + k

        # Create random input and output data
        x = np.random.randn(D_in, D_out)

        size = getDirectorySize()

        data = [
            {
                "id": uuid.uuid4().hex,
                "time": time.time(),
                "preinsert_size": size,
                "array_size_bytes": x.size * x.itemsize,
                "tensor": x.tolist()
            }
        ]

        op_dict = {
            'operation': 'insert',
            'schema': 'torchtrace',
            'table': 'x',
            'records': data
        }

        postToHarper(op_dict)


# insertTensor()
batchInsertTensors()
exportTableToCSV()