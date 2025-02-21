from flask import Blueprint, request, jsonify, g

from .db_models import Post

from .decorators import rate_limit, token_required

home_page_bp = Blueprint('home_page', __name__)

@home_page_bp.route('/', methods=['GET'])
@rate_limit # Apply rate limiting
@token_required
def home():
    try:

        user_id = g.user_id  # Access the user ID

        previous_posts = Post.query.filter_by(user_id=user_id).all()

        result = []
        for post in previous_posts:
            title = post.title
            post_id = post.id
            content = post.content
            generated_post = post.generated_post
            style = post.tone_and_style
            platform = post.platform

            result.append({
                "title": title,
                "content": content,
                "generated_post": generated_post,
                "style": style,
                "platform": platform
            })

        return(jsonify({"result": result})), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500