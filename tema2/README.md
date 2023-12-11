## Zanficu Madalina 343 C1 - Tema 2

1. Baza de date:
- pentru baza de date am optat sa folosesc MongoDB
- am pastrat campul _id autogenerat la crearea unui obiect (string)
2. Pentru api, am folosit flask si python
3. Interfata grafica folosita este Mongo Express

Rulare:

Containere active: sudo  docker ps 
Containere: sudo docker ps -active

Rulare fisier docker (izolat):
1. Build: sudo docker build -t my-flask-app -f server/Dockerfile .
2. Run:  sudo docker run -p 6000:6000 my-flask-app

Rulare docker compose:
1. docker-compose -f ./docker-compose.yml up --build
2. docker-compose -f ./docker-compose.yml down

Resurse:
1. Laborator 3 si 4 - SPRC
2. https://blog.tericcabrel.com/using-docker-and-docker-compose-with-nodejs-and-mongodb/