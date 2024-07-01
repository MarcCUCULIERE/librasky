# LIBRASKY

LIBRASKY est une application conçue pour gérer une collection de spiritueux, permettant aux utilisateurs de suivre et de mettre à jour leur collection en temps réel. Elle offre des fonctionnalités telles que l'ajout, la mise à jour, la suppression et la recherche d'articles dans la collection.

## Fonctionnalités

- **Ajout de nouveaux articles** : Permet aux utilisateurs d'ajouter de nouveaux spiritueux à leur collection.
- **Mise à jour des articles existants** : Les utilisateurs peuvent mettre à jour les détails des spiritueux déjà présents dans leur collection.
- **Suppression d'articles** : Offre la possibilité de supprimer des spiritueux de la collection.
- **Recherche d'articles** : Les utilisateurs peuvent rechercher des spiritueux spécifiques dans leur collection en utilisant différents critères.

## Technologies Utilisées

- **Backend** : Python avec Flask pour le serveur API.
- **Base de données** : SQL Server pour le stockage des données.
- **Frontend** : (Si applicable, ajouter des technologies frontend).

## Installation

Pour installer et exécuter LIBRASKY localement, suivez ces étapes :

1. **Cloner le dépôt** :
 
 git clone https://github.com/MarcCUCULIERE/librasky

2. **Installer les dépendances** :

pip install -r requirements.txt

3. **Configurer la base de données** :
- Assurez-vous que SQL Server est installé et en cours d'exécution.
- Créez une base de données nommée `LIBRASKY`.
- Exécutez les scripts SQL fournis pour initialiser la base de données.

4. **Lancer l'application** :

python main.py

## Utilisation

Après avoir lancé l'application, elle sera accessible via `http://localhost:5000`. Vous pouvez utiliser des outils comme Postman ou cURL pour interagir avec l'API.

### Exemples de requêtes

- **Ajouter un nouvel article** :

POST /add { "Nom": "Spectacular", "Distillerie": "Ardbeg", ... }

- **Mettre à jour un article** :

PUT /update { "Nom": "Spectacular", "Quantite": 3, ... }

- **Supprimer un article** :

DELETE /delete { "Nom": "Spectacular", ... }

## Contribution

Les contributions sont les bienvenues. Pour contribuer, veuillez forker le dépôt, créer une branche pour votre fonctionnalité, puis soumettre une pull request.

## Licence

C'est pas encore bien defini mais ca sera open source.

---

Pour plus d'informations, veuillez consulter la documentation officielle ou contacter lesdéveloppeur.