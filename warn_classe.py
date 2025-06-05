#bibliothèque discord de base et le get pour la récupération de données
import discord
from discord.utils import get
#on importe les bibliothèques nécessaires pour faire notre base de donnée
import os 
import sqlite3



#on créé une classe pour notre base de donnée pour l'appeler facilement
class BaseDeDonnee():
    def __init__(self, database_name : str):
        #ici on se connecte à notre base de donnée en prenant le chemin absolu dans nos fichiers
        self.connect = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{database_name}") 
        self.connect.row_factory = sqlite3.Row

    #méthode de création de warn pour agir sur notre base de donnée avec tout ce qu'on aura définit
    def create_warn(self, user_name: str, guild_id: int, reason: str = None):
        cursor = self.connect.cursor()
        if reason:
            #on insère dans notre base de donnée toutes les données de l'avertissement que l'on vient d'envoyer
            insert_warn = "INSERT INTO avertissement (user_name, server_id, nb_warn, reason) VALUES (?, ?, ?, ?);"
            cursor.execute(insert_warn,(user_name, guild_id, 1, reason))
            cursor.close()
            self.connect.commit()
        else:
            print("problème")

#on créé une base de données que l'on va appeler bdd, on lui donne le nom de notre table à savoir avertissement.db
bdd = BaseDeDonnee("avertissement.db")

#on va faire des fonctions qui ne seront pas des fonctions du bot, mais des fonctions auxquelles nous feront appel dans notre commande warn pour assigner un rôle à une personne warn
async def get_warn_role(guild : discord.Guild) -> discord.Role:
    #on va créer un rôle n'ayant aucune permissions, en théorie il ne devrait être capable de rien faire mais les permissions
    #de base de discord font que sans restriction particulière salon par salon de ce rôle, il peut faire la même chose que s'il n'avait pas le rôle
    role = get(guild.roles, name=f"Avertissement n°1")
    if role is not None:
        return role
    else : 
        permission = discord.Permissions(send_messages = False)
        role = await guild.create_role(name="Avertissement n°1", permissions=permission)


#on créer la fonction warn qui envoit un message et assigne le rôle à la personne warn
async def warn(interaction: discord.Interaction, member : discord.Member, reason):
    if not reason:
        #on envoit un message à l'auteur de la commande grâce à l'ajout de "ephemeral=True"
        await interaction.reponse.send_message("**Tu es le seul à voir ce message**. Pour exercer cette commande, tu dois absolument donner une raison !", ephemeral=True)
    else :
        #on ajoute le rôle au membre puis on envoie le message de warn
        warn_role = await get_warn_role(interaction.guild)
        await member.add_roles(warn_role)
        await interaction.response.send_message(f"{member.mention} a été warn pour {reason}")