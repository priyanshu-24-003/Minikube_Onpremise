from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    if request.method == "POST":
        attendance = float(request.form.get("attendance"))
        prev_score = float(request.form.get("prev_score"))
        message = f"Predictions are {attendance/prev_score}, "
    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)