#on importe toutes les bibliothèques nécessaires
'''
malheureusement la partie musique du code ne marche, il y a eu des problèmes avec les API, toutes les bibliothèques testées se sont trouvées obsolètes, en python
il semble ne plus y avoir de moyen de coder un bot discord de musique à moins de créer soi même son API, c'est cela dit possible en js.
'''
#bibliothèque discord de base, et son extension "commands" ainsi que "app_commands" pour pouvoir faire des commandes slash, et le get pour la récupération de données
import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
#les bibliothèques utilisées pour la partie musique
import asyncio
import youtube_dl
#on en a besoin pour l'économie
from random import randint
#on importe les autres codes avec nos classesp our les bases de donnée
from warn_classe import BaseDeDonnee, warn
from economie_classe import Economie
from rp_classe import FichePerso


#on définit le client, le bot et toutes les permissions qu'on lui donne en prenant tout les intents
intents = discord.Intents().all()
#le "command_prefix" définit le prefix utilisé par le bot. Sur notre serveur discord, chaque commande que l'on fait au bot devra être précédé du prefix (collé à la commande)
bot = commands.Bot(command_prefix = "§", intents=intents)

#on rajoute des intents pour pouvoir les utiliser (ici on n'a besoin que des utilisateurs, du serveur et des messages)
intents.message_content = True
intents.guilds = True
intents.members = True
intents.messages = True

#on définit "tree" pour effectuer des tree.command à savoir des commandes slash
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


voice_clients = {}

# On met les paramètres de youtube_dl pour l'optimisation du streaming
yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)
#ffmpeg permet de lire le son de vidéos dont on importe le lien, on n'a pas réellement cerné les commandes d'ffmpeg
ffmpeg_options = {'options': "-vn"}

    
    
#on créé une base de données que l'on va appeler bdd, on lui donne le nom de notre table à savoir avertissement.db
bdd = BaseDeDonnee("avertissement.db")


#on va instancier un objet de la classe FichePerso avec comme nom le nom de notre table soit "ficheperso.db"
bdd_fiche = FichePerso("ficheperso.db")


#on instancie une base de donnée d'Economie avec comme nom, le nom de notre base de donnée soit "economie.db"
bdd_eco = Economie("economie.db")


#on fait ça pour supprimer la commande Help de départ et en rajouter une autre personnalisée
bot.remove_command("help")



#ici on vérifie que le bot s'est bien connecté, et on renvoit son nom et id, puis on regarde le nombre de tree.command synchronisées. Ici on n'a pris aucun serveur en particulier donc il n'y en a aucune
@bot.event
async def on_ready():
    print(f"{bot.user.name} s'est connecté avec succès !")
    print("Nom du bot :",bot.user.name)
    print("ID du bot :",bot.user.id)
#puis on regarde le nombre de tree.command synchronisées. Ici on n'a pris aucun serveur en particulier donc il n'y en a aucune
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")

    except Exception as e:
        print(e)


#on définit ici l' "owner" d'un serveur, qui ne servira ensuite que pour la commande /owner
def is_owner():
    def predicate(interaction: discord.Interaction):
    #on renvoit True si la personne qui fait la commande est bien l'owner du serveur, ce qui lui permettra d'exécuter la commande
        if interaction.user.id == interaction.guild.owner.id:
            return True
    return app_commands.check(predicate)



