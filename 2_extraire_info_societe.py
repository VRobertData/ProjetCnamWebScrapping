import re
import pdb
import csv
from bs4 import BeautifulSoup
import pickle
import datetime


# je créée une BDD qui sera une liste de record
BDD=[]

with open('siren_test.txt','r',encoding='utf8') as infile:
        fichier_siren=infile.read().split("\n")
        #fichier_siren=['315065292']
        
        for siren in fichier_siren:
            #pour chaque siren, je créée un dictionnaire qui aura plusieurs clés et valeurs
            record={}
            record['siren']=siren
            
            with open('Fichiers_societe\Fichier_S_'+siren+'.txt','r',encoding='utf8') as infile:
                html = infile.read()

                bs=BeautifulSoup(html,'html.parser')


                #tableau renseignements juridiques
                table=bs.find("table",{'id':{"rensjur"}})

                if table!= None:
              
                    #lignes du tableau
                    data = []
                    for lig,tr in enumerate(table.findAll('tr')):
                        #print(lig,'tr=',tr)

                        row=[]
                        for td in tr.findAll('td'):
                            row.append(td.get_text())
                        if len(row)>0:
                            data.append(row)


                    #récupérer date de création et créer une variable age de l'entreprise
                    CD='pb de date'
                    for row in data:
                        if row[0] == "Date création entreprise":
                            pattern_CD='(?s)\n                (.{1,10})\n                \n                 - \n                    \n                    \n'
                            Result_CD=re.findall(pattern_CD,row[1])
                            if len(Result_CD)==1:
                                CD=Result_CD[0]
                                CD_date=datetime.datetime.strptime(CD, '%d-%m-%Y')
                                jour=CD_date.now()
                                age=jour-CD_date
                                age=round(age.days/365)
                                #print(age)
                            else:
                                CD,age='',''
                                
                    
                else:
                    CD,age = '',''

                record['date creation']=CD
                record['age']=age

                BDD.append(record)
                
      
#enregistrer BDD dans un fichier pickle
with open('Fichiers_societe\BDD_societe','wb') as output:
    pickle.dump(BDD,output)
         

#enregistrer liste BDD dans un fichier csv
with open('Fichiers_societe\BDD_societe.csv','w') as outfile:
    writer=csv.writer(outfile,delimiter=";",lineterminator='\n')
    writer.writerow(['siren','date creation','age'])
    for record in BDD:
        writer.writerow([record['siren'],record['date creation'],record['age']])
    
       

