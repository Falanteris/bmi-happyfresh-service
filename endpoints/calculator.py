from flask import Flask, jsonify, render_template, send_from_directory, request, make_response, Blueprint
from schema import BMISchema
from module.calculator import BMICalculator
app = Blueprint('transfer', __name__,url_prefix="/")


@app.route("/",methods=["GET"])
def calculate_bmi():
    try:
        query = request.query_string.decode()
        query_data = filter(None,query.split("&"))
        json_query = {}
        for data in query_data:
            item = data.split("=")
            json_query[item[0]] = item[1]
    except Exception as e:
        return {"Error":"Invalid Query Parameter"}, 400
    try:
        data = BMISchema().load(json_query)
    except Exception as e:
        err = str(e)
        if hasattr(e,"normalized_messages"):
          err = e.normalized_messages()
        return {"error":"Entry data is not valid","details":err},400
    
    return BMICalculator(**data).calculate().check(),200
