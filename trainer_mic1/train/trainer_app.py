from flask import Flask, render_template, jsonify
from trainer_mic1.train.model_trainer import Model_Trainer
import logging, time
import sys 

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

app = Flask(__name__)

# Routes
@app.route("/")
def home():
    return render_template('index.html', route="home")


@app.route("/train",methods=["GET", "POST"])
def train():

    MT = Model_Trainer('ingest/train.csv/./data/bin/train_ingest.csv')

    Training = MT.Training()

    if Training:
        message = {"TrainingStatus": f"{Training} Complete", "Time": time.asctime()}
        logging.info(message)
        return jsonify(message), 200    
    else:
        return jsonify({"TraningStatus":f"{Training} InComplete" }), 404



if __name__ == "__main__":
    # app.run(debug=True) # for local use
    app.run(debug=True, host="0.0.0.0", port=4444)  # Accessible from outside Docker
