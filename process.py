import json
import pprint

with open("./a.json") as file:
    jsondata = json.load(file)

final_array = []

def build_array(array, data):
    for elem in data:
        if type(data[elem]) is str:
            array.append([elem, data[elem]])
        else:
            array_next = [elem]
            array_bext = []
            build_array(array_bext, data[elem])
            array_next.append(array_bext)
            array.append(array_next)

build_array(final_array, jsondata)