from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Post
from schemas import PostSchema

post_schema = PostSchema()
posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/posts', methods=['GET'])
def get_all_posts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    posts = pagination.items

    result = []
    for post in posts:
        result.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author": post.author.username,
            "created_at": post.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify({
        "posts": result,
        "page": page,
        "per_page": per_page,
        "total_posts": pagination.total,
        "total_pages": pagination.pages
    })

@posts_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()

    errors = post_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    user_id = get_jwt_identity()

    new_post = Post(title=data['title'], content=data['content'], user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({"msg": "Post created", "post_id": new_post.id}), 201

@posts_bp.route('/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    data = request.get_json()

    errors = post_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    user_id = get_jwt_identity()

    post = db.session.get(Post, post_id)
    if not post:
        return jsonify({"msg": "Post not found"}), 404

    if int(post.user_id) != int(user_id):
        return jsonify({"msg": "Unauthorized"}), 403

    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    db.session.commit()

    return jsonify({"msg": "Post updated"})

@posts_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    user_id = get_jwt_identity()
    post = db.session.get(Post, post_id)

    if not post:
        return jsonify({"msg": "Post not found"}), 404

    if int(post.user_id) != int(user_id):
        return jsonify({"msg": "Unauthorized"}), 403

    db.session.delete(post)
    db.session.commit()

    return jsonify({"msg": "Post deleted"})

@posts_bp.route('/my-posts', methods=['GET'])
@jwt_required()
def get_my_posts():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    posts = pagination.items

    result = []
    for post in posts:
        result.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author": post.author.username,
            "created_at": post.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify({
        "posts": result,
        "page": page,
        "per_page": per_page,
        "total_posts": pagination.total,
        "total_pages": pagination.pages
    })
