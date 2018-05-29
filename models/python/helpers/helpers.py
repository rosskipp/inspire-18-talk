import pickle
shotLabels = pickle.loads('../objects/shot_labels.pkl')

def convertShot(shotString):
    return shotLabels[shotString]

