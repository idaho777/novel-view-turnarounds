import json
import os
import sys


# 1 argument: directory with label.json
label_dir = sys.argv[1]
label_path = os.path.join(label_dir, 'label.json')
with open(sys.argv[1], 'r') as f:
    dj = json.load(f)

new_dj = dict()

labels = dj

l = []
for k in labels:
    l.append([k, labels[k]])

new_dj['labels'] = l

dataset_path = os.path.join(label_dir, 'dataset.json')
with open(dataset_path, 'w') as f:
    json.dump(new_dj, f)
