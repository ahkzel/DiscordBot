#on importe les bibliothèques nécessaires pour faire notre base de donnée
import os 
import sqlite3


#on créé une classe pour notre base de donnée pour l'appeler facilement
class FichePerso():
    def __init__(self, database_name : str):
        #ici on se connecte à notre base de donnée en prenant le chemin absolu dans nos fichiers
        self.connect = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{database_name}") 
        self.connect.row_factory = sqlite3.Row

    #méthode pour créer un perso, il y a beaucoup de paramètres à rentrer il faut faire attention aux int et aux str
    def create_perso(self, user_name: str, user_id: int, guild_id: int, perso_name : str, perso_age : int, perso_classe : str, perso_race : str, capacite_speciale : str, cafe : str):
        cursor = self.connect.cursor()
        #on exécute la commande sql avec toutes les valeurs puis on close la connexion
        insert_perso = "INSERT INTO ficheperso (user_name, user_id, serveur_id, perso_name, perso_age, perso_classe, perso_race, capacite_speciale, cafe) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"
        cursor.execute(insert_perso,(user_name, user_id, guild_id, perso_name, perso_age, perso_classe, perso_race, capacite_speciale, cafe))
        cursor.close()
        self.connect.commit()

    #méthode pour vérifier si quelqu'un a déjà créé un perso
    def dejapris(self, user_name: str):
        cursor = self.connect.cursor()
        #d'abord on va chercher tout les id stockés dans la table ficheperso
        user_liste = "SELECT user_name FROM ficheperso;"
        cursor.execute(user_liste)
        rows = cursor.fetchall()
        #puis on compare l'id de l'auteur de la requête avec toutes les id pour voir s'il est dedans, si c'est le cas on return True
        for n in rows:
            if n[0] == user_name:
                return True
        cursor.close()
        self.connect.commit()
        return False
    
    #méthode pour afficher la fiche perso d'un membre
    def showfiche(self, user_id: int):
        cursor = self.connect.cursor()
        #ici on regarde la ligne qui correspond à l'id de l'auteur pour pouvoir lui renvoyer toutes les caractéristiques de son perso
        fiche = "SELECT user_name, perso_name, perso_age, perso_classe, perso_race, capacite_speciale, cafe FROM ficheperso WHERE user_id = ?;"
        cursor.execute(fiche, (user_id,))
        rows = cursor.fetchall()
        cursor.close()
        return rows