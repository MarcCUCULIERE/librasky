import pyodbc
import youtils

def insert_data(quantite, nom, distillerie, annee, age, degres, date_achat, prix):
    try:
        conn = youtils.connect_to_sql_server()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Collection (Quantite, Nom, Distillerie, Année, Age, Degrés, Date_achat, Prix) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                   (quantite, nom, distillerie, annee, age, degres, date_achat, prix))
        conn.commit()
        print(f"Données insérées avec succès : {quantite}, {nom}, {distillerie}, {annee}, {age}, {degres}, {date_achat}, {prix}")
    except pyodbc.Error as e:
        print("Erreur lors de l'insertion des données:", str(e))
    finally:
        if conn:
            conn.close()


def list_data():
    conn = None
    try:
        conn = youtils.connect_to_sql_server()
        cursor = conn.cursor()
        cursor.execute("SELECT Quantite, Nom, Distillerie, Année, Age, Degrés, Date_achat, Prix FROM Collection")
        rows = cursor.fetchall()
        if rows:
            print("Liste des éléments dans la base de données :")
            for row in rows:
                print(f"Quantité: {row.Quantite}, Nom: {row.Nom}, Distillerie: {row.Distillerie}, Année: {row.Année}, Age: {row.Age}, Degrés: {row.Degrés}, Date d'achat: {row.Date_achat}, Prix: {row.Prix}")
                return rows
        else:
            print("Aucune donnée trouvée.")
    except pyodbc.Error as e:
        print("Erreur lors de la récupération des données:", str(e))
    finally:
        if conn:
            conn.close()

def update_data(nom, annee, degres, new_quantite, new_nom, new_distillerie, new_annee, new_age, new_degres, new_date_achat, new_prix):
    conn = None
    try:
        conn = youtils.connect_to_sql_server()
        cursor = conn.cursor()
        cursor.execute("UPDATE Collection SET Quantite = ?, Nom = ?, Distillerie = ?, Année = ?, Age = ?, Degrés = ?, Date_achat = ?, Prix = ? WHERE Nom = ? AND Année = ? AND Degrés = ?", 
                       (new_quantite, new_nom, new_distillerie, new_annee, new_age, new_degres, new_date_achat, new_prix, nom, annee, degres))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Données mises à jour avec succès : {new_nom}, {new_annee}, {new_degres}")
        else:
            print("Aucune donnée trouvée à mettre à jour.")
    except pyodbc.Error as l:
        print("Erreur lors de la mise à jour des données:", str(e))
    finally:
        if conn:
            conn.close()



def delete_data(nom, annee, degre):
    conn = None
    try:
        conn = youtils.connect_to_sql_server()
        cursor = conn.cursor()
        # Delete the data based on nom, annee, and degre
        cursor.execute("DELETE FROM Collection WHERE nom = ? AND annee = ? AND degre = ?", (nom, annee, degre))
        conn.commit()  # Commit the transaction
        if cursor.rowcount > 0:
            print(f"Data deleted successfully: {nom}, {annee}, {degre}")
        else:
            print("No data found to delete.")
    except pyodbc.Error as e:
        print("Error while deleting data:", str(e))
    finally:
        if conn:
            conn.close()


def delete_row(server, database, username, password, table_name, condition):
    """
    Supprime une ligne de la base de données basée sur une condition donnée.

    :param server: Adresse du serveur de la base de données.
    :param database: Nom de la base de données.
    :param username: Nom d'utilisateur pour se connecter à la base de données.
    :param password: Mot de passe pour se connecter à la base de données.
    :param table_name: Nom de la table où la ligne doit être supprimée.
    :param condition: Condition à utiliser pour identifier la ligne à supprimer (ex: "id = 5").
    """
    conn = None
    try:
        conn = youtils.connect_to_sql_server()
        with pyodbc.connect(conn) as conn:
            with conn.cursor() as cursor:
                query = f"DELETE FROM {table_name} WHERE {condition}"
                cursor.execute(query)
                conn.commit()  # Commit the transaction
                if cursor.rowcount > 0:
                    print(f"Data deleted successfully where {condition}")
                else:
                    print("No data found to delete.")
    except pyodbc.Error as e:
        print("Error while deleting data:", str(e))
        
def fetch_data():
    conn = None
    try:
        conn = youtils.connect_to_sql_server()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Collection")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except pyodbc.Error as err:
        print(f"Erreur de base de données: {err}")
        return []

