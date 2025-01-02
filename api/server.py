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
            return jsonify({'error': 'Missing required field `state`'})  # return Bad request error 400

        logger.debug(f'Processing: {state}')

        message = redis_handler.get_latest_message(state)
        return jsonify({'message': message + state})

    except Exception as e:
        message = f'Error getting latest message - {e.args[0]}'
        logger.error(message)
        return jsonify({'error': message})  # return Internal server error 500


# Only if you want to test running directly with Python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)