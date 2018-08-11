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
#import asyncio
#import aiohttp

DEFAULT_SCHEMA = 'torchtrace'
DEFAULT_TABLE = 'trace'
DEFAULT_HASH = 'id'
DEFAULT_URL = 'http://localhost:9925'
DEFAULT_USER = 'harperdb'
DEFAULT_PASSWORD = 'harperdb'
DEFAULT_HDB_PATH = '/home/john/hdb'

def connect(url=DEFAULT_URL, user=DEFAULT_USER, password=DEFAULT_PASSWORD):

    # validate that the server is up and runnin

    ping(url, user, password)


def ping(url=DEFAULT_URL, user=DEFAULT_USER, password=DEFAULT_PASSWORD):

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


def validateSchema(user=DEFAULT_USER, password=DEFAULT_PASSWORD, url=DEFAULT_URL, schema_name=DEFAULT_SCHEMA):

    op_dict = {
        'operation': 'create_schema',
        'schema': schema_name
    }
    postToHarper(op_dict, url, user=DEFAULT_USER, password=DEFAULT_PASSWORD)


def createSchema(user=DEFAULT_USER, password=DEFAULT_PASSWORD, url=DEFAULT_URL, schema_name=DEFAULT_SCHEMA):

    op_dict = {
        'operation': 'create_schema',
        'schema': schema_name
    }

    print(postToHarper(op_dict, url, DEFAULT_USER, DEFAULT_PASSWORD))

def dropSchema(user=DEFAULT_USER, password=DEFAULT_PASSWORD, url=DEFAULT_URL, schema_name=DEFAULT_SCHEMA):

    op_dict = {
        'operation': 'drop_schema',
        'schema': schema_name
    }

    print(postToHarper(op_dict, url, user, password))



def createTable(table=DEFAULT_TABLE, schema=DEFAULT_SCHEMA, hash_value=DEFAULT_HASH):

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

    return response.json()


## serialize an array and insert it as the value
def insertArray(schema=DEFAULT_SCHEMA, table=DEFAULT_TABLE):

    D_in, D_out = 10, 10

    # Create random input and output data
    x = np.random.randn(D_in, D_out)

    size = sys.getsizeof(x)

    data = [
        {
            "id": uuid.uuid4().hex,
            "time": time.time(),
            "size": size,
            "array": x.tolist()
        }
    ]

    op_dict = {
        'operation': 'insert',
        'schema': schema,
        'table': table,
        'records': data
    }

    print(postToHarper(op_dict))


def getDirectorySize():
    path = DEFAULT_HDB_PATH 
    folder = sum([sum(map(lambda fname: os.path.getsize(os.path.join(
        directory, fname)), files)) for directory, folders, files in os.walk(path)])
    MB = 1024*1024.0

    print("{0}".format(folder/MB))

    return folder/MB


def exportTableToCSV(schema=DEFAULT_SCHEMA, table=DEFAULT_TABLE):

    schema_table = schema + '.' + table
    query = "SELECT * FROM {0}".format(schema_table)

    op_dict = {
        "operation": "export_local",
        "format": "csv",
        "path":  '/home/john',
        "search_operation": {
            "operation": "sql",
                "sql": query 
        }
    }

    print(postToHarper(op_dict))

def batchInsertTensors(iterations=1, schema=DEFAULT_SCHEMA, table=DEFAULT_TABLE, user=DEFAULT_USER, password=DEFAULT_PASSWORD):

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
                "array": x.tolist()
            }
        ]

        op_dict = {
            'operation': 'insert',
            'schema': schema,
            'table': table,
            'records': data
        }

        print(postToHarper(op_dict))

dropSchema()
createSchema()
createTable()
batchInsertTensors(100)
exportTableToCSV()