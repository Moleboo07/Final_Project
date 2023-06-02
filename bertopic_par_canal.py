#penser à faire un pip install bertopic et unidecode dans l'environnement virtuel

import pandas as pd
import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk import word_tokenize
nltk.download(['punkt','wordnet','stopwords'])

from bertopic import BERTopic
from sklearn.datasets import fetch_20newsgroups

from unidecode import unidecode

import matplotlib.pyplot as plt


chemin_acces = ""

def bertopic_fct(chemin_acces, canal):
	df = pd.read_csv(chemin_acces, sep=";")
	df_APE_DL = df[df[canal] == 1]
	df_APE_DL = df_APE_DL.loc[:, ['Description', canal]]

	df_APE_DL['Description'] = df_APE_DL['Description'].str.replace('\W', ' ', regex=True)
	df_APE_DL['Description'] = df_APE_DL['Description'].apply(lambda x: re.sub(r'[^a-zA-ZÀ-ÿ0-9 ]', '', x))
	df_APE_DL['Description'] = df_APE_DL['Description'].apply(lambda x: unidecode(x.lower()))
	df_APE_DL['Description_2'] = df_APE_DL['Description'].apply(lambda x: nltk.word_tokenize(x))

	french_stopwords = stopwords.words('french')
	french_stopwords = french_stopwords + ['pole', 'emploi', 'a', 'jai', 'cest', 'ete', 'faire', 'fait', 'tres', 'car', 'donc', 'cela', 'si', 'cette', 'alors', 'ai', 'nest', 'comme', 'etre', 'toujours', 'quil', 'avoir', 'ca', 'dun', 'quand', 'peut', '2', 'na', 'dit', 'faut', 'dune', 'tous', 'chaque', '3', 'suite', 'espace', '1', 'ni', 'simple', 'trop', 'pourquoi', 'pouvoir', 'deux', 'aussi', 'etait', 'beaucoup', 'moins', 'jamais', 'avant', 'pu', 'part', 'peux', 'javais', 'cas', 'deja', '2022', 'merci', 'lon', 'afin', 'autre', 'encore', 'quelle', 'quon', 'dois', 'propose', 'ny', 'bonjour', 'quils', 'lors', 'peu', 'quoi', 'dire', '4', 'passe', 'toutes', 'vers', 'prendre', 'pendant', 'comment', 'mettre', 'debut', 'periode', 'quelques', 'pris', 'pourtant', 'place', 'entre', 'via', 'chez', 'besoin', 'dont', 'va', 'bon', 'detre', 'concernant', 'voir', 'reste', 'mal', 'trouver', 'tant', 'possible', '6', '15', '5', 'maintenant', 'puis', 'donne', 'juste', 'seul', 'etaient', 'cetait', 'recois', 'manque', 'sous', 'davoir', 'retrouve', 'nombre', 'directement', 'toute', 'seule', 'cet', 'vraiment', 'nont', 'sest', 'vais', 'complique', 'malgre', 'lorsque', 'parce', 'comprendre', 'exemple', 'doit', 'aujourdhui', 'suivre', 'surtout', 'fonctionne', 'mis', '0', 'egalement', 'sais', 'ainsi', 'tard', 'vie', 'souhaite', 'pense', 'ensuite', 'autres', '20', 'fais', 'remplir', 'cause', 'niveau', 'leurs', 'premiere', 'puisque', 'rendre', '2023', 'permet', 'viens', 'perdre', '2021', 'vu', 'sinon', 'or', 'cours', 'oblige', 'change', 'possibilite', 'donner', 'mise', 'bout', 'savoir', 'partir', 'cordialement', 'aupres', 'monde', 'netait', 'changer', 'prise', 'coup', 'mont', 'sauf', 'precise', 'bref', 'jen', 'perdu', 'assez', 'chercher', 'indique', 'passer', 'percu', 'trois', 'partie', 'carriere', 'etc', 'calcul', 'mieux', 'choses', 'seulement', 'transmis', "aider", "laide", "moment", "differents", "elles", "clair", "raison", "quelquun", "laquelle", "maider", "facile", "jetais", "chose", "etant", "disant", "cadre", "dernier", "cote", "fournir", "font", "quune", "arrive", "memes", "dautres", "bonjourje", "bonne", "solution", "dommage", "rester", "retrouver", "dates", "derniere", "effectue", "voulu", "semble", "long", "acces", "beneficier", "certains", "bloque", "daide", "valide", "an", "postule", "parle", "30", "facon", "realite", "madame", "choix", "societe", "cesu", "correctement", "10", "charge", "peuvent", "donnees", "radie", "malheureseument", "notamment", "veux", "jusqua", "aller", "parler", "1er", "davance", "brut", "signaler", "final", "quel", "creer", "creation", "case", "reprises", "changement", "actuellement", "radiation", "comprehension", "clairement", "premier", "souvent", "7", "nombreux", "competences", "effet", "prend", "vue", "dobtenir", "disponible", "veut", "grace", "presque", "oui", "nen", "rapide", "cherche", "sait", "efficace", "pouvais", "parfois", "qua", "grande", "moyens", "uniquement", "marche", "moyen", "totalement", "mest", "pose", "devrait", "plein", "su", "motif", "lire", "grand", "durant", "constate", "voila", "comprends", "plutot", "daller", "particulier", "ceux", "fallait", "dactivite", "faite", "celui", "avis", "tiens", "commence", "version", "sens", "genre", "decide", "pire", "sociale", "dautre", "puisse", "modifier", "remerciements", "ateliers", "accepter", "justifier", "preuve", "utiliser", "certaines", "jenvoie", "annnonces", "entreprises", "contre", "quun", "reussi", "completement", "telecharger", "monsieurveuillez", "enfin", "necessaire", "denvoyer", "tombe", "pouvait", "fourni", "2020", "vrai", "devais", "tente", "etes", "motivation", "vecu", "doute", "difficile", "voire", "lecoute", "recherches", "surprise", "deplacer", "jaurais", "sert", "celle", "delai", "quant", "fausses", "mots", "laisse", "qualite", "explique", "suivant", "effectuees", "periodes", "francais", "dabord", "celleci", "explication", "total", "ici", "domaine", "pratique", "acceder", "pourrait", "permis", "desormais", "monsieur", "doivent", "correspond", "heureseument", "bravo", "dailleurs", "particuliers", "complexe", "utilise", "postuler", "quen", "lai", "effectuer", "nimporte", "navais", "mot", "mauvaise", "validation", "reprendre", "maniere", "ressenti", "vont", "explications", "rapport", "prive", "moindre", "rapidement", "chance", "faux", "limitte", "precedent", "essaye", "chomeur", "tellement", "technique", "conseils", "zero", "carte", "sachant", "confiance", "reception", "pieces", "confirmation", "candidatures", "secteur", "proposer", "claire", "corriger", "vivre", "devient", "matin", "point", "general", "arriver", "simplement", "navait", "nexiste", "verifier", "jattends", "quelque", "rupture", "minimum", "celuici", "moimeme", "sil", "devoir", "informe", "transimission", "partiel", "parfaitement"]

	df_APE_DL['Description_2'] = df_APE_DL['Description_2'].apply(lambda x : [item for item in x if item not in french_stopwords])

	#stemming, mise à la racine
	stemmer=SnowballStemmer('french')
	df_APE_DL['Description_2']=df_APE_DL['Description_2'].apply(lambda x: [stemmer.stem(item) for item in x ])

	mots_a_supprimer = ["pol", "emploi", "plus", "demand", "mois", "tout", "mem", "bien", "aucun", "san", "jour", "nai", "demploi", "rien", "fin", "apre", "an", "non", "plusieur", "impossibl", "droit", "recu", "trouv", "recherch", "actualis", "envoi", "suiv", "dactualis", "aid", "mensuel", "envoy", "lactualis", "post", "trait", "projet", "pag", "retour", "repond", "lagenc", "fich", "activit", "entrepris", "experient", "repondr", "gen", "anne", "inscript", "renseign", "obten", "repondu", "difiicult", "nom", "prestat", "mont", "valid", "fonction", "annonc", "rencontr", "meti", "lieu", "attent", "met", "rend", "lettr", "commun", "present", "pert", "disposit", "resultat", "echang", "adress", "dev", "referent", "different", "recevoir", "vers", "candidat", "candidatur", "complet", "franc", "informat", "accompagn", "mactualis", "parcour", "organ", "continu", "transmettr", "sais", "touch", "reel", "certain", "bas", "minscrir", "reunion", "papi", "malheur", "chiffr", "del", "correspond", "vill", "sort", "spectacl", "bon", "pens", "precis", "realis", "normal", "ancien", "assist", "connaiss", "salar", "import", "automat", "dinform", "regl", "essai", "souhait", "relanc", "consider", "physiqu", "evit", "risqu", "sent", "amelior", "inutil", "ecrit", "evident", "mission", "depos", "utilis", "compliqu", "domicil", "cotis", "petit", "not", "ven", "cre", "rentr", "diplom", "faudr", "direct", "dembauch", "alle", "obligatoir", "pass", "doc", "signal", "finalis", "proposit", "fais", "precedent", "social", "financier", "manqu", "pouv", "lenvoi", "boit", "gagn", "reessai", "heureux", "dis", "particip", "menac", "excus", "agreabl", "loi", "permet", "oblig", "sollicit", "rejet", "termin", "sactualis", "appliqu", "fait", "don", "forc", "control", "linscript", "text", "imprim", "modif", "negat", "rubriqu", "fichi", "stag", "men", "consult", "bel", "cliqu", "doffr", "statut", "limit", "esper", "propos", "enregistr", "cens", "devenu", "scann", "simplif", "recrut", "con", "deplac", "accept", "coch", "relat", "ger", "cour", "voul", "sag", "term", "form", "indiqu", "sujet", "journe", "principal", "regularis", "affich", "cop", "naur", "desolesincerementun", "cod", "croir", "rempl", "oubl", "convers", "embauch", "adapt", "serieux", "absolu", "proch", "dysfonction", "ouvr", "prim", "humain", "narriv", "fauss", "comport", "verit", "connu", "declare", "prochain", "expliqu", "laiss", "rendu", "envi", "pourr", "notif", "8", "sign", "vis", "pein", "method", "minform", "mindiqu", "annul", "dutilis", "fourn", "depart", "environ", "interess", "mention", "bienveil", "lappliqu", "calcul", "mesur", "feuill", "avanc", "centr", "bilan", "chacun", "logiciel", "are", "euro", "faut", "econom", "enfant", "necessair", "ladministr", "client", "lattest", "revenu", "lorgan", "list", "transmiss", "quel", "25", "factur", "retourn", "deuxiem", "typ", "publiqu", "final", "piec", "commenc", "outil", "desagre", "relev", "parent", "dur", "facilit", "local", "lass", "12", "decu", "supprim", "aut", "multipl", "fort", "contrair", "lespac", "longu", "62", "posit", "champ", "refuse", "ailleur", "consequent", "exig", "trimestr", "regret", "28", "voi", "titr", "systemat", "particulier", "ladress", "formul", "formateur", "remerc", "dam", "dinscript", "arret", "coordonne", "tourn", "enorm", "dit", "suffis", "concern", "repris", "comprend", "gros", "lav", "chois", "loffr", "ecout", "activ", "transmis", "action", "detail"]
	df_APE_DL['Description_2'] = df_APE_DL['Description_2'].apply(lambda x : [item for item in x if item not in mots_a_supprimer])

	mot_supp_DL =["conseiller","email", "telephon","mail","angoiss","sit","depuis", "conseil", "travail", "situat", "travaill", "nouvel", "demandeur", "lign", "problem", "erreur", "nouveau", "question", "professionnel", "messag", "ci", "entretien", "public", "accueil", "cv", "pe", "difficult", "inscrir", "etais", "joindr", "emplois", "quelqu", "ordin", "travaille", "employ", "pre", "veuill", "fr", "exist", "attendr", "chomeur", "etat", "age", "rappel", "temp", "heur", "dat", "semain", "aujourd", "hui", "septembr", "fevri", "minut", "aout", "jusqu", "mar", "janvi", "octobr", "decembr", "novembr", "mai", "avril", "fois", "inform", "nul", "etoil", "refus", "numero", "hont", "catastroph", "sup", "mid", "incap", "gar", "port", "pet", "allez", "servent", "bat", "aim", "franch", "honteux", "lament", "mobilit", "organis", "beau", "vit", "loin", "devr", "incroi", "symp", "fer"]
	df_APE_DL['Description_2'] = df_APE_DL['Description_2'].apply(lambda x : [item for item in x if item not in mot_supp_DL])

	#préparation de la donnée pour bertopic cra pas possible sous forme de token
	df_APE_DL["Description_3"]=df_APE_DL["Description_2"].apply(lambda x: " ".join(x))

	all_items = []
	for items in df_APE_DL['Description_2']:
	    all_items.extend(items)

	#print(all_items)

	#bertopic
	docs = df_APE_DL['Description_3'].tolist()
	topic_model = BERTopic(language="french", min_topic_size=15, nr_topics=20, top_n_words= 10)
	topics, probs = topic_model.fit_transform(docs)

	df_APE_DL['clusters']= topics
	print(df_APE_DL['clusters'])
	print("######################")
	print(topic_model.get_topic_info())
	data = topic_model.visualize_barchart(top_n_topics=20, n_words=10)
	# Créer les sous-graphiques séparés
	fig, axs = plt.subplots(len(data['data']), 1, figsize=(10, len(data['data']) * 3), sharex=True)

	# Parcourir les données et créer les graphiques séparés
	for i, d in enumerate(data['data']):
	    ax = axs[i]
	    ax.barh(d['y'], d['x'], color=d['marker']['color'], align='center')
	    ax.set_title(f'Topic {i}', fontsize=16)
	    ax.set_xlabel('Scores')
	    ax.set_ylabel('Mots')
	    ax.grid(True)

	# Ajuster les espacements entre les sous-graphiques
	plt.tight_layout()

	# Afficher les graphiques dans une fenêtre pop-up
	plt.show()

	#plt.show()

canal = "telephone"

chemin_acces="C:\\Users\\poire\\OneDrive\\Bureau\\topic_pe\\can_rep.csv"
bertopic_fct(chemin_acces, canal)
chemin_acces="C:\\Users\\poire\\OneDrive\\Bureau\\topic_pe\\channel_2.csv"
bertopic_fct(chemin_acces, canal)