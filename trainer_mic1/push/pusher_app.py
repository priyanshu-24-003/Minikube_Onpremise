
from flask import Flask, render_template
from trainer_mic1.push.model_pusher import Model_Pusher

app = Flask(__name__)

# Routes
@app.route("/")
def home():
    return render_template('index.html', route="home")


@app.route("/train")
def train():

    MP = Model_Pusher("ingest/test.csv/./data/bin/test_ingest.csv")

    MP.Pusher()

    return render_template('index.html', route='Training-model-pushing')



if __name__ == "__main__":
    # app.run(debug=True) # for local use
    app.run(debug=True, host="0.0.0.0", port=5555)  # Accessible from outside Docker
