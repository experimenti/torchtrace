# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import http.client as http
import harperdb as hdb
import datetime as dt

loss_history = []


now = dt.datetime.now()

writer = pd.ExcelWriter('inspection.xlsx', engine='xlsxwriter')

def frameToExcel(narray, label):
    df = pd.DataFrame(narray)
    df.to_excel(writer, sheet_name=label)

def frameToHarper(narray, label):
    hdb.insert_narray(narray, label)

# N is batch size; D_in is input dimension;
# H is hidden dimension; D_out is output dimension.
N, D_in, H, D_out = 64, 1000, 100, 10
# Create random input and output data
#x = np.random.randn(N, D_in)
x = np.full((N, D_in), .24)
#y = np.random.randn(N, D_out)

# y = np.fromfunction(lambda 1, 2: N, D_out)
# y = np.fromfunction(lambda i, j: (i + 1 + j)**2 * .001, (N, D_out), dtype=int)
y = np.full((N, D_out), .25)

# Randomly initialize weights
w1 = np.random.randn(D_in, H)
w2 = np.random.randn(H, D_out)

learning_rate = 1e-6

hdb.dropSchema()
hdb.createSchema()
hdb.createTable('x')
hdb.createTable('y')
hdb.createTable('w1')
hdb.createTable('w2')
hdb.createTable('h_relu')
hdb.createTable('y_pred')
hdb.createTable('grad_y_pred')
hdb.createTable('grad_w2')

for t in range(500):
    # Forward pass: compute predicted y
    h = x.dot(w1)
    h_relu = np.maximum(h, 0)
    y_pred = h_relu.dot(w2)

    # Compute and print loss
    loss = np.square(y_pred - y).sum()
    loss_history.append(loss)

    # print(t, loss)

    # Backprop to compute gradients of w1 and w2 with respect to loss
    grad_y_pred = 2.0 * (y_pred - y)
    grad_w2 = h_relu.T.dot(grad_y_pred)
    grad_h_relu = grad_y_pred.dot(w2.T)
    grad_h = grad_h_relu.copy()
    grad_h[h < 0] = 0
    grad_w1 = x.T.dot(grad_h)
    # Update weights
    w1 -= learning_rate * grad_w1
    w2 -= learning_rate * grad_w2

    #Dump the weights to HDB
    if(t < 100):
        frameToHarper(w1, 'w1')
        frameToHarper(w2, 'w2')
    
    if(t == 0):
        n1=dt.datetime.now()

        frameToHarper(x, 'x')
        frameToHarper(y, 'y')
        frameToHarper(w1, 'w1')
        frameToHarper(w2, 'w2' )
        frameToHarper(h_relu, 'h_relu')
        frameToHarper(y_pred, 'y_pred')
        frameToHarper(grad_y_pred, 'grad_y_pred')
        frameToHarper(grad_w2, 'grad_w2')

        n2=dt.datetime.now()

        print("HarperDB elapsed time: ")
        diff = n2 - n1
        elapsed_ms = (diff.days * 86400000) + (diff.seconds * 1000) + (diff.microseconds / 1000)
        print(elapsed_ms)

        n1x=dt.datetime.now()

        frameToExcel(x, 'x')
        frameToExcel(y, 'y')
        frameToExcel(w1, 'w1')
        frameToExcel(w2, 'w2')
        frameToExcel(h_relu, 'h_relu')
        frameToExcel(y_pred, 'y_pred')
        frameToExcel(grad_y_pred, 'grad_y_pred')
        frameToExcel(grad_w2, 'grad_w2')

        n2x=dt.datetime.now()
        
        diff = n2x - n1x
        elapsed_ms = (diff.days * 86400000) + (diff.seconds * 1000) + (diff.microseconds / 1000)
        print("Elapsed time for EXCEL: ")
        print(elapsed_ms)

    if(t == 499):
        frameToExcel(y_pred, 'y_final_pred')

        history = pd.DataFrame.from_dict(loss_history)
        history.to_excel(writer, sheet_name='loss')

writer.save()
writer.close()
