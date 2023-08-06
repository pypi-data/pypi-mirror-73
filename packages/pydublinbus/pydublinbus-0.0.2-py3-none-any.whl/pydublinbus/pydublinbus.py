"""
Dublin Bus RTPI REST API client
"""

from datetime import datetime, timedelta
import json
import requests

_RESOURCE = "https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation"

class DublinBusRTPI(object):
    def __init__(self, stopid=None):
        """
        A class used to interact with the Dublin Bus RTPI API
        
        :param stopid: Dublin bus stop id (default None).
        :type stopid: int

        """
        self.stopid = stopid

    def get_rtpi_data(self):
        """
        :returns: Return a json object containing Dublin Bus RTPI data
        :rype: dict
        """
        params = {
            "stopid": self.stopid,
            "format": "json"
        }
        
        try:
            response = requests.get(_RESOURCE, params, timeout=10)
        
        except (requests.ConnectionError,
                requests.RequestException,
                requests.HTTPError,
                requests.Timeout,
                requests.TooManyRedirects) as e:
            raise self.CONNError(str(e))
       
        try:
            results = json.loads(response.text)
            results = response.json()
        except ValueError:
            raise self.APIError('JSON parse failed.')
        
        if results["errorcode"] != "0":
            raise self.APIError(results["errormessage"])
        
        return results
    
    def bus_timetable(self):
        """   
        :return: List of the dictioneries of the due bus routes.
        :rtype: list
         
        eg:
         [{'due_in': '5', 'route': '67'},
         {'due_in': '12', 'route': '66B'},
         {'due_in': '13', 'route': '25A'},
         {'due_in': '21', 'route': '66'}]
        """
        timetable=[]
        result = self.get_rtpi_data()
        for item in result["results"]:
            duetime = item.get("duetime")
            route = item.get("route")
            bus_data = {
                "route": route,
                "due_in": duetime
            }
            timetable.append(bus_data)
        return timetable