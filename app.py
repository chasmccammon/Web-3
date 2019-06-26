from flask import Flask, render_template
from mongoengine import *
import os
import csv
import json
import csv
app = Flask(__name__)
app.config.from_object('config')
connect('DB_NAME_3')
# Create a new class called country to hold or read in CSV values
class Country(Document):
    countryid = StringField()
    name = StringField()
    data = DictField()

# API route used to test adding hard coded values to country classes
@app.route('/addcountry')
def addcountry():
    NZ = Country(countryid='1',name='New_Zealand')
    NZ.save()
    AUS = Country(countryid='2',name='Australia')
    AUS.save()
    USA = Country(countryid='3',name='America')
    USA.save()
    return render_template('index.html',name=myName),200

# Set home API route to the index page
@app.route('/')
def index():
    myName = "Chas"
    return render_template('index.html',name=myName),200

# set route to inspiration page
@app.route('/inspiration')
def inspirations():
    myName = "Chas"
    return render_template('inspirations.html', name=myName),200

# API routes used to get data from our countries in the database with a specific country or returns all
@app.route('/countries/', methods=['GET'])
@app.route('/countries/<country_id>', methods=['GET'])
def getCountries(country_id=None):
    country = None
    if country_id is None:
        country = Country.objects
    else:
        country = Country.objects.get(name=country_id)

    country = country.to_json()
    parsed_country = json.loads(country)
    return country 
# API route used to remove a specific country
@app.route('/deleteCountry/<country_id>', methods=['DELETE'])
def deleteCountries():
    Country.objects.delete(id=country_id)
    return render_template('index.html'),200
# API route used to read in CSV values from our files in the ./files folder
@app.route('/ReadCSV')
def readCSV():
      returnstring = ""
      for file in os.listdir(app.config['FILES_FOLDER']):
          filename = os.fsdecode(file)
          path = os.path.join(app.config['FILES_FOLDER'],filename)
          f = open(path)
          r = csv.DictReader(f)
          d = list(r)
          linecount = 1
          #read through each file and map a key and value pair for the dictionary object in country class
          for data in d:
            dictionary = {
            "1985":data["1985"],
            "1986":data["1986"],
            "1987":data["1987"],
            "1988":data["1988"],
            "1989":data["1989"],
            "1990":data["1990"],
            "1991":data["1991"],
            "1992":data["1992"],
            "1993":data["1993"],
            "1994":data["1994"],
            "1995":data["1995"],
            "1996":data["1996"],
            "1997":data["1997"],
            "1998":data["1998"],
            "1999":data["1999"],
            "2000":data["2000"],
            "2001":data["2001"],
            "2002":data["2002"],
            "2003":data["2003"],
            "2004":data["2004"],
            "2005":data["2005"],
            "2006":data["2006"],
            "2007":data["2007"],
            "2008":data["2008"],
            "2009":data["2009"],
            "2010":data["2010"],
            "2011":data["2011"],
            "2012":data["2012"],
            "2013":data["2013"],

            }
           #Create country using read in CSV data and save to database
            data["country"] = Country(countryid=str(linecount), name=str(data["country"]),data=dictionary) 
            data["country"].save()        
            linecount += 1 
          return("Countries added to database")
app.run(debug=True, host='0.0.0.0',port=80)
