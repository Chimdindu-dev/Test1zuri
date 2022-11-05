import os
import openai
from flask import Flask, request, abort, jsonify
from flask_cors import CORS, cross_origin
from settings import OPENAI_API_KEY

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

operation_types = {"addition": "+", "subtraction": "-", "multiplication": "*"}

#openai.organization = "org-7A1rvHNcWGQMun2XVbvQxPNH"
openai.api_key = OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")


@app.route('/')
def index():
    return jsonify({
        'success': True,
        'message': 'WORKS'
    })

@app.route('/api/v1.0/calculate', methods=['POST'])
def get_simple_calculation():
    body = request.get_json()

    result = None
    operation_type = None
    body_data_operation = body.get("operation_type", None)

    if body_data_operation != None:
        body_data_operation = body_data_operation.lower()
    
    if body_data_operation in operation_types:
        operation_type = body_data_operation

        firstInt = body.get('x', None)
        secondInt = body.get('y', None)
        if firstInt != None and secondInt != None:
            result = eval(f'{firstInt}{operation_types[operation_type]}{secondInt}')

    else:
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=f"{body_data_operation} \n\n| solution | operation_type |",
            temperature=0,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        if len([ x.strip() for x in response.choices[0].text.split("\n")[-1].split("|") ]) == 4:
            _, result, operation_type, _ = [
            x.strip() 
        for x in response.choices[0].text.split("\n")[-1].split("|")
            ]
        else:
            abort(400)
    result = int(result)

    return jsonify({
        'slackUserName': 'cchimdindu',
        'result': result,
        'operation_type': operation_type,
    })

# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({
#         "success": False,
#         "error": 404,
#         "message": "Not found"
#         }), 404

# @app.errorhandler(422)
# def unprocessable(error):
#     return jsonify({
#         'success': False,
#         'error': 422,
#         'message': 'unprocessable'
#     }), 422

# @app.errorhandler(400)
# def bad_request(error):
#     return jsonify({
#         'success': False,
#         'error': 400,
#         'message': 'Bad Request'
#     }), 400

# @app.errorhandler(405)
# def not_allowed(error):
#     return jsonify({
#         'success': False,
#         'error': 405,
#         'message': 'method not allowed'
#     }), 405

# @app.errorhandler(500)
# def not_successful(error):
#     return jsonify({
#         'success': False,
#         'error': 500,
#         'message': 'Request Not Successful'
#     }), 500


if __name__ == '__main__':
    app.run()
