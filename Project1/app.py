from flask import Flask, request, render_template
from main import ask_ai  

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    user_input = ""
    response = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        response = ask_ai(user_input)
    return render_template("index.html", response=response, user_input=user_input)

if __name__ == "__main__":
    app.run(debug=True)
