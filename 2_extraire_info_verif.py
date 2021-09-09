import re
import pdb
import csv
from bs4 import BeautifulSoup
import pickle


# je créée une BDD qui sera une liste de record
BDD=[]

with open('siren_test.txt','r',encoding='utf8') as infile:
        fichier_siren=infile.read().split("\n")
        #fichier_siren=['325720720']
        
        for siren in fichier_siren:
            #pour chaque siren, je créée un dictionnaire qui aura plusieurs clés et valeurs
            record={}
            record['siren']=siren
            
            with open('Fichiers_verif\Fichier_'+siren+'.txt','r',encoding='utf8') as infile:
                html = infile.read()
                #pdb.set_trace()

                bs=BeautifulSoup(html,'html.parser')
                #pdb.set_trace()

                #Raison sociale
                pattern_RS='<td class="fiche_tdhead">Raison sociale</td>\n\n\t\t\t\t\t<td>(.+?(?=</td>))'
                Result_RS=re.findall(pattern_RS,html)
                if len(Result_RS)==1:
                    raison_sociale=Result_RS[0]
                else:
                    #print('pb RS',siren)
                    raison_sociale=''
                record['raison sociale']=raison_sociale


                #Code NAF
                pattern_NAF='<span id="verif_fiche.code.naf" >(.+?(?=</span>))'
                Result_NAF=re.findall(pattern_NAF,html)
                if len(Result_NAF)==1:
                    NAF=Result_NAF[0]
                else:
                    NAF=''
                record['code NAF']=NAF

                #Nom DG
                pattern_DG='<td class="fiche_tdhead">Directeur général</td>\n\n\t\t\t\t\t\t\t<td>(.+?(?=\xa0))'
                Result_DG=re.findall(pattern_DG,html)
                if len(Result_DG)==1:
                    DG=Result_DG[0]
                else:
                    DG=''
                record['Nom du DG']=DG

                #Nom DAF
                pattern_DAF='<td class="fiche_tdhead">Directeur administratif et financier</td>\n\n\t\t\t\t\t\t\t<td>(.+?(?=</td>))'
                Result_DAF=re.findall(pattern_DAF,html)
                if len(Result_DAF)==1:
                    DAF=Result_DAF[0]
                else:
                    DAF=''
                record['Nom du DAF']=DAF

                #Nom DF
                pattern_DF='<td class="fiche_tdhead">Directeur financier</td>\n\n\t\t\t\t\t\t\t<td>(.+?(?=</td>))'
                Result_DF=re.findall(pattern_DF,html)
                if len(Result_DF)==1:
                    DF=Result_DF[0]
                else:
                    DF=''
                record['Nom du DF']=DF

                

                #tableau de chiffres
                table=bs.find("table",{'class':{"table chiffres"}})

                if table!= None:
                    #en-tête
                    headers = []
                    thead = table.find('thead')
                    if thead != None:
                        headers=[]
                        tr = thead.find('tr')
                        if tr != None:
                            for th in tr.findAll('th'):
                                headers.append(th.get_text())
                                
                    year=headers[1].replace('\n','')

                    #lignes du tableau
                    data = []
                    table_body=table.find('tbody')

                    for lig,tr in enumerate(table_body.findAll('tr')):
                        #print(lig,'tr=',tr)

                        row=[]
                        for td in tr.findAll('td'):
                            row.append(td.get_text())
                        if len(row)>0:
                            data.append(row)

                    #récupérer CA et effectif de l'année la plus récente dans le tableau
                    CA='pb CA'
                    eff='pb eff'
                    for row in data:
                        if row[0] == "Chiffre d'affaires":
                            CA=row[1].replace('\xa0','').replace(' ','')
                        if row[0] == "Nombre d'employés":
                            eff=row[1].replace(' ','').replace('\xa0','')
                    

                else:
                    year,CA,eff = '','',''

                record['year']=year
                record['CA']=CA
                record['eff']=eff
                   

                BDD.append(record)
                
#enregistrer BDD dans un fichier pickle
with open('Fichiers_verif\BDD_verif','wb') as output:
    pickle.dump(BDD,output)
         

#enregistrer liste BDD dans un fichier csv
with open('Fichiers_verif\BDD_verif.csv','w') as outfile:
    writer=csv.writer(outfile,delimiter=";",lineterminator='\n')
    writer.writerow(['siren','raisonsociale','Code Naf','Nom du DG','Nom du DAF','Nom du D. Financier','Année',"Chiffres d'affaires","Nombre d'employés"])
    for record in BDD:
        writer.writerow([record['siren'],record['raison sociale'],record['code NAF'],record['Nom du DG'],record['Nom du DAF'],record['Nom du DF'],record['year'],record['CA'],record['eff']])
    

       