@bot.command()
async def help(ctx):
    #on va créer un message en embed pour que ce soit plus joli et plus lisible
    #les embed sont des messages particuliers compris dans une cellule dans lesquels on peut personnaliser de nombreuses chose, comme la couleur, ou mettre des liens, des images, etc
    embed = discord.Embed(title="Informations sur le bot", description=f"**{bot.user.name}** est un bot de musique (qui marche pas), de modération, et de Roleplay\
                          \nVoici ses fonctions :", color=discord.Color.blurple())
    
    #on va écrire l'embed en lignes séparées au lieu de faire un seul gros embed.add_field, pour des quesstions de lecture de code
    embed.add_field(name="Commandes :", value="liste des commandes du serveur", inline=False)
    embed.add_field(name="§help", value="Renvoie la liste des commandes disponibles", inline=False)
    embed.add_field(name="§ping", value="Cette commande renvoie Pong", inline=False)
    embed.add_field(name="§coucou", value="Pour saluer le bot", inline=False)
    embed.add_field(name="§servinfo", value="Donne diverses informations sur le serveur", inline=False)
    embed.add_field(name="§quoi", value="Je vous laisse essayer", inline=False)
    embed.add_field(name="/owner (réservée au gérant du serv)", value="Un bonjour spécial pour les rois", inline=False)
    embed.add_field(name="/warn <mentionner un membre du serveur> <entrer une raison>", value="Pour donner un avertissement à un membre du serveur", inline=False)
    embed.add_field(name="§mute", value="Pour rendre muet un membre dans un salon vocal", inline=False)
    embed.add_field(name="§unmute", value="Pour rétablie la voix membre dans un salon vocal", inline=False)
    embed.add_field(name="§ban <mentionner un membre du serveur> <entrer une raison>", value="Pour bannir un membre du serveur", inline=False)
    embed.add_field(name="§unban <mentionner un membre banni du serveur>", value="Pour débannir un membre du serveur (ne marche pas)", inline=False)
    embed.add_field(name="§kick <mentionner un membre du serveur>", value="Pour expulser un membre du serveur sans le bannir", inline=False)
    embed.add_field(name="§play <coller l'URL d'une vidéo ytb>", value="Pour jouer de la musique si vous êtes en vocal (ne marche pas à cause des bibliothèques)", inline=False)
    embed.add_field(name="§pause", value="Pour mettre la musique actuelle en pause (ne marche pas car play ne marche pas)", inline=False)
    embed.add_field(name="§resume", value="Pour relancer la musique en pause (ne marche pas car play et pause ne marchent pas)", inline=False)
    embed.add_field(name="§stop", value="Pour déconnecter le bot du vocal (marche)", inline=False)
    embed.add_field(name="§créerperso", value="Pour se créer un personnage de roleplay (très basique)\nune fois la commande lancée, le bot vous donnera des instructions", inline=False)
    embed.add_field(name="§afficherperso", value="Pour afficher votre personnage", inline=False)
    embed.add_field(name="§créercompte", value="Pour se créer un compte sur l'économie du serveur", inline=False)
    embed.add_field(name="§beg", value="Pour gagner entre 15 et 60 pessos, aucune limite de temps, vous pouvez spam la commande", inline=False)
    embed.add_field(name="§leaderboard", value="Affiche la liste des membres les plus riches du serveur", inline=False)

    await ctx.send(embed=embed)


#commande classique, le nom de la commande est définit par "name"
@bot.command(name='ping', help='commande qui sert pas à grand chose')
async def ping(ctx):
    #avec le send, on demande au bot d'envoyer comme message ce qui est entre parenthèse à la suite
    await ctx.send(f'Pong')

#commande classique
@bot.command(name="coucou", help="Pour dire bonjour au bot (la politesse)")
async def coucou(ctx):
    await ctx.send('Bonjour jeune entrepreneur ! Avez vous acheté ma masterclass en ligne ?')

#commande de serveurinfo, qui renvoie les caractéristiques voulues du serveur sur lequel on est
@bot.command(name="servinfo", help="Commande qui renvoie les caractéristiques du serveur")
async def servinfo(ctx):
    #ici on décrit toutes les info qu'on va vouloir donner
    nb_textchannel = len(ctx.guild.text_channels)
    nb_voicechannel = len(ctx.guild.voice_channels)
    nbmembre = ctx.guild.member_count
    servName = ctx.guild.name
    #on créé le message que l'on va envoyer puis on l'envoie
    message = f"Bienvenue sur le serveur **{servName}**. \nCelui-ci possède **{nbmembre}** membres et contient **{nb_textchannel}** salons écrits et **{nb_voicechannel}** salons vocaux."
    await ctx.send(message)

#commande classique (pas franchement obligatoire)
@bot.command(name = "quoi", help= "ceci n'est pas un exercice")
async def quoi(ctx):
    await ctx.send(f"feur")


