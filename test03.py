import tkinter as tk
from tkinter import ttk
import os
import subprocess
import json
import pandas as pd
from pandastable import Table
import numpy as np
import collections

# Initialiser l'application
app = tk.Tk()

# Nommer le projet
app.title('projet_etoile_python_test_01_script_03')

# Définir la taille de la fenêtre
app.geometry('1200x600')

# Créer un Treeview
tree = ttk.Treeview(app, columns=("A", "B", "C", "D", "E"), show="headings")


#
def is_number(n):
    return isinstance(n, (int, float, complex))

# fonction qui exécute le calcul
def processus_methode(val_A, val_B):
    # vérifie si les deux valeurs sont numériques
    if is_number(val_A) and is_number(val_B) and val_B != 0:
        return abs(np.subtract(val_A, val_B)) / val_B
    else:
        return val_A  # conserve la valeur non numérique

def read_json_file(file_path):

    with open(file_path, 'r') as file:
        json_data = json.load(file, object_pairs_hook=collections.OrderedDict)

    # Convertir chaque dictionnaire en DataFrame
    dfs = [pd.DataFrame.from_dict(data, orient='index', columns=['value']) for data in json_data]

    return dfs


def restart_process():
    # Fermer l'application courante
    app.destroy()

    # Exécuter le script test01.py
    subprocess.run(["python3", "test01.py"])


# obtenir le contenu du fichier comparaison.json
dataframes = read_json_file("comparaison.json")

# obtenir la valeur "seuil" depuis le fichier txt
with open("seuil.txt", 'r') as f:
    line = f.read().strip()

# séparer la ligne en utilisant la virgule comme délimiteur
seuil, pas = line.split(',')

# Convertir les valeurs en nombre si nécessaire
seuil = float(seuil)
pas = float(pas)

# effacer le fichier "seuil".txt
os.remove("seuil.txt")

# effacer le fichier comparaison.json
os.remove("comparaison.json")



# =============================================================================

#
dict_resultat = {}

# Créer les titres des colonnes
tree.column("A", width=200, anchor="w", stretch=False)
tree.column("B", width=200, anchor="w", stretch=False)
tree.column("C", width=200, anchor="w", stretch=False)
tree.column("D", width=200, anchor="w", stretch=False)
tree.column("E", width=200, anchor="w", stretch=False)

tree.heading("A", text="")
tree.heading("B", text="Candidat_fichier_A")
tree.heading("C", text="Modifiez vos valeurs")
tree.heading("D", text="Candidat_fichier_B")
tree.heading("E", text="Résultat")

# Ajouter des données (à remplacer par les données de votre DataFrame)
for idx, (index, row) in enumerate(pd.concat(dataframes, axis=1).iterrows()):
    val_A = row[0]  # obtenir la valeur de la clé dans le fichier A
    val_B = row[1]  # obtenir la valeur de la clé dans le fichier B
    resultat = processus_methode(val_A, val_B)

    # Modifier la couleur de fond selon l'index de la ligne
    tree.insert("", "end", values=(index, val_A, "", val_B, resultat), tags = ('oddrow' if idx % 2 == 0 else 'evenrow',))

# Créer le widget slider
slider = tk.Scale(app, from_=0, to=100, orient='horizontal')
slider.place(x=300, y=300)  # Initial placement (not visible)

# Cacher le slider au début
slider.place_forget()

def on_tree_click(event):
    # get the coordinates of the mouse click
    x, y, widget = event.x, event.y, event.widget
    elem = widget.identify('item', x, y)
    column = widget.identify('column', x, y)

    # check if the click was on the third column
    if column == '#3':
        # if so, get the values of columns B and D
        val_A = widget.set(elem, '#2')
        val_B = widget.set(elem, '#4')

        # if neither value is numeric, show the slider
        if not (is_number(val_A) or is_number(val_B)):
            slider.place(x=x, y=y)

# Bind the click event to the handler
tree.bind('<Button-1>', on_tree_click)

# Définir les couleurs de fond
tree.tag_configure('oddrow', background='light gray')
tree.tag_configure('evenrow', background='white')

# Créer les bordures de chaque ligne et de chaque colonne
tree["show"] = "headings" # cache la colonne vide à l'extrême gauche

# =============================================================================

# Afficher le Treeview
tree.place(x=0, y=0, width=1000, height=700)


# Boucle principale pour l'application
app.mainloop()
