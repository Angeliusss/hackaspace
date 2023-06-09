import tkinter as tk
from tkinter import ttk
import os
import subprocess

# Initialiser l'application
app = tk.Tk()

# Nommer le projet
app.title('projet_etoile_python_test_01')

# Définir la taille de la fenêtre
app.geometry('800x600')

def confirm_and_run_new_script():
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

# Fonction pour afficher la valeur sélectionnée et vérifier les préfixes
def show_selection():
    selection_A = combo_A.get()
    selection_B = combo_B.get()
    prefix_A = selection_A.split('_')[0]
    prefix_B = selection_B.split('_')[0]
    if prefix_A == prefix_B:
        label_A['text'] = selection_A
        label_B['text'] = selection_B
        confirm_button.pack()  # Afficher le bouton "Confirmer"
    else:
        label_A['text'] = ""
        label_B['text'] = ""
        confirm_button.pack_forget()  # Cacher le bouton "Confirmer"

# Bouton pour confirmer la sélection
# confirm_button = tk.Button(app, text="Confirmer la sélection", command=show_selection)
confirm_button = tk.Button(app, text="Confirmer la sélection", command=confirm_and_run_new_script)
#confirm_button.pack()  # Commenté pour le cacher initialement

# Labels pour afficher la sélection
label_A = tk.Label(app, text="")
label_A.pack()

label_B = tk.Label(app, text="")
label_B.pack()

# Boucle principale pour l'application
app.mainloop()