#c'est une commande slash ce qui veut dire qu'elle s'appelle avec un / et non pas avec un § comme les autres commandes
#le "guild" définit sur quel serveur la commande sera effective, si l'on ne met pas de "guild" alors elle sera effective sur tout les serveurs où se trouve le bot
@bot.tree.command(guild=discord.Object(id=1215215746905542656),name="owner", description="Commande réservée au proprio du serv")
#le is_owner vérifie que la personne qui lance la commande est bien le créateur du serveur
@is_owner()
#l'ajout de "interaction" permet au bot lorsque l'on créé la commande de faire quelque chose en retour
async def owner_slash(interaction: discord.Interaction):
    #ici, ce n'est pas comme les commandes classiques on doit faire un "interaction.response.send_message" pour répondre quelque chose, l'ephemeral=True signifie que seul
    #celui qui a fait la commande peut voir le message
    await interaction.response.send_message(f"Enchanté boss {interaction.user.mention}",ephemeral=True)


#une commande slash
@bot.tree.command(guild=discord.Object(id=1215215746905542656), name="test", description="Du coup ça c'est un test")
async def test_slash(interaction: discord.Interaction):
    await interaction.response.send_message('Test réussi avec succès réussi positivement de façon positive')


#la command warn qui va faire appel à nos fonctions tout en haut du code, c'est une commande slash ce qui veut dire qu'elle s'appelle avec un /
#avec cette commande on va appeler la fonction "create_warn" dans notre "BaseDeDonnee" pour ajouter les données du warn à la base de données
#puis on appelle la fonction "warn" dans warn_classe
@bot.tree.command(guild=discord.Object(id=1215215746905542656), name="warn", description="gestion_avertissement")
async def warn_command(interaction: discord.Interaction, member : discord.Member, reason : str):
    bdd.create_warn(member.name, interaction.guild.id, 1, reason)
    await warn(interaction, member, reason)


#commande mute pour activer le mute dans un salon vocal sur discord sur un membre du serveur    
@bot.command()
#on a le ctx qui est fournit de base dans le message, ainsi que le membre à mute qui doit être mentionné dans l'appel à la commande et la raison derrière
async def mute(ctx : commands.Context, member : discord.Member, *, reason : str = ""):

    #on teste si la commande a été utilisée en message privé (on a pas de bot dans des groupes de message privé donc ce if ne servira pas)
    if ctx.guild is None and isinstance(ctx.author, discord.User):
        return await ctx.send('Cette commande ne peut pas être utilisé pour les messages privés')

    #ici on teste si l'auteur de la commande a les permissions pour gérer les permissions de salons
    if not ctx.author.guild_permissions.manage_channels:
        return await ctx.send(f"Désolé {ctx.author.name} vous n'avez pas l'autorisation pour utiliser cette commande")

    #si notre rôle de plus haut rang est moins haut rang que celui de la personne que l'on veut mute, cette commande ne marche pas
    if not ctx.author.top_role > member.top_role:
        return await ctx.send('Vous ne pouvez pas muter ce membre, il est trop haut gradé capitaine')

    #si la personne ciblée n'est pas dans un salon vocal
    if member.voice is None:
        return await ctx.send("Ce membre n'est pas dans un salon")

    if reason == "":
        reason = "Aucune raison n'a été fournit"
    #ici on gère les permissions de la personne mute pour enfin la mute une fois que tout a été testé
    await member.edit(mute=True,reason=reason)

    return await ctx.send(f"{member.name} a été mute pour {reason}. J'espère que c'était pas une bavure policière")


#commande unmute pour réactiver le micro d'un membre que l'on a mute
@bot.command()
async def unmute(ctx : commands.Context, member : discord.Member, *, reason : str = ""):

    #ce sont les même tests que pour la commande mute
    if ctx.guild is None and isinstance(ctx.author, discord.User):
        return await ctx.send('Cette commande ne peut pas être utilisé pour les messages privés')

    
    if not ctx.author.guild_permissions.manage_channels:
        return await ctx.send("Vous n'avez pas l'autorisation pour utiliser cette commande")

    
    if not ctx.author.top_role > member.top_role:
        return await ctx.send('Vous ne pouvez pas muter ou unmuter ce membre')


    if member.voice is None:
        return await ctx.send("ce membre n'est pas dans un salon")

    if reason == "":
        reason = "No reason provided"
    #ici on rétabli le micro de la personne
    await member.edit(mute=False,reason=reason)

    return await ctx.send(f'{member.name} a été unmute')


