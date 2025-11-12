from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message": "yt‑dlp API is running"}), 200

@app.route("/extract", methods=["GET"])
def extract():
    video_url = request.args.get("url")
    if not video_url:
        return jsonify({"error": "Missing required parameter ‘url’"}), 400

    try:
        opts = {
            "quiet": True,
            "skip_download": True,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
        
        # Selecting the direct url for best format
        formats = info.get("formats", [])
        if formats:
            # pick best (usually last or first depending on sort)
            best = formats[-1]
            direct_url = best.get("url")
        else:
            direct_url = info.get("url")

        return jsonify({
            "title": info.get("title"),
            "direct_url": direct_url,
            "info": info
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Use port 10000 to match your Render deployment
    app.run(host="0.0.0.0", port=10000)