if __name__ == "__main__":
    action = input("Do you want to insert (i), list (l), update (u), or delete (d) data? ")
    if action.lower() == 'i':
        # Demander à l'utilisateur de saisir les données
        quantite = input("Entrez la quantité : ")
        nom = input("Entrez le nom : ")
        distillerie = input("Entrez la distillerie : ")
        annee = input("Entrez l'année : ")
        age = input("Entrez l'âge : ")
        degre = input("Entrez le degré : ")
        date_achat = input("Entrez la date d'achat (AAAA-MM-JJ) : ")
        prix = input("Entrez le prix : ")
        insert_data(server, database, username, password, quantite, nom, distillerie, annee, age, degre, date_achat, prix)
        pass
    elif action.lower() == 'l':
        # Lister les données de la base de données
        list_data()
        pass
    elif action.lower() == 'u':
        # Demander à l'utilisateur de saisir les données pour identifier la ligne à mettre à jour
        quantite = input("Entrez la quantité à mettre à jour : ")
        nom = input("Entrez le nom à mettre à jour : ")
        distillerie = input("Entrez la distillerie à mettre à jour : ")
        annee = input("Entrez l'année à mettre à jour : ")
        age = input("Entrez l'âge à mettre à jour : ")
        degre = input("Entrez le degré à mettre à jour : ")
        date_achat = input("Entrez la date d'achat (AAAA-MM-JJ) à mettre à jour : ")
        prix = input("Entrez le prix à mettre à jour : ")
        # Demander à l'utilisateur de saisir les nouvelles données
        new_quantite = input("Entrez la nouvelle quantité : ")
        new_nom = input("Entrez le nouveau nom : ")
        new_distillerie = input("Entrez la nouvelle distillerie : ")
        new_annee = input("Entrez la nouvelle année : ")
        new_age = input("Entrez le nouvel âge : ")
        new_degre = input("Entrez le nouveau degré : ")
        new_date_achat = input("Entrez la nouvelle date d'achat (AAAA-MM-JJ) : ")
        new_prix = input("Entrez le nouveau prix : ")
        # Convertir annee et degre en types appropriés
        annee = int(annee)
        degre = float(degre)
        new_annee = int(new_annee)
        new_degre = float(new_degre)
        # Mettre à jour les données dans la base de données
        update_data(server, database, username, password, nom, annee, degre, new_quantite, new_nom, new_distillerie, new_annee, new_age, new_degre, new_date_achat, new_prix)
        pass
    elif action.lower() == 'd':
    # Supposons que `fetch_data` est une fonction qui récupère toutes les données que l'utilisateur peut vouloir supprimer
        data_to_delete = fetch_data(server, database, username, password)
        if not data_to_delete:
            print("Aucune donnée disponible pour la suppression.")
        else:
            # Afficher les données avec des numéros
            for i, row in enumerate(data_to_delete, start=1):
                print(f"{i}. Quantité: {row.Quantite}, Nom: {row.Nom}, Distillerie: {row.Distillerie}, Année: {row.Année}, Age: {row.Age}, Degrés: {row.Degrés}, Date d'achat: {row.Date_achat}, Prix: {row.Prix}")

                # Demander à l'utilisateur de choisir le numéro de la ligne à supprimer
            try:
                choice = int(input("Entrez le numéro de la ligne à supprimer : "))
                if 1 <= choice <= len(data_to_delete):
                    selected_row = data_to_delete[choice - 1]
                    # Demander confirmation avant de supprimer
                    confirm = input(f"Êtes-vous sûr de vouloir supprimer la ligne {choice}? (oui/non): ")
                    if confirm.lower() == 'oui':
                    # Supprimer la ligne sélectionnée
                        delete_row(server, database, username, password, "Collection", f"Nom = '{selected_row.Nom}' AND Année = {selected_row.Année} AND Degrés = {selected_row.Degrés} AND Date_achat = '{selected_row.Date_achat}' AND Prix = {selected_row.Prix} AND Quantite = {selected_row.Quantite} AND Distillerie = '{selected_row.Distillerie}' AND Age = {selected_row.Age}")
                        print("Donnée supprimée avec succès.")
                    else:
                        print("Suppression annulée.")
                else:
                    print("Numéro de ligne invalide.")
            except ValueError:
                print("Veuillez entrer un nombre valide.")