#commande ban classique, on ban l'utilisateur mentionné et on envoie un message de confirmation avec la raison du ban
@bot.command(name = "ban", help="pour ban des gens quoi")
async def ban(ctx, user : discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.ban(user, reason = reason)
    await ctx.send(f"{user} à été ban pour la raison suivante : {reason}.")


#commande d'unban classique, elle ne marche plus avec les nouveaux profils d'utilisateurs de discord qui n'utilisent plus de # et de numéros derrière.
@bot.command(name = "unban", help="pour unban des gens quoi")
async def unban(ctx, user, *reason):
    reason = " ".join(reason)
    #cette partie ne marche plus, ce qui pose problème pour le reste du code
    bannedUsers = get(ctx.guild.bans())
    for i in bannedUsers:
        #on cherche si l'user rentré est dans la liste des bannis et dans ce cas on le débannit 
        if i.user.name == user.name:
            await ctx.guild.unban(i.user, reason = reason)
            await ctx.send(f"{user} à été unban.")
            return
    #Ici on sait que lutilisateur na pas ete trouvé donc on envoie un message correspondant
    await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")


#commande kick classique, marche comme la commmande pour le ban
@bot.command(name = "kick", help="pour kick des gens quoi")
async def kick(ctx, user : discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.kick(user, reason = reason)
    await ctx.send(f"{user} à été kick.")


# Commande pour play la musique, on ne sait pas pourquoi mais elle ne marche pas
@bot.command(name="play", description = "alors ça joue ?")
async def play(ctx):
    #ici on va faire se connecter le bot dans le salon où est l'utilisateur qui a fait la commande
    try:
        voice_client = await ctx.author.voice.channel.connect()
        voice_clients[voice_client.guild.id] = voice_client
    #si l'utilisateur n'est pas dans un salon on print error
    except:
        print("error")

    try:
        #on va split le message entre la partie commande et la partie url, la partie url étant msg.content.split()[1] (puisque [0] c'est la commande)
        url = ctx.message.content.split()[1]
        #on envoit un message de confirmation dans le salon où la commande a été exécutée pour vérifier que tout se passe correctement
        await ctx.send(f"Je lance {url}")
        #avec yt_dl
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        #le "song" c'est ce qui va être joué, et le player devrait jouer la musique 
        song = data['url']
        player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song, **ffmpeg_options))
        #cette commande devrait jouer le son défini par player. Le code ne nous renvoit pas de réelle erreur, mais apparemment cette biblitohèque semble ne pas bien marcher
        voice_clients[ctx.guild.id].play(player)

    #ici on demande de print l'erreur s'il y a, ce qui est fait on voit dans notre terminal le problème posé (en l'occurence un problème de bibliothèque)
    except Exception as err:
        print(err)


# Commande pour pause la musique
@bot.command(name = "pause", description = "pour pauser une musique déjà jouée")
async def pause(ctx):
    try:
        voice_clients[ctx.guild.id].pause()
    except Exception as err:
        print(err)

# Commande pour play le bot si il était sur pause
@bot.command(name = "resume", description = "pour relancer une musique mise en pause")
async def resume(ctx):
    try:
        voice_clients[ctx.guild.id].resume()
    except Exception as err:
        print(err)

# Commande qui stop la musique définitivement
@bot.command(name = "stop", description = "pour déconnecter le bot") 
async def stop(ctx):
    try:
        #on déconnecte également le bot
        voice_clients[ctx.guild.id].stop()
        await voice_clients[ctx.guild.id].disconnect()
    except Exception as err:
        print(err)


