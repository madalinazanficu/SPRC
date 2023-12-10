from flask import Flask, request
from pymongo import MongoClient
import mongoengine
from mongoengine import connect
from db_entities import Tari, Orase
import json


# Request codes:
#     200 - OK
#     201 - Created
#     400 - Bad Request
#     404 - Not Found
#     409 - Conflict - NonUniqueError

def connect_to_database():
    try:
        client = MongoClient(host = 'mongo',
                             port = 27017,
                             username = 'admin',
                             password = 'admin',
                             authSource = 'admin')
    
        db = client['mongo']
        
        connect(
            db = 'mongo',
            host = 'mongo',
            username = 'admin',
            password = 'admin',
            authentication_source = 'admin'
        )
        return db
    
    except:
        print("Error connecting to database!")
        return None
    

# ------------- Definire aplicatie Flask
app = Flask(__name__)



# ------------ Autentificare la baza de date
database_connection = connect_to_database()
if database_connection is None:
    print("Exiting...")
    exit(1)
else:
    print("Connected to database!")
    
    
    
def check_payload_country(payload):
    if 'nume' not in payload or 'lat' not in payload or 'lon' not in payload:
        return False
    
    if (
        type(payload['nume']) != str or
        type(payload['lon']) == str or
        type(payload['lat']) == str or
        type(payload['lon']) == None or
        type(payload['lat']) == None
    ):
        return False
    return True


def check_payload_city(payload):
    if (
        'nume' not in payload or 
        'lat' not in payload or
        'lon' not in payload or
        'idTara' not in payload
    ):
        return False
    
    if (
        type(payload['nume']) != str or
        type(payload['lon']) == str or
        type(payload['lat']) == str or
        type(payload['lon']) == None or
        type(payload['lat']) == None
    ):
        return False
    return True


# ------------- Rute country
@app.route('/api/countries', methods = ['POST'])
def post_country():
    try:
        payload = request.get_json()
        # JSON-ul nu contine datele necesare
        if check_payload_country(payload) is False:
            return '', 400
        
        tara = Tari(nume_tara = payload['nume'],
                    latitudine = payload['lat'],
                    longitudine = payload['lon'])
        
        try:
            tara.save()
            id = tara.pk.__str__()
            response = {
                "id": id
            }
            return json.dumps(response), 201   
          
        except mongoengine.errors.NotUniqueError as e:
            return '', 409
    
    except:
        return '', 400


@app.route('/api/countries', methods = ['GET'])
def get_countries():
    
    try:
        tari = Tari.objects
        response = []
        for tara in tari:
            response.append(
                {
                    "id": tara.pk.__str__(),
                    "nume": tara.nume_tara,
                    "lat": tara.latitudine,
                    "lon": tara.longitudine
                }
            )
        return json.dumps(response), 200
    
    except mongoengine.errors.ValidationError as e:
        return '', 400


@app.route('/api/countries/<id>', methods = ['DELETE'])
def delete_country(id):
    try:
        try: 
            tara = Tari.objects(pk = id).get()
        except:
            return '', 404
        
        tara.delete()
        response = {
            "id": tara.pk.__str__()
        }
        return json.dumps(response), 200
    
    except:
        return '', 400
    
    
@app.route('/api/countries/<id>', methods = ['PUT'])
def put_country(id):
    try:
        payload = request.get_json()
        # JSON-ul nu contine datele necesare / corecte
        if check_payload_country(payload) is False:
            return '', 400
        
        try:
            tara = Tari.objects(pk = id).get()
            tara.nume_tara = payload['nume']
            tara.latitudine = payload['lat']
            tara.longitudine = payload['lon']
            tara.save()
            response = {
                "id": tara.pk.__str__()
            }
            return json.dumps(response), 200
        
        # Eroare, nu s-a gasit tara cu id-ul respectiv
        except mongoengine.errors.ValidationError as e:
            return '', 404
    
    except:
        return '', 400
    
    
    
    
    
    
