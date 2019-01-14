import json

def read():    
    with open('config.json') as json_file:  
        return json.load(json_file)

