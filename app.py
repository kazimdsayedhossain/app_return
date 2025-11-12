from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

# Read proxy credentials from environment variables
PROXY_HOST = os.getenv("YTDLP_PROXY_HOST")
PROXY_PORT = os.getenv("YTDLP_PROXY_PORT")
PROXY_USER = os.getenv("YTDLP_PROXY_USER")
PROXY_PASS = os.getenv("YTDLP_PROXY_PASS")

proxy_url = None
if PROXY_HOST and PROXY_PORT:
    # Build proxy string if credentials provided
    if PROXY_USER and PROXY_PASS:
        proxy_url = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
    else:
        proxy_url = f"http://{PROXY_HOST}:{PROXY_PORT}"

@app.route("/")
def index():
    return jsonify({"message": "yt-dlp API is running"}), 200

@app.route("/audio", methods=["GET"])
def get_audio_link():
    song_name = request.args.get("song")
    if not song_name:
        return jsonify({"error": "Missing required parameter ‘song’"}), 400

    query = f"ytsearch1:{song_name}"  # first search result
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "format": "bestaudio/best",
    }
    if proxy_url:
        ydl_opts["proxy"] = proxy_url

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            video = info["entries"][0]

        formats = video.get("formats", [])
        audio_url = None
        for f in formats:
            if f.get("vcodec") == "none":  # audio only
                audio_url = f.get("url")
                break
        if not audio_url:
            audio_url = video.get("url")

        return jsonify({
            "title": video.get("title"),
            "audio_stream_url": audio_url,
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
