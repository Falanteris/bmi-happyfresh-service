import os
import pytest
import shutil
@pytest.fixture(scope="class")
def bmi_parameters():
    """
    metrics ==> (weight,height)
    result ==> {
        'bmi':<bmi>
        'label':<healthy>
    }

    """
    test_cases = [
        {
            "metrics": (90,170),
            "result":{
                "bmi":31.1,
                "label":"overweight"
            }
        },
        {
            "metrics": (70,170),
            "result":{
                "bmi":24.2,
                "label":"healthy"
            }
        },
        {
            "metrics": (50,170),
            "result":{
                "bmi":17.3,
                "label":"underweight"
            }
        },
        
    ]
    return test_cases

@pytest.fixture(scope="class")
def bmi_api_setup():
    SERVICE_HOST = "0.0.0.0"
    SERVICE_PORT = "9095"

    print("Preparing sample environment")
    with open("../.env",mode="w") as envfile:
        to_write =[
            "SERVICE_HOST={}".format(SERVICE_HOST),
            "SERVICE_PORT={}".format(SERVICE_PORT)
        ]
        for items in to_write:
            envfile.writelines(items+"\n")

    return SERVICE_HOST,SERVICE_PORT