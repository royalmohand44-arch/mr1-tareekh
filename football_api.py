from flask import Flask, jsonify
from flask_cors import CORS
import feedparser, urllib.request, ssl

app = Flask(__name__)
CORS(app)
ctx = ssl._create_unverified_context()

SOURCES = [
    "https://bbci.co.uk",
    "https://skysports.com",
    "https://espn.com"
]

@app.route("/api/news")
def get_news():
    errors = []
    for url in SOURCES:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            xml = urllib.request.urlopen(req, context=ctx, timeout=8).read()
            feed = feedparser.parse(xml)
            if feed.entries:
                articles = [{"title": e.title, "summary": e.get("summary", ""), "link": e.link, "published": e.get("published", "")} for e in feed.entries[:10]]
                return jsonify({"status": "success", "source": url, "count": len(articles), "news": articles})
        except Exception as err:
            errors.append(f"{url}: {str(err)}")
    return jsonify({"status": "error", "details": errors})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)