# app.py
from flask import Flask, request, jsonify
from doc_retrieval import provide_ans
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route('/query', methods=['POST'])
def query_documents():
    user_query = request.form.get('user_query')
    image = request.files.get('image')
    # print(image)
    if not user_query:
        return jsonify({"error": "No query provided"}), 400
    if image == None:
        prompt_with_context, response, sources = provide_ans(user_query)
    else:
        prompt_with_context, response, sources = provide_ans(user_query, image)

    return jsonify({"answer": response, "context": prompt_with_context, "sources": sources})

if __name__ == '__main__':
    app.run(debug=True)