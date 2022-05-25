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
    SERVICE_HOST = os.getenv("SERVICE_HOST")
    SERVICE_PORT = os.getenv("SERVICE_PORT")
    MEMCACHE_HOST = os.getenv("MEMCACHE_HOST")
    MEMCACHE_PORT = os.getenv("MEMCACHE_PORT")
    if not SERVICE_HOST:
       SERVICE_HOST = "0.0.0.0"
    if not SERVICE_PORT:
       SERVICE_PORT = "9095"
    if not MEMCACHE_HOST:
       MEMCACHE_HOST = "memcache"
    if not MEMCACHE_PORT:
       MEMCACHE_PORT = "11211"

    print("Preparing sample environment")
    with open("../.env",mode="w") as envfile:
        to_write =[
            "SERVICE_HOST={}".format(SERVICE_HOST),
            "SERVICE_PORT={}".format(SERVICE_PORT),
            "MEMCACHE_HOST={}".format(MEMCACHE_HOST),
            "MEMCACHE_PORT={}".format(MEMCACHE_PORT)
        ]
        for items in to_write:
            envfile.writelines(items+"\n")
    os.mkdir("log")
    yield SERVICE_HOST,SERVICE_PORT
    os.rmdir("log")
@pytest.fixture(scope="class")
def bmi_existing_api_setup():
    address_list = [
      "http://0.0.0.0:9095",
      "https://bmi.raytsan.me"
    ]

    for data in address_list:
        yield data
