# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 18:15:19 2018

@author: Anaelle
"""
# Import des librairies:
import os
from lxml import etree
import re
import json
from collections import Counter
import pandas as pd
#from collections import Counter
import matplotlib.pyplot as plt

###############################################################################
########## Conversion en wtc 
###############################################################################

# import du fichier de metadonnees
path = "F:/MIASHS/UEs/text_analysis/projet/now_corpus/text_parse/metadata.txt"
metadata = json.load(open(path))

# Chemin vers les xml output:
path = "F:/MIASHS/UEs/text_analysis/projet/now_corpus/sortie_stanford/"

# Liste des articles:
os.chdir(path)
laListe = os.listdir()

# Tableau des sentiments et des locations : 
locSenti = pd.DataFrame(columns=['idArticle','country','location','sentiment'])

articleSANSmetadata = 0
articleOK = 0
idToken = 0
lindexOK = []

corpusTotal=''
idp=0
ids=0    
for xml in laListe:# laListe contient les articles 
    article=''
    listeLocation=[]
    
    # recupere metadata de l'article
    lindex = re.search('^(.+?)\.',xml).group(1)
    if any(lindex in s for s in list(metadata.keys())):
        articleOK +=1
        lindexOK.append(lindex)
        
        article+='</text>\n'
        article+='<text id="'+ lindex+'" nbwords="'+metadata[lindex]['#words']+'" country="'+metadata[lindex]['country']+'" date="'+metadata[lindex]['date']+'" title="'+metadata[lindex]['title']+'" url="'+metadata[lindex]['url']+'" website="'+metadata[lindex]['website']+'">\n'
    
        # recupere info du xml
        listeWord = []
        listeLemma = []
        listePOS = []
        listeNER = []
        listeSentimentSub = []
        
        tree = etree.parse(xml)
        for token in tree.xpath(".//token"):
            listItem = []
            for item in token:
                if item.tag == 'word':
                    listeWord.append(item.text)
                    listItem.append('word')
                if item.tag == 'lemma':
                    listeLemma.append(item.text)
                    listItem.append('lemma')
                if item.tag == 'POS':
                    listePOS.append(item.text)
                    listItem.append('POS')
                if item.tag == 'NER':
                    listeNER.append(item.text)
                    listItem.append('NER')
                if item.tag == 'sentiment':
                    listeSentimentSub.append(item.text)  
                    listItem.append('sentiment')
            if 'word' not in listItem:
                listeWord.append("NULL")
            if 'lemma' not in listItem:
                listeLemma.append("NULL")
            if 'POS' not in listItem:
                listePOS.append("NULL")
            if 'NER' not in listItem:
                listeNER.append("NULL")
            if 'sentiment' not in listItem:
                listeSentimentSub.append("NULL")
        
        sentiSentence=[] # liste des sentiments de la phrase                      
        for i in range(0,len(listeWord)):
            if listeWord[i] == "<h>":
                idp+=1
                article+='<p id="'+str(idp)+'" type="title">\n'
                ids+=1
                article+='<s id="'+str(ids)+'" sentiment="toReplace">\n'
            elif listeWord[i] == "<p>":
                idp+=1
                article+='<p id="'+str(idp)+'">\n'
                ids+=1
                article+='<s id="'+str(ids)+'" sentiment="toReplace">\n'
            elif listeWord[i] =="<":
                article+=''
            elif listeWord[i] =="\\":
                article+=''
            elif listeWord[i] =="p":
                article+='</p>\n'
            elif listeWord[i] =="h":
                article+='</p>\n'
            elif listeWord[i] ==">":
                article+=''
            elif listeWord[i] ==" ":
                article+=''
            elif listeWord[i] =="":
                article+=''
                
            elif listeWord[i] ==".":
                idToken+=1
                article+=listeWord[i]+'\t'+listeLemma[i]+'\t'+listePOS[i]+'\t'+listeNER[i]+'\t'+listeSentimentSub[i]+'\t'+str(idToken)+'\n'
                article+='</s>\n'

                # Sentiment global de la phrase
                if Counter(sentiSentence)['Positive'] > Counter(sentiSentence)['Negative']:
                    article = article.replace("toReplace", "Positive")
                elif Counter(sentiSentence)['Negative'] > Counter(sentiSentence)['Positive']:
                    article = article.replace("toReplace", "Negative")
                else:
                    article = article.replace("toReplace", "Neutral")
                sentiSentence=[]
                
                # Ajout début de phrase si pas <h> ou <p> ensuite
                if "<" not in listeWord[i:i+5]:
                    ids+=1
                    article+='<s id="'+str(ids)+'" sentiment="toReplace">\n'
            
            # Pour tous les mots : 
            else:
                idToken+=1
                article+=listeWord[i]+'\t'+listeLemma[i]+'\t'+listePOS[i]+'\t'+listeNER[i]+'\t'+listeSentimentSub[i]+'\t'+str(idToken)+'\n'
                sentiSentence.append(listeSentimentSub[i])
                # Pour les localisations
                loc = ''
                if listeNER[i] == "LOCATION":
                    loc = listeWord[i]
                    if listeNER[i+1] == "LOCATION":
                        loc = listeWord[i]+" "+listeWord[i+1]
                        if listeNER[i+2] == "LOCATION":
                            loc = listeWord[i]+" "+listeWord[i+1]+" "+listeWord[i+2]
                    elif listeNER[i-1] == "LOCATION":
                        loc = ""
                if loc != "":        
                    listeLocation.append(loc)
              
        corpusTotal += article
        
        # On rempli le tableau:
        sentiArticle ='Neutral'
        if Counter(listeSentimentSub)['Positive'] > Counter(listeSentimentSub)['Negative']:
            sentiArticle ='Positive'
        elif Counter(listeSentimentSub)['Negative'] > Counter(listeSentimentSub)['Positive']:
            sentiArticle = 'Negative'
        
        for k in set(listeLocation): # On prend uniquement une occurence de localisation par article!
            locSenti.loc[len(locSenti)] = [lindex,metadata[lindex]['country'],k,sentiArticle]

    else:
        articleSANSmetadata +=1
        print(lindex + " : pas de métadata ?!")

# Enregistrer corpus total
with open('corpusTotal.wtc', 'wb') as the_file:
    the_file.write(corpusTotal.encode("utf-8"))
# Enregistrer tableau    
locSenti.to_csv('locSenti.csv')



###############################################################################
########## Numerique / Stats
###############################################################################

##  Infos numériques :
articleOK # 2863
idToken # 2 073 734 tokens
articleSANSmetadata # 52
 


##### pour les metadatas :

# plot du nombre d'articles par pays
listePays=[]
for i in metadata.keys():
    if i in lindexOK:
        listePays.append(metadata[i]['country'])
    
listePaysDic=Counter(listePays)  
plt.bar(range(len(listePaysDic)), listePaysDic.values(), align="center")
plt.xticks(range(len(listePaysDic)), list(listePaysDic.keys()))
    
# plot du nombre d'articles par magazine
listeSites=[]
for i in metadata.keys():
    listeSites.append(metadata[i]['website'])
    
listeSitesDic=Counter(listeSites)  
plt.bar(range(len(listeSitesDic)), listeSitesDic.values(), align="center")
plt.xticks(range(len(listeSitesDic)), list(listeSitesDic.keys()))   

# plot du nombre de site par pays
listePaysSites={}
for i in metadata.keys():
    if i in lindexOK:
        if metadata[i]['country'] not in listePaysSites:
            listePaysSites[metadata[i]['country']]=[metadata[i]['website']]
        else:
            if metadata[i]['website'] not in listePaysSites[metadata[i]['country']]:
                listePaysSites[metadata[i]['country']].append(metadata[i]['website'])

for key, value in listePaysSites.items():
    print(key, len([item for item in value if item]))


