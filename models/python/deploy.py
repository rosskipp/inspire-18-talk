import promote
import helpers

# load in our saved model weights
from sklearn.externals import joblib
WEIGHTS = joblib.load('./objects/log_reg_model.pkl')

# instanciate the Promote class with our API information
USERNAME = "USERNAME"
API_KEY = "APIKEY"
PROMOTE_URL = "https://promote.c.yhat.com/"

p = promote.Promote(USERNAME, API_KEY, PROMOTE_URL)

def shotPredictor(data):
    
    
    prediction = getclass.get_classname(WEIGHTS.predict(data).tolist())
    return {"prediction": prediction}


# Add two flowers as test data
TESTDATA = {"players": [{"player": {"id": 8477444, "fullName": "Andre Burakovsky", "link": "/api/v1/people/8477444"}, "playerType": "Scorer", "seasonTotal": 1}, {"player": {"id": 8474189, "fullName": "Lars Eller", "link": "/api/v1/people/8474189"}, "playerType": "Assist", "seasonTotal": 9}, {"player": {"id": 8476880, "fullName": "Tom Wilson", "link": "/api/v1/people/8476880"}, "playerType": "Assist", "seasonTotal": 9}, {"player": {"id": 8476883, "fullName": "Andrei Vasilevskiy", "link": "/api/v1/people/8476883"}, "playerType": "Goalie"}], "result": {"event": "Goal", "eventCode": "TBL295",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            "eventTypeId": "GOAL", "description": "Andre Burakovsky (1) Wrist Shot, assists: Lars Eller (9), Tom Wilson (9)", "secondaryType": "Wrist Shot", "strength": {"code": "EVEN", "name": "Even"}, "gameWinningGoal": false, "emptyNet": false}, "about": {"eventIdx": 162, "eventId": 295, "period": 2, "periodType": "REGULAR", "ordinalNum": "2nd", "periodTime": "08:59", "periodTimeRemaining": "11:01", "dateTime": "2018-05-24T01:27:24Z", "goals": {"away": 2, "home": 0}}, "coordinates": {"x": 76, "y": -15}, "team": {"id": 15, "name": "Washington Capitals", "link": "/api/v1/teams/15", "triCode": "WSH"}}
print(shotPredictor(TESTDATA))

# add metadata
p.metadata.n_neighbors = WEIGHTS.n_neighbors
p.metadata["leaf_size"] = WEIGHTS.leaf_size

# name and deploy our model
p.deploy("shotPredictor", irisClassifier, TESTDATA,
         confirm=True, dry_run=False, verbose=2)

# once our model is deployed and online, we can send data and recieve predictions
# p.predict("IrisClassifier", TESTDATA)
