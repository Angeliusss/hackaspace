import tkinter as tk
from tkinter import ttk
import os
import subprocess
from PIL import Image, ImageTk

"""
Ce script crée une interface utilisateur avec tkinter qui permet à
l'utilisateur de sélectionner des fichiers à partir de deux listes déroulantes.
Ces listes déroulantes sont remplies avec les noms des fichiers contenus dans
deux dossiers spécifiques. L'utilisateur peut sélectionner un fichier de
chaque liste déroulante. Si les fichiers sélectionnés ont le même préfixe
(c'est-à-dire la partie du nom du fichier avant le premier caractère de
 soulignement), alors un bouton "Confirmer la sélection" est affiché.
En cliquant sur ce bouton, les noms des fichiers sélectionnés sont enregistrés
dans un fichier texte, l'application courante est fermée, et un autre
script Python est exécuté.
"""

# =============================================================================

# Initialiser l'application
app = tk.Tk()

# Nommer le projet
app.title('projet_etoile_python_test_01')

# Définir la taille de la fenêtre
app.geometry('800x600')

#
img_path = "images/galaxy.png"
bg_image = Image.open(img_path)
bg_image = bg_image.resize((800, 600), Image.ANTIALIAS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(app, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# =============================================================================


def confirm_and_run_new_script():
    """
    Récupère les noms de fichiers sélectionnés à partir des combobox,
    enregistre ces noms dans un fichier texte,
    ferme l'application courante,
    et exécute un autre script.
    """

    # Récupérer les noms de fichiers sélectionnés
    selection_A = combo_A.get()
    selection_B = combo_B.get()

    # Créer le fichier et écrire les noms de fichiers
    with open("fichiers_selectionnes.txt", "w") as f:
        f.write(f"{selection_A}\n{selection_B}\n")

    # Fermer l'application courante
    app.destroy()

    # Exécuter le script test02.py
    subprocess.run(["python3", "test02.py"])

# =============================================================================


# Fonction pour afficher la valeur sélectionnée et vérifier les préfixes
def show_selection():
    """
    Affiche les noms de fichiers sélectionnés,
    vérifie si les préfixes de ces noms sont identiques,
    et montre ou cache le bouton de confirmation en conséquence.
    """

    selection_A = combo_A.get()
    selection_B = combo_B.get()
    prefix_A = selection_A.split('_')[0]
    prefix_B = selection_B.split('_')[0]
    if prefix_A == prefix_B:
        label_A['text'] = selection_A
        label_B['text'] = selection_B

        # Afficher le bouton "Confirmer"
        confirm_button.pack()
    else:
        label_A['text'] = ""
        label_B['text'] = ""

        # Cacher le bouton "Confirmer"
        confirm_button.pack_forget()

# =============================================================================


# Les noms des dossiers
dossier_A = 'dossier_fichiers_A'
dossier_B = 'dossier_fichiers_B'

# Récupérer les noms des fichiers dans les dossiers
fichiers_A = os.listdir(dossier_A)
fichiers_B = os.listdir(dossier_B)

# Créer le tableau
tableau = ttk.Treeview(app, columns=('Dossier A', 'Dossier B'), show='headings')
tableau.column('Dossier A', width=400)
tableau.column('Dossier B', width=400)
tableau.heading('Dossier A', text=dossier_A)
tableau.heading('Dossier B', text=dossier_B)

# Ajouter les fichiers au tableau
for fichier_A, fichier_B in zip(fichiers_A, fichiers_B):
    tableau.insert('', 'end', values=(fichier_A, fichier_B))

# Afficher le tableau
tableau.pack()

# Créer la liste déroulante pour le dossier A
combo_A = ttk.Combobox(app, values=fichiers_A)
combo_A.pack()
combo_A.bind("<<ComboboxSelected>>", lambda _: show_selection())

# Créer la liste déroulante pour le dossier B
combo_B = ttk.Combobox(app, values=fichiers_B)
combo_B.pack()
combo_B.bind("<<ComboboxSelected>>", lambda _: show_selection())

# Bouton pour confirmer la sélection
confirm_button = tk.Button(app, text="Confirmer la sélection",
                           command=confirm_and_run_new_script,
                           bg = "#9bffff",
                           fg = "black")

# Labels pour afficher la sélection
label_A = tk.Label(app, text="")
label_A.pack()

label_B = tk.Label(app, text="")
label_B.pack()

# Boucle principale pour l'application
app.mainloop()
