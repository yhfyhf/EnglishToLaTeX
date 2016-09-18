from flask import Flask, request, jsonify
from latex import EnglishToLatex


app = Flask(__name__)


@app.route("/", methods=['POST'])
def english_to_latex():
    english = request.form.get("english")
    status = True
    try:
        latex = EnglishToLatex().to_latex(english)
    except Exception as e:
        latex = e.message
        status = False
    return jsonify({"status": status, "latex": latex})


if __name__ == "__main__":
    app.run()
