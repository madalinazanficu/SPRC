from flask import Flask, request
from pymongo import MongoClient
import mongoengine
from mongoengine import connect
from db_entities import Tari, Orase, Temperaturi
import json
from datetime import datetime
from mongoengine.queryset.visitor import Q


# Request codes:
#     200 - OK
#     201 - Created
#     400 - Bad Request
#     404 - Not Found
#     409 - Conflict - NonUniqueError
#     docker system prune -a --volumes  

def connect_to_database():
    try:
        client = MongoClient(host='mongo',
                             port=27017,
                             username='admin',
                             password='admin',
                             authSource='admin')

        db = client['mongo']

        connect(
            db='mongo',
            host='mongo',
            username='admin',
            password='admin',
            authentication_source='admin'
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
@app.route('/api/countries', methods=['POST'])
def post_country():
    try:
        payload = request.get_json()
        # JSON-ul nu contine datele necesare
        if check_payload_country(payload) is False:
            return '', 400

        tara = Tari(nume_tara=payload['nume'],
                    latitudine=payload['lat'],
                    longitudine=payload['lon'])

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


@app.route('/api/countries', methods=['GET'])
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


@app.route('/api/countries/<id>', methods=['DELETE'])
def delete_country(id):
    try:
        try:
            tara = Tari.objects(pk=id).get()
        except:
            return '', 404

        tara.delete()
        response = {
            "id": tara.pk.__str__()
        }
        return json.dumps(response), 200

    except:
        return '', 400


@app.route('/api/countries/<id>', methods=['PUT'])
def put_country(id):
    try:
        payload = request.get_json()
        # JSON-ul nu contine datele necesare / corecte
        if check_payload_country(payload) is False:
            return '', 400

        try:
            tara = Tari.objects(pk=id).get()
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
@app.route('/api/cities', methods=['POST'])
def post_city():
    try:
        payload = request.get_json()

        # JSON-ul nu contine datele necesare
        if check_payload_city(payload) is False:
            return json.dumps(payload), 400

        # Verificam daca exista tara cu id-ul respectiv
        try:
            tara = Tari.objects(pk=payload['idTara']).get()
        except:
            return '', 404

        oras = Orase(nume_oras=payload['nume'],
                     latitudine=payload['lat'],
                     longitudine=payload['lon'],
                     id_tara=tara)

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


@app.route('/api/cities', methods=['GET'])
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


@app.route('/api/cities/country/<idTara>', methods=['GET'])
def get_city(idTara):
    try:
        tara = Tari.objects(pk=idTara).get()
        orase = Orase.objects(id_tara=tara.pk)

        allResponses = []
        for oras in orase:
            response = {
                "id": oras.pk.__str__(),
                "idTara": oras.id_tara.pk.__str__(),
                "nume": oras.nume_oras,
                "lat": oras.latitudine,
                "lon": oras.longitudine,
            }
            allResponses.append(response)
        return json.dumps(allResponses), 200
    except:
        return '', 400


@app.route('/api/cities/<id>', methods=['PUT'])
def put_city(id):
    payload = request.get_json()

    # JSON-ul nu contine datele necesare / corecte
    if check_payload_city(payload) is False or 'id' not in payload:
        return json.dumps(payload), 400

    try:
        tara = Tari.objects(pk=payload['idTara']).get()
    except:
        return '', 404

    try:
        oras = Orase.objects(pk=id).get()
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


@app.route('/api/cities/<id>', methods=['DELETE'])
def delete_city(id):
    try:
        # Verificam daca exista oras cu id-ul respectiv
        try:
            oras = Orase.objects(pk=id).get()
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


# ------------- Rute temperature
@app.route('/api/temperatures', methods=['POST'])
def post_temperature():
    payload = request.get_json()

    if 'idOras' not in payload or 'valoare' not in payload:
        return '', 400

    if payload['valoare'] == None or type(payload['valoare']) == str:
        return '', 400

    try:
        oras = Orase.objects(pk=payload['idOras']).get()
    except:
        return '', 404

    timesstamp = datetime.now()
    temperatura = Temperaturi(id_oras=oras,
                              valoare=payload['valoare'],
                              timestamp=timesstamp)
    try:
        temperatura.save()
        id = temperatura.pk.__str__()
        response = {
            "id": id
        }
        return json.dumps(response), 201

    except mongoengine.errors.NotUniqueError as e:
        return '', 409


@app.route('/api/temperatures', methods=['GET'])
def get_temperatures():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    start_date = request.args.get('from')
    end_date = request.args.get('until')

    query = Q()
    if lat:
        lat = float(lat)
        orase = Orase.objects(latitudine=lat)
        query = query & Q(id_oras__in=orase)

    if lon:
        lon = float(lon)
        orase = Orase.objects(longitudine=lon)
        query = query & Q(id_oras__in=orase)

    if start_date:
        start_date = datetime.fromisoformat(start_date)
        query = query & Q(timestamp__gte=start_date)

    if end_date:
        end_date = datetime.fromisoformat(end_date)
        query = query & Q(timestamp__lte=end_date)

    temps = Temperaturi.objects(query)
    response = []
    for temp in temps:
        response.append(
            {
                "id": temp.pk.__str__(),
                "valoare": temp.valoare,
                "timestamp": str(temp.timestamp)
            }
        )

    return json.dumps(response), 200



@app.route('/api/temperatures/cities/<id_oras>', methods=['GET'])
def get_temperatures_city(id_oras):
    start_date = request.args.get('from')
    end_date = request.args.get('until')
    
    query = Q()
    orase = Orase.objects(pk=id_oras)
    query = query & Q(id_oras__in=orase)
    
    if start_date:
        start_date = datetime.fromisoformat(start_date)
        query = query & Q(timestamp__gte=start_date)
    
    if end_date:
        end_date = datetime.fromisoformat(end_date)
        query = query & Q(timestamp__lte=end_date)
        
    temps = Temperaturi.objects(query)
    response = []
    for temp in temps:
        response.append(
            {
                "id": temp.pk.__str__(),
                "valoare": temp.valoare,
                "timestamp": str(temp.timestamp)
            }
        )       
    return json.dumps(response), 200


@app.route('/api/temperatures/countries/<id_tara>', methods=['GET'])
def get_temperatures_country(id_tara):
    start_date = request.args.get('from')
    end_date = request.args.get('until')
    
    query = Q()
    tara = Tari.objects(pk=id_tara)
    orase = Orase.objects(id_tara__in=tara)
    query = query & Q(id_oras__in=orase)
    
    if start_date:
        start_date = datetime.fromisoformat(start_date)
        query = query & Q(timestamp__gte=start_date)
        
    if end_date:
        end_date = datetime.fromisoformat(end_date)
        query = query & Q(timestamp__lte=end_date)
        
    temps = Temperaturi.objects(query)
    response = []
    for temp in temps:
        response.append(
            {
                "id": temp.pk.__str__(),
                "valoare": temp.valoare,
                "timestamp": str(temp.timestamp)
            }
        )
    return json.dumps(response), 200


@app.route('/api/temperatures/<id>', methods=['PUT'])
def put_temperature(id):
    payload = request.get_json()
    if (
        'id' not in payload or
        'idOras' not in payload or
        'valoare' not in payload
    ):
        return '', 400
    
    if (
        type(payload['valoare']) == None or
        type(payload['valoare']) == str
    ):
        return '', 400
    
    try:
        temp = Temperaturi.objects(pk=id).get()
        oras = Orase.objects(pk=payload['idOras']).get()
    except:
        return '', 404
    
    
    try:
        temp.id_oras = oras
        temp.valoare = payload['valoare']
        temp.save()
        response = {
            "id": temp.pk.__str__()
        }
        return json.dumps(response), 200
    except mongoengine.errors.NotUniqueError as e:
        return '', 409
    

@app.route('/api/temperatures/<id>', methods=['DELETE'])
def delete_temperature(id):
    try:
        temp = Temperaturi.objects(pk=id).get()
    except:
        return '', 404
    
    try:
        temp.delete()
        response = {
            "id": temp.pk.__str__()
        }
        return json.dumps(response), 200
    except:
        return '', 400

# ------------- Definire rute
@app.route('/')
def view_temo():
    timestamp1 = datetime.now().__str__()
    time = datetime.fromisoformat(timestamp1)
    
    return "Hello World!" + str(time) + "\n" + str(timestamp1)

# def hello_world():
#     tara = Tari(nume_tara="dadada", latitudine=45.9432, longitudine=24.9668)
#     try:
#         tara.save()
#         return "Inserted into database!" + str(tara.nume_tara)

#     except mongoengine.errors.ValidationError as e:
#         return "Error Validation Error!"

#     except mongoengine.errors.NotUniqueError as e:
#         return "Error Not Unique Error!"


if __name__ == '__main__':
    app.run('0.0.0.0', port=6000, debug=True)