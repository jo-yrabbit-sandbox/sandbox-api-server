from flask import Flask, request, jsonify
# from flask_cors import CORS  # TODO: Enable for auth

from api.redis_handler import RedisHandler

import logging
import os

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# Note: If you change attribute name `app` for this flask server,
# make sure you edit the Dockerfile gunicorn command arg too
app = Flask(__name__)
# CORS(app)  # TODO: Enable for auth
redis_handler = RedisHandler()
redis_handler.start(redis_host=os.getenv('REDIS_HOST', 'localhost'),
                    redis_port=int(os.getenv('REDIS_PORT', 6397)),
                    redis_password=os.getenv('REDIS_PASSWORD'))


@app.route('/api/v1/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})


@app.route('/api/v1/messages/latest', methods=['GET'])
def get_latest_message():
    """Get latest message"""
    try:
        state = request.args.get('state')  # TODO:  Add bot_id to accommodate multiple bots
        if not state:
            return jsonify({'error': 'Missing required field `state`'}), 400
        logger.debug(f'Processing: {state}')

        message = redis_handler.get_latest_message(state)
        return jsonify({'message': str(message)})

    except Exception as e:
        message = f'Error getting latest message - {e.args[0]}'
        logger.error(message)
        return jsonify({'error': message}), 500


@app.route('/api/v1/messages', methods=['GET'])
def get_messages():
    """Get messages"""
    try:
        # bot_id = request.args.get('bot_id')  # TODO:  Add bot_id to accommodate multiple bots
        limit = request.args.get('limit')
        if not state:
            return jsonify({'error': 'Missing required field `limit`'}), 400
        state = request.args.get('state')
        if not state:
            return jsonify({'error': 'Missing required field `state`'}), 400

        logger.debug(f'Processing: {state}')
        messages = redis_handler.get_messages(state, limit=limit)

        return jsonify({'messages': messages})

    except Exception as e:
        m = f'Error getting last {limit} messages - {e.args[0]}'
        logger.error(m)
        return jsonify({'error': m}), 500


@app.route('/api/v1/messages', methods=['POST'])  # TODO: Add following decorators later: @require_api_key @limiter.limit("30 per minute")
def store_message():
    """Store a new message"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['bot_id', 'message']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Validate message structure
        message = data['message']
        if not all(field in message for field in ['state', 'text', 'timestamp']):
            return jsonify({"error": "Invalid message structure"}), 400

        # Store message
        stored = redis_handler.store_message(
            bot_id=data['bot_id'],
            state=message['state'],
            text=message['text'],
            timestamp=message['timestamp'],
        )

        return jsonify({"success": True, "message_id": stored}), 201

    except Exception as e:
        m = f"Error storing message: {str(e.args[0])}"
        logger.error(m)
        return jsonify({"error": f"Internal server error: {m}"}), 500