# -*- coding: utf8 -*-
import requests
import re
import pdb
import html
import csv
import time
import random


with open('siren_test.txt','r',encoding='utf8') as infile:
        fichier_siren=infile.read().split("\n")
        #fichier_siren = ['403335938']
        print(fichier_siren)

for siren in fichier_siren:
        
        url='https://www.societe.com/cgi-bin/search?champs={}'.format(siren)
        request_headers={'User-Agent': "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6" }
        req=requests.get(url,headers=request_headers,timeout=10)
        
        print(req.status_code)
        
        
        contenu = html.unescape(req.text)
        #print(len(contenu), siren)

        #Gestion des erreurs
        if req.status_code ==requests.codes.ok and len(contenu)>100000:
                with open('Fichiers_societe\Fichier_S_'+siren+'.txt','w',encoding='utf8') as mon_fichier:
                        mon_fichier.write(contenu)
        else:
                print('siren : ',siren, 'HTTPError : ',req.raise_for_status(), 'len :',len(contenu))
                        
print('end')

