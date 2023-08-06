from d3m.container import Dataset
import os.path
import sys

ddir = sys.argv[1]
path = os.path.abspath(ddir)
dset = os.path.basename(ddir)
url = "file://%s" % os.path.abspath("%s/%s_dataset/datasetDoc.json" % (ddir, dset))
print(url)
dataset = Dataset.load(url)
print(dataset.metadata.query(())['description'])

