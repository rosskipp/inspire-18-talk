import promote
import pickle
import pandas as pd
import joblib

# Load the pickle file with the model training metrics for meta data
metrics = joblib.load('./objects/model_metrics.pkl')

# load in our saved shot model
MODEL = joblib.load('./objects/log_reg_model.pkl')

# Load the shot labels for the categorical variables
shotLabels = joblib.load('./objects/shot_labels.pkl')

# Function to convert the shot type string to an int for scoring
def convertShotTypeToInt(shotString):
    return shotLabels[shotString]

# instanciate the Promote class with our API information
USERNAME = "USERNAME"
API_KEY = "API_KEY"
PROMOTE_URL = "PROMOTE_URL"

p = promote.Promote(USERNAME, API_KEY, PROMOTE_URL)

def shotPredictor(data):
    # Need to convert the shot type, which comes in as a string, to an int
    data['shotTypeCode'] = convertShotTypeToInt(data['shotType'])
    # Make sure we have a dataframe, and the order of the columns is right
    df = pd.DataFrame.from_records([data])
    df = df[["shotTypeCode", "shotOnEmptyNet", "shotRush", "shotRebound",
                   "shotDistance", "shotAngleAdjusted"]]
    # Run the prediction and return the goal probability
    prediction = MODEL.predict_proba(df)
    return {"shot_prob": prediction[0][1]}


# Test the model
TESTDATA = {"shotType": "SNAP", "shotOnEmptyNet": 0, "shotRebound": 0,
            "shotRush": 0, "shotDistance": 7.071068, "shotAngleAdjusted": 45.0}
print(shotPredictor(TESTDATA))

# add metadata
p.metadata.roc_auc_score = metrics['roc_auc_score']
p.metadata.valid_acc = metrics['valid_acc']

# name and deploy our model
p.deploy("ShotPredictor", shotPredictor, TESTDATA,
         confirm=True, dry_run=False, verbose=2)
