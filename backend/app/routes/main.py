from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return jsonify({
        "message": "Scout Backend API",
        "version": "1.0.0",
        "status": "running"
    })

@main_bp.route('/health')
def health():
    return jsonify({
        "status": "healthy"
    })