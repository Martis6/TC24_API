## TC24_API

Prediction API part of 2nd capstone project for Turing College. 

This Flask API (https://flask-tc24.herokuapp.com/) is able to use linear regression model to predict object price (specifically flat) based on given information about the flat such as neighborhood, area, year of built and etc. It also stores all inputs and predictions in postgresql database of Heroku.

### Usage

```
import json
import requests

requests.post("https://flask-tc24.herokuapp.com/predict", data=json.dumps(
    {
      "input":[
                  {
	                  	'neighborhood': 'Užupis', 
	                    'rooms': 2, 
	                    'area_m2': 50, 
	                    'floor': 3, 
	                    'max_floors': 3, 
	                    'year': 2020, 
	                    'build_material': 'brick', 
	                    'heating_type': 'central', 
	                    'condition': 'fully equipped'
                  }, 
              ]
    }
)).text

requests.get("https://flask-tc24.herokuapp.com/history").text
```

### License

API has a MIT-style license, as found in the [LICENSE](LICENSE) file.