#la commande pour créer un personnage
@bot.command(name = "créerperso", help = "pour créer un personnage de rp")
async def creerperso(ctx):
    #d'abord on vérifie si l'auteur n'a pas déjà un perso, si c'est le cas on arrête la commande
    if bdd_fiche.dejapris(ctx.author.name):
        return await ctx.send(f"Désolé **{ctx.author.name}**, vous ne pouvez pas créer de perso car vous en avez déjà un")
    
    await ctx.send("Vous voulez vous créer un perso ? Commencez par me donner le nom de votre personnage :")
    #ici le checkMessage servira à vérifier que la réponse au bot est bien par l'auteur de la commande et dans le même salon que la commande originelle
    def checkMessage(message):
        return message.author == ctx.message.author and ctx.message.channel == message.channel
    #ici on a un timeout de 60secondes, au bout de ces 60 secondes le try est raté, on a une erreur, donc on passe dans le except où le bot dit "commande annulée"
    try:
        #le bot.wait_for demande au bot d'attendre une réponse, ici pendant 60 secondes et avec le paramètre obligatoire du checkMessage
        nom = await bot.wait_for("message", timeout=60, check = checkMessage)
    except:
        return await ctx.send(f"commande annulée")
    #ici on a passé le try, donc on continue dans notre commande, le bot renvoie le contenu du message de réponse de l'utilisateur à savoir le nom de son perso
    await ctx.send(f"Bien, votre nom est : **{nom.content}**. Veuillez désormais choisir votre âge : ")
    #on refait l'opération pour toutes les caractéristiques du personnage
    try:
        age = await bot.wait_for("message", timeout=60, check = checkMessage)
    except:
        return await ctx.send(f"commande annulée")

    await ctx.send(f"Vous avez rentré votre âge, vous avez **{age.content}** ans. Choisissez maintenant votre classe :")
    try:
        classe = await bot.wait_for("message", timeout=60, check = checkMessage)
    except:
        return await ctx.send(f"commande annulée")
    
    await ctx.send(f"Vous êtes de la classe **{classe.content}**, choisissez maintenant votre race :")
    try:
        race = await bot.wait_for("message", timeout=60, check = checkMessage)
    except:
        return await ctx.send(f"commande annulée")
    
    await ctx.send(f"Vous êtes de la race **{race.content}**, choisissez enfin votre capacité spéciale (ça peut être n'importe quoi) :")
    try:
        capacite = await bot.wait_for("message", timeout=60, check = checkMessage)
    except:
        return await ctx.send(f"commande annulée")
    #ici on va stocker le message du bot dans une variable "message" car on va ensuite lui demander de rajouter 2 réactions à ce message
    message = await ctx.send(f"Votre capacité spéciale est **{capacite.content}**. Un café avec ceci ?")
    await message.add_reaction("✅")
    await message.add_reaction("❌")
    #comme pour le checkMessage on fait un checkReaction pour s'assurer que ce soit la bonne personne, dans le bon salon, avec les bonnes réactions qui réagit
    def checkReaction(reaction, user):
        return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")
    #le bot.wait_for "reaction_add" demande au bot d'attendre pendant un timeout de 60 secondes un ajout de réaction de l'utilsateur
    reaction, user = await bot.wait_for("reaction_add", timeout=60, check = checkReaction)
    #ici avec le bot on réagit en conséquence selon si l'utilisateur a réagit avec la ❌ ou le ✅
    if reaction.emoji == "✅":
        await ctx.send(f"Et un café.")
        cafe = "oui"
    elif reaction.emoji == "❌":
        await ctx.send(f"Ah. Pas de café.")
        cafe = "non"
    
    #enfin on affiche la fiche perso juste créée avec toutes ses caractéristiques
    bdd_fiche.create_perso(ctx.author.name, ctx.author.id, ctx.guild.id, nom.content, age.content, classe.content, race.content, capacite.content, cafe)

    #création d'un embed
    embed = discord.Embed(title=f"Personnage de {ctx.author.name}", description=f"Voici votre personnage :", color=discord.Color.blurple())

    embed.add_field(name="- Nom :", value=f"{nom.content}", inline=False)
    embed.add_field(name="- Age :", value=f"{age.content}", inline=False)
    embed.add_field(name="- Classe :", value=f"{classe.content}", inline=False)
    embed.add_field(name="- Race :", value=f"{race.content}", inline=False)
    embed.add_field(name="- Capacité :", value=f"{capacite.content}", inline=False)
    embed.add_field(name="- Un café ? :", value=f"{cafe}", inline=False)
    
    await ctx.send(embed=embed)
    
    
