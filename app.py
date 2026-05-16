from flask import Flask, render_template, request, jsonify
from checker import check_password_strength, generate_password

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check():
    data = request.get_json(silent=True) or {}
    password = data.get("password", "")
    result = check_password_strength(password)
    return jsonify(result)


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    length = int(data.get("length", 16))
    use_upper = bool(data.get("use_upper", True))
    use_lower = bool(data.get("use_lower", True))
    use_digits = bool(data.get("use_digits", True))
    use_symbols = bool(data.get("use_symbols", True))

    password = generate_password(
        length=length,
        use_upper=use_upper,
        use_lower=use_lower,
        use_digits=use_digits,
        use_symbols=use_symbols,
    )
    strength = check_password_strength(password)

    return jsonify({"password": password, "strength": strength})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
