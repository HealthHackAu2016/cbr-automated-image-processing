import sklearn

# features of width, height, colour
features = []
# labels of 1 if is a seed and 0 if not a seed
labels = []

clf = tree.DescisionsTreeClassifier()
clf = clf.fit(features, labels)

# input tuple
clf.predict()