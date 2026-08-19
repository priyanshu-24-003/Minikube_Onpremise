from flask import Flask, render_template, jsonify
from trainer_mic1.Ingest import data_ingestion
import time
import logging
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


@app.route("/train", methods=["GET", "POST"])
def train():


    I = data_ingestion.Ingestion('main.csv')
    Ingestion = I.Ingesting()
    if Ingestion:
        message = {"TrainingStatus": f"{Ingestion} Complete", "Time": time.asctime()}
        logging.info(message)
        return jsonify(message), 200    
    else:
        return jsonify({"TraningStatus":f"{Ingestion} InComplete" }), 404


if __name__ == "__main__":
    # app.run(debug=True) # for local use
    app.run(debug=True, host="0.0.0.0", port=3333)  # Accessible from outside Docker
