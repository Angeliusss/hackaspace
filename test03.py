import tkinter as tk
from tkinter import ttk
import os
import subprocess
import json
import pandas as pd
import numpy as np
import collections

# Initialiser l'application
app = tk.Tk()

# Nommer le projet
app.title('projet_etoile_python_test_01_script_03')

# Définir la taille de la fenêtre
app.geometry('1200x600')

# =============================================================================


def on_slider_changed(value):
    """
    Cette fonction est appelée lorsqu'une valeur sur le curseur change.
    Elle met à jour la valeur de la 
    colonne E et la couleur de la ligne dans le tableau en fonction de la
    nouvelle valeur du curseur.
    """

    """
    selected_item semble être utilisé pour stocker l'élément actuellement
    sélectionné dans une interface utilisateur. Il est utilisé dans plusieurs
    fonctions, donc il a été défini comme une variable globale afin que ces
    fonctions puissent partager cette information.
    """
    global selected_item

    # Ignore if no row is selected
    if selected_item is None:
        return

    # Get the value in column D
    val_B = tree.set(selected_item, '#4')

    # Convert the value to float and check if it's a number
    try:
        val_B = float(val_B)
        is_num = True
    except ValueError:
        is_num = False

    if is_num:
        # Convert slider value to float
        val_A = float(value)

        # Compute the new result
        resultat = processus_methode(val_A, val_B)

        # Update column E with the new result
        tree.set(selected_item, '#5', resultat)

        # Update row color based on the new result
        update_row_color_based_on_result(selected_item, resultat)

# =============================================================================


def update_row_color_based_on_result(item, result):
    """
    Met à jour la couleur d'une ligne du tableau en fonction d'un résultat
    donné. Les lignes avec un 
    résultat supérieur au seuil sont marquées en haut, celles avec un
    résultat inférieur au seuil sont 
    marquées en bas, et toutes les autres sont marquées au milieu.
    """

    if result > seuil:  # seuil est le seuil que vous avez défini
        tree.item(item, tags=('high',))
    elif result < seuil:
        tree.item(item, tags=('low',))
    else:
        tree.item(item, tags=('medium',))

# =============================================================================


def is_number(n):
    """
    Vérifie si un certain objet est un nombre.
    """

    return isinstance(n, (int, float, complex))

# =============================================================================


def processus_methode(val_A, val_B):
    """
    Cette fonction effectue un calcul sur deux valeurs données. Si les deux
    valeurs sont numériques et 
    que la seconde valeur n'est pas égale à zéro, le calcul est effectué.
    Sinon, la première valeur est 
    retournée.
    """

    # vérifie si les deux valeurs sont numériques
    if is_number(val_A) and is_number(val_B) and val_B != 0:
        return abs(np.subtract(val_A, val_B)) / val_B
    else:
        return val_A  # conserve la valeur non numérique

# =============================================================================


def read_json_file(file_path):
    """
    Ouvre un fichier JSON, le lit et le convertit en une liste de
    DataFrames pandas.
    """

    with open(file_path, 'r') as file:
        json_data = json.load(file, object_pairs_hook=collections.OrderedDict)

    # Convertir chaque dictionnaire en DataFrame
    dfs = [pd.DataFrame.from_dict(data, orient='index', columns=['value']) for data in json_data]

    return dfs

# =============================================================================


def restart_process():
    """
    Ferme l'application courante et exécute un autre script.
    """

    # Fermer l'application courante
    app.destroy()

    # Exécuter le script test01.py
    subprocess.run(["python3", "test01.py"])

# =============================================================================


def on_tree_click(event):
    """
    Cette fonction est appelée lorsqu'un utilisateur clique sur une ligne
    du tableau. Elle vérifie si le 
    clic a été fait sur la troisième colonne, et si c'est le cas,
    elle récupère les valeurs des colonnes B 
    et D. Si aucune de ces valeurs n'est numérique, le curseur est affiché.
    """

    """
    selected_item semble être utilisé pour stocker l'élément actuellement
    sélectionné dans une interface utilisateur. Il est utilisé dans plusieurs
    fonctions, donc il a été défini comme une variable globale afin que ces
    fonctions puissent partager cette information.
    """
    global selected_item

    # get the coordinates of the mouse click
    x, y, widget = event.x, event.y, event.widget
    selected_item = widget.identify('item', x, y)
    column = widget.identify('column', x, y)

    # check if the click was on the third column
    if column == '#3':
        # if so, get the values of columns B and D
        val_A = widget.set(selected_item, '#2')
        val_B = widget.set(selected_item, '#4')

        # if neither value is numeric, show the slider
        if not (is_number(val_A) or is_number(val_B)):
            slider.place(x=x, y=y)

# =============================================================================


# Créer un Treeview
tree = ttk.Treeview(app, columns=("A", "B", "C", "D", "E"), show="headings")

#
selected_item = None

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

# dictionnaire json vide
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
tree.heading("E", text="Resultat")

tree.tag_configure('high', background='red')
tree.tag_configure('medium', background='yellow')
tree.tag_configure('low', background='green')

# Ajouter des données (à remplacer par les données de votre DataFrame)
for idx, (index, row) in enumerate(pd.concat(dataframes, axis=1).iterrows()):
    val_A = row[0]  # obtenir la valeur de la clé dans le fichier A
    val_B = row[1]  # obtenir la valeur de la clé dans le fichier B
    resultat = processus_methode(val_A, val_B)

    # Modifier la couleur de fond selon l'index de la ligne
    tree.insert("", "end", values=(index, val_A, "", val_B, resultat), tags = ('oddrow' if idx % 2 == 0 else 'evenrow',))

# Créer le widget slider
"""
La raison de l'underscore après from dans from_=0 est que from est un mot-clé
réservé en Python. Les mots-clés sont des mots spéciaux que le
compilateur/interpréteur Python reconnaît et qui ont une signification
spécifique dans le langage. Pour éviter les conflits avec ce mot-clé réservé,
un underscore est ajouté à la fin de from
"""
slider = tk.Scale(app, from_=0, to=100, orient='horizontal', command=on_slider_changed)
slider.place(x=300, y=300)  # Initial placement (not visible)

# Cacher le slider au début
slider.place_forget()


# Bind the click event to the handler
tree.bind('<Button-1>', on_tree_click)

# Définir les couleurs de fond
tree.tag_configure('oddrow', background='light gray')
tree.tag_configure('evenrow', background='white')

# Créer les bordures de chaque ligne et de chaque colonne
# cache la colonne vide à l'extrême gauche
tree["show"] = "headings"

#
button = tk.Button(app, text="Restart", command=restart_process)

# Placer le bouton à une position appropriée
button.place(x=1050, y=300)

#
quit_button = tk.Button(app, text="Quit", command=app.destroy)

# Placer le bouton à une position appropriée
quit_button.place(x=1050, y=350)

# =============================================================================

# Afficher le Treeview
tree.place(x=0, y=0, width=1000, height=700)


# Boucle principale pour l'application
app.mainloop()
