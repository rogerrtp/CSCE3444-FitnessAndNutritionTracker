#!/usr/bin/env python3
import matplotlib.pyplot as plt
import datetime as dt
import io
import base64

def graph(x, y, xlabel, ylabel):
    output = io.BytesIO()
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(output, format='png')
    return base64.b64encode(output.read()).decode('utf-8')
