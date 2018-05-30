import promote
import pickle
import pandas as pd
from sklearn.externals import joblib


shotLabels = joblib.load('./objects/shot_labels.pkl')
metrics = joblib.load('./objects/model_metrics.pkl')

def convertShotTypeToInt(shotString):
    return shotLabels[shotString]

# load in our saved shot model
MODEL = joblib.load('./objects/log_reg_model.pkl')

# instanciate the Promote class with our API information
USERNAME = "ross"
API_KEY = "d580d451-06b9-4c10-a73f-523adca5f48c"
PROMOTE_URL = "http://localhost:3000"

p = promote.Promote(USERNAME, API_KEY, PROMOTE_URL)

def shotPredictor(data):
    data['shotTypeCode'] = convertShotTypeToInt(data['shotType'])
    df = pd.DataFrame.from_records([data])
    df = df[["shotTypeCode", "shotOnEmptyNet", "shotRush", "shotRebound",
                   "shotDistance", "shotAngleAdjusted"]]
    prediction = MODEL.predict_proba(df)
    return {"shot_prob": prediction[0][1]}


# Add two flowers as test data
TESTDATA = {"shotType": "SNAP", "shotOnEmptyNet": 0, "shotRebound": 0,
            "shotRush": 0, "shotDistance": 7.071068, "shotAngleAdjusted": 45.0}
print(shotPredictor(TESTDATA))

# add metadata
p.metadata.roc_auc_score = metrics['roc_auc_score']
p.metadata.valid_acc = metrics['valid_acc']

# name and deploy our model
p.deploy("ShotPredictor", shotPredictor, TESTDATA,
         confirm=True, dry_run=False, verbose=2)
