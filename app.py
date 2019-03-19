from flask import Flask, render_template
from mongoengine import *
app = Flask(__name__)
connect('DB_NAME')

class User(Document):
    email = StringField()
    first_name = StringField()
    last_name = StringField()

Chas = User(first_name='Chas', last_name='McCammon', email='Example@')
Chas.save()

class Country(Document):
    name = StringField()

NZ = Country(name='New Zealand')
NZ.save()

for u in User.objects:
    print(u.first_name, u.last_name, u.email)

for countries in Country.objects:
    print(countries.name)


@app.route('/')
def index():
    myName = "Chas"
    return render_template('index.html', name=myName)

@app.route('/inspiration')
def inspirations():
    myName = "Chas"
    return render_template('inspirations.html', name=myName)

@app.route('/countries/', methods=['GET'])
@app.route('/countries/<country_id>', methods=['GET'])
def getCountries(country_id=None):
    country = None
    if country_id is None:
        country = Country.objects
    else:
        country = Country.objects.get(id=country_id)
    return country.to_json()

@app.route('/deleteCountry/<country_id>', methods=['DELETE'])
def deleteCountries():
    Country.objects.delete(id=country_id)
    return render_template('index.html')



if __name__ =="__main__":
    app.run(debug=True,port=8080)