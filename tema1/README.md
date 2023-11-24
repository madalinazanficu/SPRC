### Tema1 - SPRC
### Zanficu Madalina 343C1

### Observatii:
1. Am modificat oauth_svc.c pentru a putea prelua parametrii din 
linia de comanda pentru fisiele de in ale serverului. 
Astfel am apelat functia command_line_arguments_support.

2. Pentru procedesul de refresh, am descis sa mai adaug o procedura
aditionala in interfata: refresh_access_token care este apelata din
client inainte de apelarea procedurii validate_delegated_action.

### Structuri de date:
In server:
1. Pentru gestionarea bazei de date m-am folosit de map-uri,
avand un map pentru useri, un map pentru resurse, si un map pentru
approvals (populate la citirea fisierelor de intrare pentru server).

De asemenea am mai adaugat si map-uri pentru tokenii de access,
tokenii de refresh si pentru valabilitatea token-ului.

In client:
Deoarece unele apeluri catre server trebuie sa trimita acestuia ca parametru
si tokeii (access/refresh), i-am retinut si in partea de client.
Nu consider ca era neaparat necesar, pentru ca in partea de server 
pe baza client_id, se pot gasi tokenii asociati.

### Workflow:
Am respectat modelul OAuth prin ordinea apelarii procesurilor.
Am respectat indicatiile legate de regenerarea tokenului de access,
ca client-ul sa initieze acest procedeu inainte de accesarea resurselor.
Am respectat ca in structura token-ului sa nu existe id-ul utilizatorlui.