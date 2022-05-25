

import json
from pymemcache.client import base

class MemcacheBMIClient():
    def __init__(self,HOST,PORT) -> None:
        """
        Basic memcache client for BMI result storing
        """
        self.client = base.Client((HOST,PORT))
    def cache_or_store(self,height,weight):
        """
        Check if the weight and height data has been calculated before,
        Returns 'None' if it hasn't, returns the json body if it has.

        """
        cached = self.client.get("{}/{}".format(height,weight))
        result = None
        if cached:
            result = cached.decode()
        return result
    def store(self,height,weight,result):
        """
        Store calculation label and bmi inside memcache key
        key format == > height/weight
        """
        self.client.set("{}/{}".format(height,weight),json.dumps(result))

    
