
import tkinter as tk
from tkinter import ttk
import os
import subprocess
import json

# À noter qu'il y a un problème potentiel avec cette approche :
# si l'utilisateur change la sélection dans une des listes déroulantes
# après avoir sélectionné une valeur dans les deux, le bouton restera actif.
# Il serait préférable de vérifier à nouveau si une sélection a été faite
# dans les deux listes déroulantes à chaque fois que l'une d'entre
# elles change, mais cela rendrait le code un peu plus complexe.

# Initialiser l'application
app = tk.Tk()

# Nommer le projet
app.title('projet_etoile_python_test_01_script_02')

# Définir la taille de la fenêtre
app.geometry('1200x600')

#
fichier_A = tk.StringVar()
fichier_B = tk.StringVar()

# les labels qui affichent le nbre de dictionnaires
dict_count_label_A = tk.Label(app, text="")
dict_count_label_B = tk.Label(app, text="")

def comparer():
    # Récupérer les dictionnaires sélectionnés
    selection_A = combo_A.get()
    num_candidat_A = int(selection_A.split(" ")[-1]) - 1
    dict_A = liste_candidats_json_fichier_A[num_candidat_A]

    selection_B = combo_B.get()
    num_candidat_B = int(selection_B.split(" ")[-1]) - 1
    dict_B = liste_candidats_json_fichier_B[num_candidat_B]

    # Créer le fichier comparaison.json
    with open("comparaison.json", 'w') as file:
        file.write(json.dumps([dict_A, dict_B], indent=4))

    seuil = entry_def_seuil.get()
    pas = entry_def_pas.get()

    # concaténer les valeurs de seuil et pas avec un délimiteur (ici, un saut de ligne)
    data = seuil + ',' + pas

    with open("seuil.txt", 'w') as f:
        f.write(data)

    # Fermer la fenêtre et exécuter test03.py
    app.destroy()
    subprocess.run(["python3", "test03.py"])

def go_back():
    # Fermer l'application courante
    app.destroy()

    # Exécuter le script test01.py
    subprocess.run(["python3", "test01.py"])


liste_candidats_json_fichier_A = []
liste_candidats_json_fichier_B = []


def read_file_and_update_labels():

    with open("fichiers_selectionnes.txt", 'r') as file:
        lines = file.readlines()

        #
        fichier_A.set("dossier_fichiers_A/" + lines[0].strip())
        fichier_B.set("dossier_fichiers_B/" + lines[1].strip())

    # Affiche dans la console la valeur des deux variables "ficher_A" et "fichier_B"
    print("fichier_A: ", fichier_A.get())
    print("fichier_B: ", fichier_B.get())

    with open(fichier_A.get()) as json_data_fichier_A:
        data_fichier_A = json.load(json_data_fichier_A)
        for i, dict in enumerate(data_fichier_A, start=1):
            dict["candidat n° " + str(i)] = i
            liste_candidats_json_fichier_A.append(dict)

        # texte du label qui accompagne,
        # l'affichage du nbre de candidats par fichier
        dict_count_label_A['text'] = f"nbre de dictionnaire ds le fichier_A: {len(data_fichier_A)}"

        print(json.dumps(data_fichier_A, indent=4))

    with open(fichier_B.get()) as json_data_fichier_B:
        data_fichier_B = json.load(json_data_fichier_B)
        for i, dict in enumerate(data_fichier_B, start=1):
            dict["candidat n° " + str(i)] = i
            liste_candidats_json_fichier_B.append(dict)

        # texte du label qui accompagne,
        # l'affichage du nbre de candidats par fichier
        dict_count_label_B['text'] = f"nbre de dictionnaire ds le fichier_B: {len(data_fichier_B)}"

        print(json.dumps(data_fichier_B, indent=4))


# Bouton pour retourner au script test01.py
btn_retour = tk.Button(app, text="Retour", command=go_back)
btn_retour.pack()

# Créer le tableau
tableau = ttk.Treeview(app, columns=('Candidats du fichier A', 'Candidats du fichier B'), show='headings')
tableau.column('Candidats du fichier A', width=200)
tableau.column('Candidats du fichier B', width=200)
tableau.heading('Candidats du fichier A', text="Candidats du fichier A")
tableau.heading('Candidats du fichier B', text="Candidats du fichier B")

read_file_and_update_labels()


