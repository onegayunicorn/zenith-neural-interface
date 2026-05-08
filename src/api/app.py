from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/zenith/status')
def status():
    return jsonify({"status": "OMEGA ACTIVE", "unity_index": 1.000})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
