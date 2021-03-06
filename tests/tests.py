import sys, os, time, signal

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from module.calculator import BMICalculator

import subprocess
import requests

class TestBMIApp():
    def test_bmi_basic_function(self,bmi_parameters):
        
        tests = bmi_parameters
        print(tests)
        for test in tests:
            metric = test["metrics"]
            expected = test["result"]
            result = BMICalculator(*metric).calculate().check()

            assert result["label"] == expected["label"]
            assert result["bmi"] == expected["bmi"]
    def test_api_basic_function(self,bmi_api_setup):
        
        api_address_pair = bmi_api_setup
        process = subprocess.Popen(["python3","main.py"],cwd="../")
        print("Waiting for grace period to be over")
        time.sleep(5)
        print("App is running")
        assert requests.get("http://{}:{}/?weight=asd&height=170".format(*api_address_pair),timeout=10).status_code == 400 # validation bypass test
        assert requests.get("http://{}:{}/?".format(*api_address_pair),timeout=10).status_code == 400 # empty query test
        
        assert requests.get("http://{}:{}/?weight=90&height=170".format(*api_address_pair),timeout=10).status_code == 200 # normal request test
        assert requests.get("http://{}:{}/?weight=90&height=170".format(*api_address_pair),timeout=10).status_code == 200 # cached request test
        os.kill(process.pid,signal.SIGTERM)
        print("Waiting for grace period to be over")
        time.sleep(5)
        

    def test_available_api(self,bmi_existing_api_setup):
        """ 
        Test an existing deployment of the API
        """
        api_address = bmi_existing_api_setup
        print(api_address)
        assert requests.get("{}/?weight=asd&height=170".format(api_address),timeout=10).status_code == 400 # validation bypass test
        assert requests.get("{}/?".format(api_address),timeout=10).status_code == 400 # empty query test
        assert requests.get("{}/?weight=90&height=170".format(api_address),timeout=10).status_code == 200 # normal request test
        assert requests.get("{}/?weight=90&height=170".format(api_address),timeout=10).status_code == 200 # cached request test
        pass

