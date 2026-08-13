from flask import Flask, render_template
from trainer_mic1.Ingest import data_ingestion

app = Flask(__name__)

# Routes
@app.route("/")
def home():
    return render_template('index.html', route="home")


@app.route("/train")
def train():

    I = data_ingestion.Ingestion('main.csv')
    I.Ingesting()

    return render_template('index.html', route='Training-Ingestion')



if __name__ == "__main__":
    # app.run(debug=True) # for local use
    app.run(debug=True, host="0.0.0.0", port=3333)  # Accessible from outside Docker
