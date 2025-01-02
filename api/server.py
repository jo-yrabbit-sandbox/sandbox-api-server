from flask import Flask, request, jsonify

import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# Note: If you change attribute name `app` for this flask server,
# make sure you edit the Dockerfile gunicorn command arg too
app = Flask(__name__)


@app.route('/api/v1/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})


@app.route('/api/v1/messages/latest', methods=['GET'])
def get_latest_message():
    """Get latest message"""
    try:
        state = request.args.get('state')
        if not state:
            return jsonify({'error': 'Missing required field `state`'})  # return Bad request error 400
        
        # message = redis_handler.get_latest_message(state)  # TODO: Enable later
        message = 'haha'
        return jsonify({'message': message})
    
    except Exception as e:
        message = f'Error getting latest message - {e.args}'
        logger.error(message)
        return jsonify({'error': message})  # return Internal server error 500



# Only if you want to test running directly with Python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)