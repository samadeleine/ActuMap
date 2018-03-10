import os
import re
import codecs
import json


########### Séparation du texte en sous articles
os.chdir("F:/MIASHS/UEs/text_analysis/now_corpus/")

data = []
with open('text.txt', encoding="utf-8") as inputfile:
    for line in inputfile:
        data.append(line.strip())

for i in range(0,len(data)):
    # Récuperer l'id et le supprimer
    subcorpus_id = re.search('^@@(.+?) ',data[i]).group(1)
    text_modif = re.sub('@@.+? ',"",data[i])
    
    # Mettre des copyright à la place des @@@@@@
    text_modif = re.sub(' @ @ @ @ @ @ @ @ @ @',"<copyright><\copyright>",text_modif)

    line = ""
    before = ""
    # Rajouter </h>
    for j in range(0,len(text_modif)): # range ne prend pas le dernier
        if text_modif[j:j+2] =="<h" and before != "<h>": 
            before = "<h>"
            line+=text_modif[j]
        elif text_modif[j:j+2] =="<h" and before == "<h>": 
            before = "<h>"
            line+="<\h>"+text_modif[j]
        elif text_modif[j:j+2] =="<p" and before == "": 
            before = "<\p>"
            line+=text_modif[j]
        elif text_modif[j:j+2] =="<p" and before == "<h>": 
            before = "<\h>"
            line+="<\h>"+text_modif[j]
        elif text_modif[j:j+2] =="<p": 
            before = "<\p>"
            line+="<\p>"+text_modif[j]
        elif j==(len(text_modif)-1) and text_modif[j] !=">": 
            line+=text_modif[len(text_modif)-1]+"<\p>"         
        else:
            line+=text_modif[j]          
            
    completeName = os.path.join(os.getcwd()+"/text_parse/"+str(subcorpus_id)+".txt")
    file = open(completeName,"wb") 
    file.write(line.encode("utf-8"))            
    file.close()  


########### Travail sur les métadonnées
metadataBrut = []

with codecs.open('now-samples-sources.txt', "r",encoding='utf8', errors='ignore') as inputfile:
    for line in inputfile:
        metadataBrut.append(line.strip())

colonnes = ['textID', '#words', 'date', 'country', 'website', 'url', 'title']
            
metadata={}
for i in range(1,len(metadataBrut)):
    line = metadataBrut[i]
    lineSplit = line.split('\t')
    metadata[lineSplit[0]]={colonnes[1]:lineSplit[1],colonnes[2]:lineSplit[2],colonnes[3]:lineSplit[3],
            colonnes[4]:lineSplit[4],colonnes[5]:lineSplit[5],colonnes[6]:lineSplit[6]}

metadataName = os.path.join(os.getcwd()+"/text_parse/metadata.txt")
metadata = json.dumps(metadata)
file = open(metadataName,"wb") 
file.write(metadata.encode("utf-8"))            
file.close() 