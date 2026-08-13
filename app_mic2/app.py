from flask import Flask, render_template, request
import requests
import time
from src_utils import Credentials, connect_s3
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html", )

@app.route("/predict", methods=["GET", "POST"])
def prediction():
    if request.method == "POST":
        attendance = float(request.form.get("attendance"))
        prev_score = float(request.form.get("prev_score"))

        message = f"Predictions are {attendance/prev_score}, "

        #data preparation
        input_data = pd.DataFrame({"attendance_rate":[attendance,], "previous_score":[prev_score]})

        # Fetch model/production and encoder from s3 Bucket.
        model_path = "model/Production//./data/bin/model.pkl"
        encoder_path = "model/encoder/./data/bin/encoder.pkl"

        client = connect_s3(Credentials.s3_bucket, Credentials.aws_access_key, Credentials.aws_secret_key)

        model = client.fetch_model_typ(model_path)
        encoder = client.fetch_model_typ(encoder_path)

        #label Mapping to know the labels.
        label_maps = dict(zip(range(len(encoder.classes_)), encoder.classes_))      

        # Making prediction using Production model.
        prediction = "PASS" if label_maps[model.predict(input_data)[0]]=="Yes" else "FAIL"
        message = f"This Student is more likely to  {prediction} the exam."

    return render_template('index.html', message=message)    


@app.route("/train", methods=["GET", "POST"])
def retrain_model():

    #This Url intracts with 3 different microservices (Ingestion, trainer, pusher)

    #local
    # Urls = {
    #     "Ingest":"http://localhost:3333/train",
    #     "Trainer":"http://localhost:4444/train",
    #     "Pusher":"http://localhost:5555/train",
    # }

    #Production
    Urls = {
        "Ingest": Credentials.INGEST_SERVICE_URL,
        "Trainer": Credentials.TRAINER_SERVICE_URL,
        "Pusher": Credentials.PUSHER_SERVICE_URL,
    }

    TrainStatus = True
    #Running Entire Pipeline.
    for key, value in Urls.items():
        print(f"Running Stage :{key}")
        try:
            response = requests.get(value, timeout=5)
            print(response.raise_for_status)
            print(response.text)
            print(f"Stage {key} Finish")
            continue
        except Exception as e:
            print(f"Error in {key} stage : {e}")
            TrainStatus = False
            break

    return render_template("index.html", train_status="Training is Complete" if TrainStatus == True else "Training Wasn't Successfull" )




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)