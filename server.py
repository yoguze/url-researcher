from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

blacklist = [
    "malicious.com",
    "phishing-site.org",
    "evil.example"
]

# HTMLもFlaskから返す
@app.route("/")
def index():
    return render_template_string(open("index.html", encoding="utf-8").read())

@app.route("/api/check_url", methods=["POST"])
def check_url():
    data = request.get_json()
    url = data.get("url", "").lower()

    if any(bad in url for bad in blacklist):
        status = "危険"
        reason = "既知の危険URLに一致"
    elif url.startswith("http://"):
        status = "注意"
        reason = "HTTPSではなくHTTPを使用"
    else:
        status = "安全"
        reason = "既知の危険情報なし"

    return jsonify({
        "url": url,
        "status": status,
        "reason": reason
    })

if __name__ == "__main__":
    app.run(debug=True)
