#!/usr/bin/python
import re, json
from bson import json_util
from pymongo import MongoClient
from bottle import route, run, request, response, abort, get, post

# Define connection, db and collection to work with
connection = MongoClient('localhost', 27017)
db = connection.aviation
collection = db.airports
  
# Get Airport ICAO
@get('/aviation/findAirport/icao')
def form_icao():
  return '''<h2>Search for Airport ICAO identifier</h2>
              <form method="POST" action="/aviation/findAirport/icao">
                ICAO: <input name="ICAO" type="text" /><br/>
                <input type="submit" />
              </form>'''

# Find airport given ICAO
@post('/aviation/findAirport/icao')
def get_icao():
    
    # Get ticker symbols from forms
    icao = request.forms.get('ICAO')
    
    # Create list out of ticker symbols
    #tickerList = [stock1, stock2, stock3]
    
    # Find documents for all ticker symbols, project only a few desired fields, and convert to list object for easier return
    result = list(collection.find({ 'ICAO' : icao}, {'_id': 0, 'Name': 1, 'City': 1, 'Country': 1}))
    
    # If list is empty return message
    if not result:
      abort(404, "No airport found with the following ICAO symbol : " + icao )
      return
    
    # Return json version of list object
    response.content_type='application/json'
    return json.dumps(result, indent=4, default=json_util.default, sort_keys=1)

# Get airport city
@get('/aviation/findAirport/city')
def form_city():
  return '''<h2>Search for Airport by city</h2>
              <form method="POST" action="/aviation/findAirport/city">
                city: <input name="city" type="text" /><br/>
                <input type="submit" />
              </form>'''

# Find airport given city
@post('/aviation/findAirport/city')
def get_city():
    
    # Get ticker symbols from forms
    city = request.forms.get('city')
    
    # Create list out of ticker symbols
    #tickerList = [stock1, stock2, stock3]
    
    # Find documents for all ticker symbols, project only a few desired fields, and convert to list object for easier return
    result = list(collection.find({ 'City' : city}, {'_id': 0, 'ICAO': 1, 'Name': 1, 'City': 1, 'Country': 1}))
    
    # If list is empty return message
    if not result:
      abort(404, "No airport was found at the following city : " + city )
      return
    
    # Return json version of list object
    response.content_type='application/json'
    return json.dumps(result, indent=4, default=json_util.default, sort_keys=1)

# Main
if __name__ == '__main__': #declare instance of request
    #app.run(debug=True)
    run(host='127.0.0.1', port=8080)