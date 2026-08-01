from flask import Flask, render_template

app = Flask(__name__)

tasks = []

@app.route("/")
def index():
    return render_template("index.html", tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)
