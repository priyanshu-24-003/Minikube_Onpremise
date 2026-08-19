
from flask import Flask, render_template, jsonify
from trainer_mic1.push.model_pusher import Model_Pusher
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


@app.route("/train")
def train():

    MP = Model_Pusher("ingest/test.csv/./data/bin/test_ingest.csv")

    Pushing_Stage = MP.Pusher()
    if Pushing_Stage != "Pusher Method Failed":
        message = {"TraningStatus": f"{Pushing_Stage} Complete", "Time": time.asctime()}
        logging.info(message)
        return jsonify(message), 200    
    else:
        return jsonify({"TraningStatus":f"{Pushing_Stage} InComplete" }), 404


if __name__ == "__main__":
    # app.run(debug=True) # for local use
    app.run(debug=True, host="0.0.0.0", port=5555)  # Accessible from outside Docker
