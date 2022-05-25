import os,json
from datetime import datetime
from flask import  request, Blueprint
from schema import BMISchema
from module.calculator import BMICalculator
from prometheus_client import Gauge,Counter
from memcache import MemcacheBMIClient
from logger.LogFormatClass import LogFormatClass

log = LogFormatClass()


metrics = {
            "process_time": Gauge("BMI_SERVER_PROCESS_TIME",documentation="Waktu pemrosesan BMI dalam microsecods"),
            "recent_input_bmi": Gauge("BMI_SERVER_RECENTLY_INPUTTED","Data BMI terbaru",["value","timestamp"] ),
            "total_entries": Counter("BMI_SERVER_TOTAL_ENTRY","Jumlah API Call",["date"]),
            "overweight": Counter("BMI_SERVER_OVERWEIGHT_COUNT","Data Jumlah Entry yang Overweight",["value","timestamp"] ),
            "underweight": Counter("BMI_SERVER_UNDERWEIGHT_COUNT","Data Jumlah Entry yang Underweight",["value","timestamp"] ),
            "healthy": Counter("BMI_SERVER_HEALTHY_COUNT","Data Jumlah Entry yang Underweight",["value","timestamp"] ),
            "bmi":Counter("BMI_RESULT_DATA","Label BMI",["label"]),
            "result_bmi":Counter("BMI_RESULT_METRIC","Hasil Perhitungan BMI",["value"])
            
}
app = Blueprint('transfer', __name__,url_prefix="/")

def metrics_insert_method(result,end_date,delta):
    
    metrics["process_time"].set(delta)

    metrics["recent_input_bmi"].labels(result["bmi"],end_date).set(result["bmi"])

    metrics["total_entries"].labels(end_date.strftime("%Y-%m-%d")).inc()

    metrics[result["label"]].labels(result["bmi"],end_date.strftime("%Y-%m-%d")).inc()

    metrics["bmi"].labels(result["label"]).inc()

    metrics["result_bmi"].labels(result["bmi"]).inc()


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
    try:
        MEMCACHE_HOST = os.getenv("MEMCACHE_HOST")
        MEMCACHE_PORT = int(os.getenv("MEMCACHE_PORT"))
        cache = MemcacheBMIClient(MEMCACHE_HOST,MEMCACHE_PORT)
        result = cache.cache_or_store(**data)
        print("obtained")
        print(result)
        print("======")
        if result != None:
            print("Result cached")

            result = json.loads(result)

            print("data")

            print(result)

            print('+====')

            log.info("INFO :: Retrieved BMI from Cache ( Height : {} Weight : {} ==> {} {} )".format( data["height"],data["weight"],result["bmi"],result["label"] ))

            end_date = datetime.now()

            delta = (end_date - start_date).microseconds

            metrics_insert_method(result,end_date,delta)

            return result, 200 
    except ConnectionRefusedError as ce:
        log.error("ERROR :: cannot connect to MEMCACHE calculating normally instead")
    # except ValueError as ve:
    #     log.error("ERROR :: MEMCACHE environments seems to be misconfigured")
    result = BMICalculator(**data).calculate().check()
    
    end_date = datetime.now()
    
    delta = (end_date - start_date).microseconds

    metrics_insert_method(result,end_date,delta)

    log.info("INFO :: Calculated BMI ( Height : {} Weight : {} ==> {} {} )".format( data["height"],data["weight"],result["bmi"],result["label"] ))

    try:
        MEMCACHE_HOST = os.getenv("MEMCACHE_HOST")
        MEMCACHE_PORT = int(os.getenv("MEMCACHE_PORT"))
        cache = MemcacheBMIClient(MEMCACHE_HOST,MEMCACHE_PORT)
        
        cache.store(
            height=data["height"],
            weight=data["weight"],
            result=result
        )
    except ConnectionRefusedError as ce:
        log.error("ERROR :: cannot connect to MEMCACHE, data is not cached ( Height : {} Weight : {} ==> {} {} )".format( data["height"],data["weight"],result["bmi"],result["label"]))
    except ValueError as ve:
        log.error("ERROR :: MEMCACHE environments seems to be misconfigured")

    return result, 200
