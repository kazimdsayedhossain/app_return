from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return "yt-dlp API is running"

@app.route('/extract', methods=['GET'])
def extract():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "missing url"}), 400
    try:
        ydl_opts = {'quiet': True, 'skip_download': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({"title": info.get("title"), "url": info.get("url")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
