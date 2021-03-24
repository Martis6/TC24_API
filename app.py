from database import connect_db, create_table, data_to_db, last10
from prep import preprocess
from flask import Flask, request
import json
import pickle

with open("lregression.pkl", "rb") as lreg:
  model = pickle.load(lreg)

app = Flask(__name__)

@app.route("/")
def root():
  """Function returns welcoming message."""
  return "<h2>2nd Capstone Project</h2>" \
    "<p> Path '/predict' for price prediction or '/history' for last 10 predictions.</p>"

@app.route("/predict", methods=["POST"])
def predict():
  """Function takes input data via POST request and returns price prediction."""
  try:
    data = preprocess(request.data)
  except:
    return json.dumps({"Error": "preprocessing failed"}), 400
  try:
    prediction = model.predict(data)
  except(ValueError, RuntimeError, TypeError, NameError):
    return json.dumps({"Error": "Prediction failed"}), 400

  create_table()
  raw = pd.DataFrame(json.loads(request.data)["input"])
  data_to_db(input_df=raw, pred=prediction)
  return json.dumps({"Predicted price": list(prediction)}), 200

@app.route("/history", methods=["GET"])
def history():
  """Function returns last 10 predictions in JSON format."""

  db_data = last10()
  return json.dumps({"Last 10 predictions": db_data}), 200

if __name__ == "__main__":
  app.run(debug=False)