# ------------- Rute city
@app.route('/api/cities', methods = ['POST'])
def post_city():
    try:        
        payload = request.get_json()
        
        # JSON-ul nu contine datele necesare
        if check_payload_city(payload) is False:
            return json.dumps(payload), 400
        
        # Verificam daca exista tara cu id-ul respectiv
        try:
            tara = Tari.objects(pk = payload['idTara']).get()
        except:
            return '', 404
        
        oras = Orase(nume_oras = payload['nume'],
                        latitudine = payload['lat'],
                        longitudine = payload['lon'],
                        id_tara = tara)
        
        try:
            oras.save()
            id = oras.pk.__str__()
            response = {
                "id": id
            }
            return json.dumps(response), 201
        
        # Perechea (nume_oras, id_tara) nu este unica             
        except mongoengine.errors.NotUniqueError as e:
            return '', 409
        
    except:
        return '', 400
        


@app.route('/api/cities', methods = ['GET'])
def get_cities():
    try:
        orase = Orase.objects
        response = []
        for oras in orase:
            response.append(
                {
                    "id": oras.pk.__str__(),
                    "nume": oras.nume_oras,
                    "lat": oras.latitudine,
                    "lon": oras.longitudine,
                    "idTara": oras.id_tara.pk.__str__()
                }
            )
        return json.dumps(response), 200
    
    except mongoengine.errors.ValidationError as e:
        return '', 400
    

@app.route('/api/cities/country/<idTara>', methods = ['GET'])
def get_city(idTara):
    try:
        tara = Tari.objects(pk = idTara).get()
        orase = Orase.objects(id_tara = tara.pk)
        
        for oras in orase:
            response = {
                "id": oras.pk.__str__(),
                "nume": oras.nume_oras,
                "lat": oras.latitudine,
                "lon": oras.longitudine,
                "idTara": oras.id_tara.pk.__str__()
            }
        return json.dumps(response), 200
    except:
        return '', 400
    
    
@app.route('/api/cities/<id>', methods = ['PUT'])
def put_city(id):

    payload = request.get_json()
    
    # JSON-ul nu contine datele necesare / corecte
    if check_payload_city(payload) is False or 'id' not in payload:
        return json.dumps(payload), 400

    try:
        tara = Tari.objects(pk = payload['idTara']).get()
    except:
        return '', 404

    try:
        oras = Orase.objects(pk = id).get()
        oras.nume_oras = payload['nume']
        oras.latitudine = payload['lat']
        oras.longitudine = payload['lon']
        oras.id_tara = tara
        
        try:
            oras.save()
            response = {
                "id": oras.pk.__str__()
            }
            return json.dumps(response), 200
        
        except mongoengine.errors.NotUniqueError as e:
            return '', 409
    
    # Eroare, nu s-a gasit oras cu id-ul respectiv
    except mongoengine.errors.ValidationError as e:
        return '', 404

    

@app.route('/api/cities/<id>', methods = ['DELETE'])
def delete_city(id):
    try:
        # Verificam daca exista oras cu id-ul respectiv
        try: 
            oras = Orase.objects(pk = id).get()
        except:
            return '', 404
        
        oras.delete()
        response = {
            "id": oras.pk.__str__()
        }
        return json.dumps(response), 200
    
    # Eroare, nu s-a putut sterge orasul
    except:
        return '', 400


# ------------- Definire rute
@app.route('/')
def hello_world():
    
    tara = Tari(nume_tara = "dadada", latitudine = 45.9432, longitudine = 24.9668)
    try:
        tara.save()
        return "Inserted into database!" + str(tara.nume_tara)
    
    except mongoengine.errors.ValidationError as e:
        return "Error Validation Error!"

    except mongoengine.errors.NotUniqueError as e:
        return "Error Not Unique Error!"
    
    # try:
    #     database_connection['test_collection'].insert_one({"name": "test"})
    #     return "Inserted into database!"
    # except:
    #     return "Error inserting into database!"





if __name__ == '__main__':
    app.run('0.0.0.0', port=6000, debug=True)
