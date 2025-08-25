# URL セーフチェック API (Flask)

このプロジェクトは **Flask** を使って URL の安全性を判定する簡単な API サーバーです。  
Google Safe Browsing API を利用し、HTTP/HTTPS のチェックも行います。

3. 初期設定
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["https://url-researcher.onrender.com"]}})

/api/* に対するリクエストは https://url-researcher.onrender.com からのアクセスを許可。

API_KEY = os.getenv("GOOGLE_API_KEY")
SAFE_BROWSING_URL = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"

Google Safe Browsing API のエンドポイントを設定。
GOOGLE_API_KEY を環境変数から読み込む。

5. URLチェックの仕組み
data = request.get_json()
url = data.get("url", "").lower()
リクエストJSONから url を取得。

body = {
    "client": {"clientId": "my-url-checker", "clientVersion": "1.0"},
    "threatInfo": {
        "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
        "platformTypes": ["ANY_PLATFORM"],
        "threatEntryTypes": ["URL"],
        "threatEntries": [{"url": url}]
    }
}
Google Safe Browsing API に送るリクエストボディ。
threatTypes に代表的な脅威を指定。