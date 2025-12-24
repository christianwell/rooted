import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)
CORS(app)

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN', '')


@app.route('/api/hello')
def hello():
    return jsonify({'message': 'Hello from Flask!'})


@app.route('/api/slack/user/<user_id>')
def get_slack_user(user_id):
    """Get a Slack user's profile picture by their user ID."""
    if not SLACK_BOT_TOKEN:
        return jsonify({'error': 'SLACK_BOT_TOKEN not configured'}), 500

    response = requests.get(
        'https://slack.com/api/users.info',
        headers={'Authorization': f'Bearer {SLACK_BOT_TOKEN}'},
        params={'user': user_id}
    )
    data = response.json()

    if not data.get('ok'):
        return jsonify({'error': data.get('error', 'Unknown error')}), 400

    user = data['user']
    profile = user.get('profile', {})

    return jsonify({
        'id': user_id,
        'name': profile.get('real_name') or profile.get('display_name'),
        'avatar': profile.get('image_192') or profile.get('image_72'),
        'avatar_large': profile.get('image_512'),
    })


@app.route('/api/slack/users')
def get_slack_users():
    """Get multiple Slack users by IDs (comma-separated)."""
    if not SLACK_BOT_TOKEN:
        return jsonify({'error': 'SLACK_BOT_TOKEN not configured'}), 500

    user_ids = request.args.get('ids', '').split(',')
    users = []

    for user_id in user_ids:
        if not user_id.strip():
            continue
        response = requests.get(
            'https://slack.com/api/users.info',
            headers={'Authorization': f'Bearer {SLACK_BOT_TOKEN}'},
            params={'user': user_id.strip()}
        )
        data = response.json()
        if data.get('ok'):
            user = data['user']
            profile = user.get('profile', {})
            users.append({
                'id': user_id,
                'name': profile.get('real_name') or profile.get('display_name'),
                'avatar': profile.get('image_192') or profile.get('image_72'),
            })

    return jsonify({'users': users})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
