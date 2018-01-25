# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 18:15:19 2018

@author: Anaelle
"""
# Import des librairies:
import os
import subprocess as sp

# Chemin vers les articles:
path = "F:/MIASHS/UEs/text_analysis/ActuMap_data/corpus4/"
os.chdir(path)

# Liste des articles:
laListe = os.listdir()

# Liste des articles avec le chemin en entier
laListeOK=[]
for l in laListe:
    laListeOK.append(path+l)

# Lancer Standord pour chaque texte :
# Attention bien placer Python ou Spyder dans le dossier de Stanford corenlp !
for l in laListeOK:
    toRun = 'java -cp "*" -Xmx1g edu.stanford.nlp.pipeline.StanfordCoreNLP -props samplePropsFr.properties -file '+l+' -outputDirectory output'
    sp.run(toRun)
# Les fichiers sont enregistrés dans le dossier output