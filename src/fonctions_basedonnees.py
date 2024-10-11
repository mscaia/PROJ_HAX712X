import csv 
import matplotlib.pyplot as plt 
import numpy as np 

#importer les données 
filename1= 'MMM_MMM_GeolocCompteurs.csv'
filename2='TAM_MMM_CoursesVelomagg.csv'

#Fonction qui donne le colonne i du tableau voulu: 
def colonne(i, w_file):
    L=[]
    with open(w_file) as f:
        for line in f:
            x=line.split(";")
            L.append(x[i])
    return L         

#Fonction qui retourne toutes les valeurs dans la colonne j quand l'argument de la colonne i est k 
def arg(k,i,j, w_file):
    L=[]
    with open(w_file) as f:
        for line in f:
            x=line.split(";")
            if x[i]==k:
                L.append(x[j])
    return L 
