import os
import json

yolo_results = 'results\\yolo9000'
objects_in_corpus = []

def get_objects(ppn):
    all_objects = []
    file = yolo_results + ppn + '_objects.json'
    with open(file, 'r') as myfile:
        data = myfile.read()
        data = data.replace("\\", "/")
        y = json.loads(data)
        for x in range(0, len(y)):
            element = y[x]
            z = element.get("objects")
            for a in range(0, len(z)):
                b = z[a]
                obj = b.get('name')
                if obj not in all_objects:
                    all_objects.append(obj)
    print(all_objects)
    return all_objects

for subdir, dirs, files in os.walk(yolo_results):
    for filename in files:
        print(filename)
        ppn = filename[0:12]
        objects = get_objects(ppn)
        for x in range(0,len(objects)):
            if objects[x] not in objects_in_corpus:
                objects_in_corpus.append(objects[x])
                objects_in_corpus.sort()
                print(objects_in_corpus)

