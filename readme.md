Contexte du projet python

scraper les sites verif.com et société.com pour collecter les données recherchées

Informations collectées :
Siren
Raison sociale
Code NAF
Nom DG
Nom DAF
Nom D Financier
Année de référence
CA année de réf.
Effectif année de réf.

A partir d’une liste de numéro Siren, le premier programme permet de collecter le code source des pages web des sites verif.com et societe.com contenant les informations recherchées :
Societe.com : https://www.societe.com/cgi-bin/search?champs={}
Verif.com : https://www.verif.com/imprimer/{}/1/0/
Chaque page web collectée est enregistrée dans un fichier .text spécifique.

Un deuxième programme python permet d’aller chercher les informations pertinentes dans chaque page enregistrée et de les enregistrer dans une liste appelée BDD qui est sauvegardée sous format csv et pickle.Les informations extraites sont localisées avec deux solutions : les expressions régulières (module re) et BeautifulSoup.

Enfin, un troisième programme permet de transformer la liste des informations extraites en dataFrame pandas, puis de fusionner les deux dataFrames à partir de la variable ‘siren’ qui est commune aux 2 bases.A partir de ce nouveau dataFrame, quelques statistiques descriptives et quelques graphiques sont réalisés avec les modules pandas et matplotlib.
