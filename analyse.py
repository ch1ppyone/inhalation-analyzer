import pandas as pd
import matplotlib.pyplot as plt
import os
import io
import time


def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()

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
    timestamps = []
    filepaths = get_paths(input, ".LOG")
    for file in progressBar(filepaths, prefix = 'Progress:', suffix = 'Complete', length = 50):
        dtf = parse_csv(input+"/"+file)
        path = output+"/"+str(dtf['timestamp'][0])+"/"
        timestamps.append(str(dtf['timestamp'][0]))
        if not os.path.exists(path):
            os.makedirs(path)
        for col in range(2, len(dtf.columns)):
            plot = dtf.plot(x="time", y=dtf.columns[col])
            fig = plot.get_figure()
            fig.savefig(path+str(dtf.columns[col]).replace("/", "")+".png")
            time.sleep(0.1)
    return timestamps
    