def update_text_area(event):
    # Récupérer la sélection
    selection = combo_A.get()
    # Récupérer le numéro du candidat
    num_candidat = int(selection.split(" ")[-1]) - 1  # Soustraire 1 car l'indexation commence à 0
    # Récupérer le dictionnaire du candidat
    candidat_dict = liste_candidats_json_fichier_A[num_candidat]

    # Créer la chaîne à afficher
    text_to_display = "\n".join([f"{key} => {value}" for key, value in candidat_dict.items()])

    # Mettre à jour le Text widget
    text_area_candidats_fichier_A.config(state='normal')
    text_area_candidats_fichier_A.delete(1.0, tk.END)  # Supprimer le contenu précédent
    text_area_candidats_fichier_A.insert(tk.END, text_to_display)  # Insérer le nouveau contenu
    text_area_candidats_fichier_A.config(state='disabled')

    #
    btn_comparer.config(state='normal')


def update_text_area_B(event):
    selection = combo_B.get()
    num_candidat = int(selection.split(" ")[-1]) - 1  # Soustraire 1 car l'indexation commence à 0
    candidat_dict = liste_candidats_json_fichier_B[num_candidat]
    text_to_display = "\n".join([f"{key} => {value}" for key, value in candidat_dict.items()])
    text_area_candidats_fichier_B.config(state='normal')
    text_area_candidats_fichier_B.delete(1.0, tk.END)  # Supprimer le contenu précédent
    text_area_candidats_fichier_B.insert(tk.END, text_to_display)  # Insérer le nouveau contenu
    text_area_candidats_fichier_B.config(state='disabled')

    #
    btn_comparer.config(state='normal')


# Créer la liste déroulante pour le dossier A
combo_A = ttk.Combobox(app, values=[f"candidat n° {i}" for i in range(1, len(liste_candidats_json_fichier_A) + 1)])
combo_A.bind("<<ComboboxSelected>>", update_text_area)  # Associer l'action à la sélection

# Créer la liste déroulante pour le dossier B
combo_B = ttk.Combobox(app, values=[f"candidat n° {i}" for i in range(1, len(liste_candidats_json_fichier_B) + 1)])
combo_B.bind("<<ComboboxSelected>>", update_text_area_B)  # Associer l'action à la sélection


#
btn_comparer = tk.Button(app, text="Comparer", state='disabled')

#
btn_comparer.config(command=comparer)

# Créer le Text widget pour afficher les paires clé => valeur du dictionnaire JSON
text_area_candidats_fichier_A = tk.Text(app, width=40, height=10, state='disabled')
scroll = tk.Scrollbar(app, command=text_area_candidats_fichier_A.yview)
text_area_candidats_fichier_A.configure(yscrollcommand=scroll.set)

text_area_candidats_fichier_B = tk.Text(app, width=40, height=10, state='disabled')
scroll_B = tk.Scrollbar(app, command=text_area_candidats_fichier_B.yview)
text_area_candidats_fichier_B.configure(yscrollcommand=scroll_B.set)

# Ajouter le Text widget et le Scrollbar à la fenêtre
text_area_candidats_fichier_A.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

text_area_candidats_fichier_B.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
scroll_B.pack(side=tk.RIGHT, fill=tk.Y)

# Effacer le fichier nommé fichiers_selectionnes.txt
os.remove("fichiers_selectionnes.txt")

# Ajouter les fichiers au tableau
for candidat_A, candidat_B in zip(liste_candidats_json_fichier_A, liste_candidats_json_fichier_B):
    tableau.insert('', 'end', values=(candidat_A["candidat n° " + str(liste_candidats_json_fichier_A.index(candidat_A) + 1)], 
                                      candidat_B["candidat n° " + str(liste_candidats_json_fichier_B.index(candidat_B) + 1)]))
# Afficher les labels
dict_count_label_A.pack()
dict_count_label_B.pack()

# Afficher le tableau
tableau.pack()

# Afficher les listes deroulantes
combo_A.pack()
combo_B.pack()

# Ajoutez ce code après la création de combo_B
seuil_label = tk.Label(app, text="Veuillez renseigner le seuil de référence")
seuil_label.pack()

entry_def_seuil = tk.Entry(app)  # Crée un champ d'entrée
entry_def_seuil.pack()  # Affiche le champ d'entrée dans l'interface utilisateur

# Ajoutez ce code après la création de combo_B
pas_label = tk.Label(app, text="Veuillez renseigner le pas de reference")
pas_label.pack()

entry_def_pas = tk.Entry(app)  # Crée un champ d'entrée
entry_def_pas.pack()  # Affiche le champ d'entrée dans l'interface utilisateur

#
btn_comparer.pack()

# Boucle principale pour l'application
app.mainloop()
