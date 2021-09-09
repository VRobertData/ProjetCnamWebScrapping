# -*- coding: utf8 -*-
import requests
import pdb
import html




with open('siren_test.txt','r',encoding='utf8') as infile:
        fichier_siren=infile.read().split("\n")
        #fichier_siren = ['808332670']
        #print(fichier_siren)

for siren in fichier_siren:
        url='https://www.verif.com/imprimer/{}/1/0/'.format(siren)
        request_headers={'User-Agent': "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6" }
        req=requests.get(url,headers=request_headers,timeout=10)
        
        #print(req.status_code)
        
        contenu = html.unescape(req.text)
        #print(len(contenu), siren)

        #Gestion des erreurs
        if req.status_code ==requests.codes.ok and len(contenu)>20000:
                with open('Fichiers_verif\Fichier_'+siren+'.txt','w',encoding='utf8') as mon_fichier:
                        mon_fichier.write(contenu)
        else:
                print('siren : ',siren, 'HTTPError : ',req.raise_for_status(), 'len :',len(contenu))
                        
print('end')