#cette commande sert à afficher le personnage de la personne qui exécute la commande
@bot.command(name = "afficherperso", help = "pour afficher son personnage")
async def afficherperso(ctx):
    #on va stocker dans une variable la liste de liste renvoyée par la méthode showfiche
    perso = bdd_fiche.showfiche(ctx.author.id)
    #création d'un embed
    embed = discord.Embed(title=f"Personnage de {perso[0][0]}", description=f"Voici votre personnage :", color=discord.Color.blurple())
    #on rajoute dans l'embed les informations qu'on a récupérés de notre tableau avec les indices.
    embed.add_field(name="- Nom :", value=f"{perso[0][1]}", inline=False)
    embed.add_field(name="- Age :", value=f"{perso[0][2]}", inline=False)
    embed.add_field(name="- Classe :", value=f"{perso[0][3]}", inline=False)
    embed.add_field(name="- Race :", value=f"{perso[0][4]}", inline=False)
    embed.add_field(name="- Capacité :", value=f"{perso[0][5]}", inline=False)
    embed.add_field(name="- Un café ? :", value=f"{perso[0][6]}", inline=False)
    
    await ctx.send(embed=embed)
    


#première commande pour créer un compte sur un serveur spécifique
@bot.command(name = "créercompte", help = "pour permettre à un utilisateur de créer un compte")
async def creercompte(ctx):
    #on exécute la méthode pasdecompte, si jamais ça nous renvoie False alors on a déjà un compte sur ce serveur et on ne peut pas en créer un deuxième
    if not bdd_eco.pasdecompte(ctx.author.id, ctx.guild.id):
        return await ctx.send(f"Désolé {ctx.author.name} vous ne pouvez pas créer d'autre compte sur ce serveur car vous en possédez déjà un.")
    
    #dans le cas contraire, on créé le compte sur le serveur avec un départ de 0 euros
    bdd_eco.create_account(ctx.author.name, ctx. author.id, ctx.guild.id, 0)
    await ctx.send(f"Votre compte sur ce serveur a été créé avec succès **{ctx.author.name}**")


#on fait une commande "beg" simple, où le bot nous donne simplement un montant aléatoire d'argent entre 15 et 60
@bot.command(name="beg", help="pour mendier de l'argent au bot (c'est votre seul option pour gagner de l'argent)")
async def beg(ctx):
    #si on n'a pas de compte sur le serveur alors on ne peut pas exécuter cette commande
    if bdd_eco.pasdecompte(ctx.author.id, ctx.guild.id):
        return await ctx.send(f"vous n'avez pas de compte et ne pouvez donc pas ajouter d'argent. Logique me direz vous. Tapez §créercompte pour vous créer un compte")
    
    #dans le cas contraire on ajoute bien les 15-60 euros au compte qui a fait la requête, il n'y a aucune limite de temps ce qu'il veut dire qu'on peut spam cette commande
    argentaAjouter = randint(15,60)
    bdd_eco.ajouterArgent(ctx.author.id, ctx.guild.id, argentaAjouter)
    await ctx.send(f"**{argentaAjouter}** pessos ont bien été rajoutés à votre compte {ctx.author.name}")


#une commande leaderboard pour voir le classement des membres les plus riches du serveur
@bot.command(name="leaderboard", help="commande pour voir l'économie du serveur du plus au moins riche")
async def leaderboard(ctx):
    #on stocke notre classement dans un tableau
    tableau = bdd_eco.classement(ctx.guild.id)

    #on créé un embed, messages souvent envoyés par des bots pour présenter des données de façon plus pratique, avec un titre, une description et une couleur définie.
    embed = discord.Embed(title="Classement", description="Voici le classement des membres les plus riches du serveur !", color=discord.Color.blurple())

    #ensuite on regarde pour chaque element dans notre tableau (on garde l'indice avec i) et on renvoie les valeurs une par une pour créer notre classement décroissant
    for i, element in enumerate(tableau):
            embed.add_field(name=f"- {i + 1}. **{element[0]}**",
                            value=f"{element[1]} pessos",
                            inline=False)
        
    #puis on envoie le message embed
    await ctx.send(embed=embed)



#on run le bot avec son token personnalisé, on ne le montre pas pour des raisons de confidentialité
# bot.run("...")