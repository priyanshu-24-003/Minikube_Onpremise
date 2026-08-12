from flask import Flask, render_template
from trainer_mic1.train.model_trainer import Model_Trainer

app = Flask(__name__)

# Routes
@app.route("/")
def home():
    return render_template('index.html', route="home")


@app.route("/train")
def train():

    MT = Model_Trainer('ingest/train.csv/./data/bin/train_ingest.csv')

    MT.Training()

    return render_template('index.html', route='Training-model-training')



if __name__ == "__main__":
    # app.run(debug=True) # for local use
    app.run(debug=True, host="0.0.0.0", port=4444)  # Accessible from outside Docker
