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

<img width="1673" height="1400" alt="Diagramme Archi" src="https://github.com/user-attachments/assets/f02b23c0-b9c8-4971-8a4d-99386a4a055b" />

### Notes
 * L'accès aux endpoints ne marchera qu après un login réussi. Seule la création d'un usager n'est pas protégée par un token.
 * Les codes matières affichés dans les listes sont connus dans le champ sémantique pédagogique des usagers concernés, c'est pourquoi ils sont affichés sans détours pour
 plus de praticité


### Documentation yml
 * Accessible via Swagger au endpoint http://127.0.0.1:5600/apidocs/
 * On peut y accéder en contrepassant les protocoles d'authentification jwt, 
		mais pour tester certaines méthodes il faut aller chercher son token. Pour cela, cliquer sur Authorize dans la methode
		swagger concernée, le lien pour avoir le token est fourni.
