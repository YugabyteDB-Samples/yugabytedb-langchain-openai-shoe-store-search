from flask import Flask, request, jsonify

app = Flask(__name__)

from llm_db import query_database;

@app.route('/queries', methods=['POST'])
def handle_post_request():
    data = request.json
    db_response = query_database(data['user_prompt'])
    return jsonify(db_response)

if __name__ == '__main__':
    app.run(debug=True, port=8080)