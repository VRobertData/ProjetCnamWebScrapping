import pickle
import matplotlib.pyplot as plt
import pandas as pd

with open('Fichiers_verif\BDD_verif','rb') as output:
    BDD_V=pickle.load(output)

with open('Fichiers_societe\BDD_societe','rb') as output:
    BDD_S=pickle.load(output)


#Tranformer les 2 BDD en dataframe pandas
dfV=pd.DataFrame(BDD_V)
dfS=pd.DataFrame(BDD_S)


#Joindre les 2 dataframes à partir du siren
df=dfS.merge(dfV,how='left', left_on=['siren'], right_on=['siren'], indicator=True)

#convertir les colonnes CA et Eff en int ou float
df[['CA','eff','age']]=df[['CA','eff','age']].apply(pd.to_numeric)

#supprimer les lignes avec valeurs manquantes
df=df.dropna()


#Moyenne CA, age des entreprises, effectif
A=df['CA'].describe()
CA_moyen=round(A['mean'])
nbA=round(A['count'])

B=df['eff'].describe()
eff_moyen=round(B['mean'])

C=df['age'].describe()
age_moyen=round(C['mean'])

print('Pour ',nbA,'entreprises :','\n','le CA moyen est de ',CA_moyen,'euros','\n',"l'effectif moyen est de ",eff_moyen,'employés','\n',"l'âge moyen des entreprises est de ",age_moyen,'ans')

#graphiques CA
plt.style.use('ggplot')

df_CA=df.sort_values(by=['CA'],ascending=False)
df_CA.plot(x='raison sociale',y=['CA'], figsize=(12,5), kind="bar", stacked=True)
plt.show()

#graphique CA et effectif
x=df['raison sociale']
y1=df_CA['CA']
y2=df_CA['eff']

fig, ax1 = plt.subplots()
ax2=ax1.twinx()
ax1.plot(x,y1, 'g-')
ax2.plot(x,y2, 'b-')

ax1.set_xlabel('raison sociale')
ax1.set_ylabel('CA', color='g')
ax2.set_ylabel('eff', color='g')
plt.show()

#graphiques boxplot
boxplotCA=df.boxplot(['CA'])
boxplotCA.plot()
plt.show()

boxplotage=df.boxplot(['age'])
boxplotage.plot()
plt.show()

boxploteff=df.boxplot(['eff'])
boxploteff.plot()
plt.show()
