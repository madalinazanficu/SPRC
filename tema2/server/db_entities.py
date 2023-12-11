import mongoengine
from mongoengine import Document, StringField, IntField, FloatField, ReferenceField, CASCADE, DateTimeField

class Tari(Document):
    nume_tara = StringField(required=True, unique=True)
    latitudine = FloatField(required=True)
    longitudine = FloatField(required=True)


class Orase(Document):
    id_tara = ReferenceField(Tari, required=True, reverse_delete_rule=CASCADE)
    nume_oras = StringField(required=True)
    latitudine = FloatField(required=True)
    longitudine = FloatField(required=True)
    
    meta = {
        'indexes': [{'fields': ['id_tara', 'nume_oras'], 'unique': True}]
    }

class Temperaturi(Document):
    id_oras = ReferenceField(Orase, required=True, reverse_delete_rule=CASCADE)
    valoare = FloatField(required=True)
    timestamp = DateTimeField(required=True)
    
    meta = {
        'indexes': [{'fields': ['id_oras', 'timestamp'], 'unique': True}]
    }