import pandas as pd
import matplotlib.pyplot as plt
import os
import io


def get_paths(input, ext):
    return [f for f in os.listdir(input) if f.endswith(ext)]

def parse_csv(path):
    with open(path) as file:
        data = io.StringIO()
        timestamp = ""
        line = file.readline()
        header = f"timestamp;{line[2:].rsplit(';', 1)[0]}\n"
        data.writelines([header])
        for line in file.readlines():
            if line.startswith('# POWERON'):
                splited = line.rsplit(' ')
                timestamp = line[10:].strip()
            else:
                line = timestamp + ";" + line.rsplit(';', 1)[0] + "\n"
                data.writelines([line])
    data.seek(0)
    return pd.read_csv(data, sep=';', parse_dates=['timestamp'])


def process(input, output="output"):
    dtf = parse_csv(input)
    path = output+"/"+str(dtf['timestamp'][0]).split()[0]+"/"
    if not os.path.exists(path):
        os.makedirs(path)
    for col in range(2, len(dtf.columns)):
        plot = dtf.plot(x="time", y=dtf.columns[col])
        fig = plot.get_figure()
        fig.savefig(path+str(dtf.columns[col]).replace("/", "")+".png")
    return str(dtf['timestamp'][0]).split()[0]
