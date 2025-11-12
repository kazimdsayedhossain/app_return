from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

# Example: proxy credentials as environment variable or config
PROXY = os.getenv("YTDLP_PROXY", "http://username:password@142.111.48.253:7030")

@app.route("/audio", methods=["GET"])
def get_audio_link():
    song_name = request.args.get("song")
    if not song_name:
        return jsonify({"error": "Missing required parameter ‘song’"}), 400

    query = f"ytsearch1:{song_name}"
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "format": "bestaudio/best",
        "proxy": PROXY,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            video = info["entries"][0]

        formats = video.get("formats", [])
        audio_url = None
        for f in formats:
            if f.get("vcodec") == "none":
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
