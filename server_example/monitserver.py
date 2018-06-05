import falcon
import json

class DataStatusResource:
    def on_get(self, req, resp):
        
        data = {
            "chart1_list": [0, 0, 0],
            "chart2_list": [0, 0, 0],
            "chart3_list": [0, 0, 0],
            "data1_label": "Label 1",
            "data2_label": "Label 2",
            "data3_label": "Label 3",
            "data4_label": "Label 4",
            "data5_label": "Label 5",
            "data6_label": "Label 6",
            "data1": 0,
            "data2": 0,
            "data3": 0,
            "data4": 0,
            "data5": 0,
            "data6": "Ok",
        }
        if data:
            resp.body = json.dumps({"status": 200, "data": data})
        else:
            resp.body = json.dumps({"status": 404})

api = falcon.API()
api.add_route('/data_status', DataStatusResource())
