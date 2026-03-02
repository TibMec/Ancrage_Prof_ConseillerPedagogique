# Ancrage Prof - Conseiller pédagogique

Le but du service est de permettre aux enseignants fraichement arrivés de pouvoir obtenir l'aide pédagogique dont ils ont besoin au plus vite. 
Pour cela on a créé deux portails au sein d'un même client: 
  * Un portail enseignant permettant:
    1. La création d'un enseignant et son insertion dans la base de données Profs
    2. La modification de cet enseignant
    3. L'obtention d'une liste des conseillers pédagogiques en lien avec ses matières
    4. La consultation du programme ministériel en vigueur  ***- À VENIR -***
       
  * Un portail conseiller pédagogique permettant:
    1. La création d'un conseiller pédagogique et son insertion dans la base de données Conseillers
    2. La modification de ce conseiller
    3. L'obtention d'une liste des enseignants nouvellement inscrits
       
---

<img width="1673" height="1400" alt="Diagramme Archi" src="https://github.com/user-attachments/assets/f02b23c0-b9c8-4971-8a4d-99386a4a055b" />

---

### Notes
 * L'accès aux endpoints ne marchera qu après un login réussi. Seule la création d'un usager n'est pas protégée par un token.
 * Les codes matières affichés dans les listes sont connus dans le champ sémantique pédagogique des usagers concernés, c'est pourquoi ils sont affichés sans détours pour
 plus de praticité
* Les token sont accessibles actuellement pour une durée de 2h

---

### Documentation yml
 * Accessible via Swagger au endpoint http://127.0.0.1:5600/apidocs/
 * On peut y accéder en contrepassant les protocoles d'authentification jwt, 
		mais pour tester certaines méthodes il faut aller chercher son token. Pour cela, cliquer sur Authorize dans la methode
		swagger concernée, le lien pour avoir le token est fourni.

---

### Déploiement docker

***!! Terminal, à partir du dossier source (Projet_API_REST_Ancrage_Prof_CP) !!***
* Option 1) Pour builder et runner tous les conteners en une commande
  
Lancer le docker-compose:

`docker-compose up --build`

* Option 2) Pour tester les conteners individuellement, meilleur affichage d'erreurs
```
docker build -t dao:latest ./Service_DAO
docker build -t auth:latest ./Service_auth
docker build -t prof:latest ./ServiceProf
docker build -t conseiller:latest ./ServiceConseiller
docker build -t client:latest ./Client_Prof_CP
 ```


Puis ouvrir un terminal par service et lancer respectivement:

```
docker run -p 5600:5600 dao:latest
docker run -p 5100:5100 auth:latest
docker run -p 5700:5700 -e API_DAO=http://host.docker.internal:5600 prof:latest
docker run -p 5900:5900 -e API_DAO=http://host.docker.internal:5600 conseiller:latest
docker run -p 5000:5000 -e API_PROF=http://host.docker.internal:5700 -e API_CP=http://host.docker.internal:5900 -e API_AUTH=http://host.docker.internal:5100 client:latest
```



---

### Résultats

#### Doc swagger
* *3 API DÉCRITES*
<img width="1690" height="784" alt="image" src="https://github.com/user-attachments/assets/fb8590a6-c028-417a-be23-e8a48e186dd7" />


* *TEST DE L'API lierConseiller*
<img width="1431" height="910" alt="image" src="https://github.com/user-attachments/assets/b3b2b9f2-bb9a-4db7-bfc9-69ec9c9550f4" />


#### Test obtention token 
<img width="1919" height="240" alt="image" src="https://github.com/user-attachments/assets/b438ab7a-7f67-4d41-a466-c6c6dc2e7072" />


#### Endpoints
* *CHEMIN NOMINAL DE CRÉATION DE CONSEILLER*
  <img width="1512" height="580" alt="image" src="https://github.com/user-attachments/assets/f4028a62-2871-4d67-8bf5-4f111ad931b0" />
          --------------------------------------------------------------------------------------------------------------                  
  <img width="1142" height="822" alt="image" src="https://github.com/user-attachments/assets/822567d2-7790-4ab9-ad17-1b803246d149" />
         --------------------------------------------------------------------------------------------------------------                  
                        
  <img width="1090" height="814" alt="image" src="https://github.com/user-attachments/assets/8054d2f7-c176-4339-9e11-91350d819774" />
        --------------------------------------------------------------------------------------------------------------                  
                     
  <img width="1163" height="887" alt="image" src="https://github.com/user-attachments/assets/24d498ce-ffbc-4376-b664-1d28c1bbde6f" />
        --------------------------------------------------------------------------------------------------------------                  
                 
  <img width="1608" height="648" alt="image" src="https://github.com/user-attachments/assets/ef7bafb6-95d6-4da6-9f95-d1ca050b0b9a" />

* *LOGIN*

<img width="1222" height="502" alt="image" src="https://github.com/user-attachments/assets/87b63ece-ec88-4863-9992-e412159a66f6" />

      --------------------------------------------------------------------------------------------------------------

<img width="1031" height="837" alt="image" src="https://github.com/user-attachments/assets/ef35f804-d78a-409e-9acf-43c163b6f00a" />

					
* *LISTE PROFS*
  
  <img width="1849" height="933" alt="image" src="https://github.com/user-attachments/assets/7bb9b0ef-b8db-4d70-ba5b-7308a342b7bb" />
  

* *CONSEILLERS AFFILIÉS*

<img width="1571" height="654" alt="image" src="https://github.com/user-attachments/assets/6b2e4096-4755-4543-af87-364f08ff0e4c" />

---

#### Déploiement
<img width="1208" height="998" alt="image" src="https://github.com/user-attachments/assets/0be65e77-156f-494e-a62e-7ba05b0ce512" />

---

### Conclusion
**Non fonctionnel - perspectives d'amélioration:**
* Delete pas fini d'être implémenté sur client (prof et conseiller)
* Update pas fini d'être implémenté sur client prof
* Update = préremplissage automatique
* Pages d'erreur
* Meilleur affichage des messages flash
* UI-UX plus cohérent (chemins nominaux, code couleur, design consistant)
* Affichages de session quand utilisateur connecté (nom, prénom)


*À venir*
* tri par date de creation
* encryptage du password
* routes https
* envoi de courriel aux conseillers concernés lorsqu'un enseignant vient de s'inscrire,avec les infos du prof
