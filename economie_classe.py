#on importe les bibliothèques nécessaires pour faire notre base de donnée
import os 
import sqlite3



#on créé une classe pour notre base de donnée pour l'appeler facilement
class Economie():
    def __init__(self, database_name : str):
        #ici on se connecte à notre base de donnée en prenant le chemin absolu dans nos fichiers
        self.connect = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{database_name}") 
        self.connect.row_factory = sqlite3.Row

    #on fait une méthode pour se créer un compte dans un serveur spécifique quand rentrant son id
    def create_account(self, user_name: str, user_id: int, server_id: int, money: int):
        cursor = self.connect.cursor()
        creer_compte = "INSERT INTO economie (user_name, user_id, server_id, money) VALUES (?,?,?,?);"
        cursor.execute(creer_compte, (user_name, user_id, server_id, money))
        cursor.close
        self.connect.commit()

    #une méthode pour vérifier si l'on n'a pas de compte
    def pasdecompte(self, user_id: int, server_id: int):
        cursor = self.connect.cursor()
        user_list = "SELECT user_id, server_id FROM economie;"
        cursor.execute(user_list)
        rows = cursor.fetchall()
        #on prend la liste de tout les comptes créé dans le serv où la commande est exécuté
        for n in rows:
            if n[0] == user_id and n[1] == server_id:
                #si on voit une correspondance on return False car ça veut dire qu'on a déjà un compte
                return False
        cursor.close()
        self.connect.commit()
        #sinon on return True
        return True
        
    #une méthode pour rajouter de l'argent à un compte sur le serveur dans lequel a lieu la commande
    def ajouterArgent(self, user_id: int, server_id: int, money: int):
        cursor = self.connect.cursor()
        ajout = "UPDATE economie SET money = money + ? WHERE user_id = ? and server_id = ?;"
        cursor.execute(ajout, (money, user_id, server_id))
        cursor.close()
        self.connect.commit()

    #une méthode pour avoir accès aux noms et montants de tout les comptes créés sur un serveur
    def classement(self, server_id: int):
        cursor = self.connect.cursor()
        ranking = "SELECT user_name, money FROM economie WHERE server_id = ? ORDER BY money DESC;"
        cursor.execute(ranking, (server_id, ))
        #on met le tout dans rows que l'on return ensuite pour le stocker dans une autre variable et l'afficher
        rows = cursor.fetchall()
        cursor.close()
        self.connect.commit()
        return rows