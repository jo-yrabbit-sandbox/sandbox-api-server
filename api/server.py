from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

# Only if you want to test running directly with Python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)