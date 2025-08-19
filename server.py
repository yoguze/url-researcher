from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
# 公開する場合はフロントエンドのドメインを指定してください
CORS(app, resources={r"/api/*": {"origins": ["https://url-researcher.onrender.com"]}})

# Google Safe Browsing APIキー（環境変数から読み込む）
API_KEY = os.getenv("GOOGLE_API_KEY")
SAFE_BROWSING_URL = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"

@app.route("/")
def index():
    with open("index.html", encoding="utf-8") as f:
        return render_template_string(f.read())

@app.route("/api/check_url", methods=["POST"])
def check_url():
    data = request.get_json()
    url = data.get("url", "").lower()

    body = {
        "client": {
            "clientId": "my-url-checker",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION"
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    try:
        response = requests.post(SAFE_BROWSING_URL, json=body)
        result = response.json()

        if "matches" in result:
            threat = result["matches"][0]["threatType"]
            status = "危険"
            reason = f"Google Safe Browsingにより {threat} と判定"
        else:
            # HTTPSチェックも追加
            if url.startswith("http://"):
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
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render用に0.0.0.0で起動
    app.run(host="0.0.0.0", port=5000)

