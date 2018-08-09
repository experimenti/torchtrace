# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import http.client as http
import json
import urllib.request
import base64
import requests


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

    return response.json()


def tensortoHarperDB():
    print("Building Frame")

    D_in, D_out = 64, 100

    # Create random input and output data
    x = np.random.randn(D_in, D_out)


# createSchema()
# createTable('x')
tensortoHarperDB()
