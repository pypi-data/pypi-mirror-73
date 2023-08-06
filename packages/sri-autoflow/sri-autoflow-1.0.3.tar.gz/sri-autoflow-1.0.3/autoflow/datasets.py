import plac
import json
import os

tasks = []

def json_rec(d, problem, what):
    doc = "%s/%s/%s_%s/%sDoc.json" % (d, problem, problem, what, what)
    with open(doc) as fh:
        rec = json.load(fh)
    return rec

def problem_attributes(d, problem):
    rec = json_rec(d, problem, 'problem')
    type_ = rec['about']['taskType']
    try:
        subtype = rec['about']['taskSubType']
    except KeyError:
        subtype = ''
    return { 'type': type_, 'subtype': subtype }

def data_attributes(d, problem):
    rec = json_rec(d, problem, 'dataset')
    types = [ r['resType'] for r in rec['dataResources']]
    return { 'types': ' '.join(types) }


def main(*data_dirs):
    print("Name,Task Type,Task Subtype,Resource Types")
    for d in data_dirs:
        for problem in os.listdir(d):
            patt = problem_attributes(d, problem)
            datt = data_attributes(d, problem)
            tasks.append((problem, patt['type'], patt['subtype'], datt['types']))
    for problem, type_, subtype, dtypes in sorted(tasks, key=lambda x: x[0]):
        print("%s,%s,%s,%s" % (problem, type_, subtype, dtypes))


plac.call(main)