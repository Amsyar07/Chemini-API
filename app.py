from flask import Flask, request, jsonify
from flask_cors import CORS

from chemistry.chemical_equation import ChemicalEquation
from llm_api_request import LLMsAPIRequests



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def root():
    return "Welcome, flask app is operationg"


@app.route("/balance", methods=["POST"])
def balance():
    if request.is_json:
        data = request.get_json()
        reactants = data.get('reactants', [])
        products = data.get('products', [])
        return jsonify({
            "balanced_equation" : ChemicalEquation(reactants, products).stoichimetric_equation()
            })
    return "Request must be JSON", 400



@app.route("/ai/v1", methods=["POST"])
def ai():
    if request.is_json:
        data = request.get_json()
        prompt = data.get('prompt', '')
        image_bytes = data.get('image_bytes', None)
        llm_request = LLMsAPIRequests(prompt, image_bytes=image_bytes, host_url=request.host_url)
        return jsonify({
            "response": llm_request.get_response()
        })
    return "Request must be JSON", 400