from flask import Blueprint, request, jsonify, render_template
from services.youtube_service import search_youtube

youtube_bp = Blueprint("youtube", __name__)

# API REST
@youtube_bp.route("/api/youtube", methods=["GET"])
def youtube_api():
    query = request.args.get("q", "tecnología")
    videos = search_youtube(query)

    return jsonify([
        {
            "title": v.title,
            "channel": v.channel,
            "video_id": v.video_id,
            "thumbnail": v.thumbnail
        } for v in videos
    ])

# Vista web MVC
@youtube_bp.route("/youtube", methods=["GET", "POST"])
def youtube_view():
    query = request.form.get("query") if request.method == "POST" else "programación"
    videos = search_youtube(query)
    return render_template("youtube.html", videos=videos, query=query)
    
