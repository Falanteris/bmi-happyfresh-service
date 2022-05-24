from datetime import datetime
from flask import  request, Blueprint
from schema import BMISchema
from module.calculator import BMICalculator
from prometheus_client import Gauge,Counter

metrics = {
            "process_time": Gauge("BMI_SERVER_PROCESS_TIME",documentation="Waktu pemrosesan BMI dalam microsecods"),
            "recent_input_bmi": Gauge("BMI_SERVER_RECENTLY_INPUTTED","Data BMI terbaru",["value","timestamp"] ),
            "total_entries": Counter("BMI_SERVER_TOTAL_ENTRY","Jumlah API Call",["date"]),
            "overweight": Counter("BMI_SERVER_OVERWEIGHT_COUNT","Data Jumlah Entry yang Overweight",["value","timestamp"] ),
            "underweight": Counter("BMI_SERVER_UNDERWEIGHT_COUNT","Data Jumlah Entry yang Underweight",["value","timestamp"] ),
            "healthy": Counter("BMI_SERVER_HEALTHY_COUNT","Data Jumlah Entry yang Underweight",["value","timestamp"] )
}
app = Blueprint('transfer', __name__,url_prefix="/")


@app.route("/",methods=["GET"])
def calculate_bmi():
    start_date = datetime.now()
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

    result = BMICalculator(**data).calculate().check()
    
    end_date = datetime.now()
    
    delta = (end_date - start_date).microseconds
    
    metrics["process_time"].set(delta)

    metrics["recent_input_bmi"].labels(result["bmi"],end_date).set(result["bmi"])

    metrics["total_entries"].labels(end_date.strftime("%Y-%m-%d")).inc()

    metrics[result["label"]].labels(result["bmi"],end_date.strftime("%Y-%m-%d")).inc()

    return result,200
