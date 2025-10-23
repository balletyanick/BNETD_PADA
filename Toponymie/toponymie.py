import tkinter as tk
from tkinter import  ttk
from tkinter import messagebox
from datetime import date
import psycopg2


def submit_client():
    # Récupérer les valeurs saisies dans les champs du formulaire
    numero = entry_numero.get().strip()
    id_voie_siga = entry_id.get().strip()
    commune = entry_commune.get().strip()
    nom_toponyme = entry_nom_toponyme.get().strip()
    statut = entry_statut.get().strip()
    nom_pada = entry_nom_pada.get().strip()
    typologie = entry_typologie.get().strip()
    etat = entry_etat.get().strip()
    description = entry_desc.get("1.0", tk.END).strip()

    # Obtenir la date actuelle
    current_date = date.today()

    # Connexion à la base de données PostgreSQL
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="Cadr@20$24!",
            host="10.128.3.34",
            port="5432",
            database="pada_toponyme"
        )

        # Création d'un curseur
        cursor = connection.cursor()

        # Préparer la requête de mise à jour dynamique
        update_query = "UPDATE toponyme.topo_pada SET "
        update_values = []

        if commune:
            update_query += "commune = %s, "
            update_values.append(commune)
        if nom_toponyme:
            update_query += "nom_toponyme = %s, "
            update_values.append(nom_toponyme)
        else:
            update_query += "nom_toponyme = NULL, "
        if nom_pada:
            update_query += "nom_pada = %s, "
            update_values.append(nom_pada)
        else:
            update_query += "nom_pada = NULL, "
        if etat:
            update_query += "etat = %s, "
            update_values.append(etat)
        if typologie:
            update_query += "typologie = %s, "
            update_values.append(typologie)
        if statut:
            update_query += "statut = %s, "
            update_values.append(statut)
        if description:
            update_query += "description = %s, date = %s, "
            update_values.append(description)
            update_values.append(current_date)
        else:
            update_query += "description = NULL, date = %s, "
            update_values.append(current_date)

        # Enlever la dernière virgule et ajouter la condition WHERE
        update_query = update_query.rstrip(', ') + " WHERE id_voie_siga = %s"
        update_values.append(id_voie_siga)

        # Exécuter la requête de mise à jour
        cursor.execute(update_query, tuple(update_values))
        connection.commit()

        # Vider les champs après succès
        entry_id.delete(0, 'end')
        entry_commune.delete(0, 'end')
        entry_nom_pada.delete(0, 'end')
        entry_etat.set('')
        entry_nom_toponyme.delete(0, 'end')
        entry_typologie.set('')
        entry_statut.set('')
        entry_desc.delete(1.0, 'end')

        # Afficher un message de succès
        messagebox.showinfo("Succès", "Les données ont été mises à jour avec succès.")

        cursor.close()
        connection.close()
    except (Exception, psycopg2.Error) as error:
        messagebox.showerror("Erreur", "Impossible de mettre à jour les données dans la base de données : {}".format(error))

  

def fetch_id_voie(): # fonction pour afficher les information sur l'id fourni dans la base
    id_voie_siga = entry_id.get().strip()

    if not id_voie_siga:
        messagebox.showwarning("Avertissement", "Veuillez entrer un ID de voie.")
        return

    try:
        id_voie_siga=int(id_voie_siga)
        connection = psycopg2.connect(
            user="postgres",
            password="Cadr@20$24!",
            host="10.128.3.34",
            port="5432",
            database="pada_toponyme"
        )

        cursor = connection.cursor()
    # requete pour recuperer les données de la base
        cursor.execute("SELECT numero, id_voie_siga, commune, nom_pada, typologie, statut, nom_toponyme, etat, description FROM toponyme.topo_pada WHERE id_voie_siga = %s", (id_voie_siga,))
        client_data = cursor.fetchone()


    # Insérer la description récupérée dans la zone de texte
        if client_data:
            entry_numero.delete(0, 'end')
            entry_numero.insert(0, client_data[0] if client_data[0] is not None else "")

            entry_id.delete(0, 'end')
            entry_id.insert(0, client_data[1] if client_data[1] is not None else "")

            entry_commune.delete(0, 'end')
            entry_commune.insert(0, client_data[2] if client_data[2] is not None else "")

            entry_nom_pada.delete(0, 'end')
            entry_nom_pada.insert(0, client_data[3] if client_data[3] is not None else "")

            # Pour la combobox typologie
            if client_data[4] is not None:
                 entry_typologie.set(client_data[4]) # Utiliser set() pour les combobox

            # Pour la combobox statut
            if client_data[5] is not None:
                entry_statut.set(client_data[5])

                entry_nom_toponyme.delete(0, 'end')
                entry_nom_toponyme.insert(0, client_data[6] if client_data[6] is not None else "")

            # Pour la combobox etat
            if client_data[7] is not None:
               entry_etat.set(client_data[7])

               entry_desc.delete(1.0, tk.END)
               entry_desc.insert(tk.END, client_data[8] if client_data[8] is not None else "")
        else:
            messagebox.showwarning("Avertissement", "Aucun ID de voie trouvé avec cet ID.")

        cursor.close()
        connection.close()
    except (Exception, psycopg2.Error) as error:
        messagebox.showerror("Erreur", "Impossible de récupérer les données de la base de données : {}".format(error))

def num_suivant():
    try:
        # Connexion à la base de données
        connection = psycopg2.connect(
            user="postgres",
            password="Cadr@20$24!",
            host="10.128.3.34",
            port="5432",
            database="pada_toponyme"
        )
        cursor = connection.cursor()

        # Récupérer la valeur actuelle de l'entrée, l'incrémenter de 1
        current_value = int(entry_numero.get())
        next_value = current_value + 1

        # Requête pour récupérer les données associées au numéro suivant
        cursor.execute("""
            SELECT numero, id_voie_siga, commune, nom_pada, typologie, statut, nom_toponyme, etat, description 
            FROM toponyme.topo_pada 
            WHERE numero = %s
        """, (next_value,))
        topo_data = cursor.fetchone()

        if topo_data:
            # Mettre à jour l'entrée avec la nouvelle valeur
            entry_numero.delete(0, tk.END)
            entry_numero.insert(0, next_value)

            # Vider tous les champs avant de remplir avec les nouvelles données
            entry_id.delete(0, 'end')
            entry_commune.delete(0, 'end')
            entry_nom_pada.delete(0, 'end')
            entry_typologie.set('')  # Réinitialiser la combobox
            entry_statut.set('')     # Réinitialiser la combobox
            entry_nom_toponyme.delete(0, 'end')
            entry_etat.set('')       # Réinitialiser la combobox
            entry_desc.delete(1.0, tk.END)

            # Remplir les champs avec les données récupérées
            entry_id.insert(0, topo_data[1] if topo_data[1] is not None else "")
            entry_commune.insert(0, topo_data[2] if topo_data[2] is not None else "")
            entry_nom_pada.insert(0, topo_data[3] if topo_data[3] is not None else "")
            if topo_data[4] is not None:
                entry_typologie.set(topo_data[4])  # Utiliser set() pour les combobox
            if topo_data[5] is not None:
                entry_statut.set(topo_data[5])
            entry_nom_toponyme.insert(0, topo_data[6] if topo_data[6] is not None else "")
            if topo_data[7] is not None:
                entry_etat.set(topo_data[7])
            entry_desc.insert(tk.END, topo_data[8] if topo_data[8] is not None else "")

        else:
            messagebox.showwarning("Avertissement", "Aucune donnée trouvée pour le numéro suivant.")

        # Fermeture de la connexion
        cursor.close()
        connection.close()

    except (Exception, psycopg2.Error) as error:
        messagebox.showerror("Erreur", "Impossible de récupérer les données de la base de données : {}".format(error))

   
def num_precedent():
    try:
        # Connexion à la base de données
        connection = psycopg2.connect(
            user="postgres",
            password="Cadr@20$24!",
            host="10.128.3.34",
            port="5432",
            database="pada_toponyme"
        )
        cursor = connection.cursor()

        # Récupérer la valeur actuelle de l'entrée, la décrémenter de 1
        current_value = int(entry_numero.get())
        previous_value = current_value - 1

        # Requête pour récupérer les données associées au numéro précédent
        cursor.execute("""
            SELECT numero, id_voie_siga, commune, nom_pada, typologie, statut, nom_toponyme, etat, description 
            FROM toponyme.topo_pada 
            WHERE numero = %s
        """, (previous_value,))
        topo_data = cursor.fetchone()

        if topo_data:
            # Mettre à jour l'entrée avec la nouvelle valeur
            entry_numero.delete(0, tk.END)
            entry_numero.insert(0, previous_value)

            # Vider tous les champs avant de remplir avec les nouvelles données
            entry_id.delete(0, 'end')
            entry_commune.delete(0, 'end')
            entry_nom_pada.delete(0, 'end')
            entry_typologie.set('')  # Réinitialiser la combobox
            entry_statut.set('')     # Réinitialiser la combobox
            entry_nom_toponyme.delete(0, 'end')
            entry_etat.set('')       # Réinitialiser la combobox
            entry_desc.delete(1.0, tk.END)

            # Remplir les champs avec les données récupérées
            entry_id.insert(0, topo_data[1] if topo_data[1] is not None else "")
            entry_commune.insert(0, topo_data[2] if topo_data[2] is not None else "")
            entry_nom_pada.insert(0, topo_data[3] if topo_data[3] is not None else "")
            if topo_data[4] is not None:
                entry_typologie.set(topo_data[4])  # Utiliser set() pour les combobox
            if topo_data[5] is not None:
                entry_statut.set(topo_data[5])
            entry_nom_toponyme.insert(0, topo_data[6] if topo_data[6] is not None else "")
            if topo_data[7] is not None:
                entry_etat.set(topo_data[7])
            entry_desc.insert(tk.END, topo_data[8] if topo_data[8] is not None else "")

        else:
            messagebox.showwarning("Avertissement", "Aucune donnée trouvée pour le numéro précédent.")

        # Fermeture de la connexion
        cursor.close()
        connection.close()

    except (Exception, psycopg2.Error) as error:
        messagebox.showerror("Erreur", "Impossible de récupérer les données de la base de données : {}".format(error))

   
    

def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    


root = tk.Tk()
root.title("FORMULAIRE TOPONYME 1")
    
    # Créer un Canvas
canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Créer une Scrollbar verticale
scrollbar_y = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Associer la Scrollbar verticale au Canvas
canvas.config(yscrollcommand=scrollbar_y.set)
    
    # Créer un frame à l'intérieur du Canvas pour contenir les widgets
frame = tk.Frame(canvas)
frame.pack(padx=20, pady=10)

    
    # Ajouter le frame au Canvas
canvas.create_window((0,0), window=frame, anchor="nw")
    
# Remplir le frame avec plusieurs widgets pour illustrer le défilement
# Champ d'entrée pour la numérotation
label_num_actu = tk.Label(frame, text="NUMERO  :")
label_num_actu.grid(row=0, column=0, padx=10, pady=5)
entry_numero = tk.Entry(frame, justify="center")
entry_numero.grid(row=0, column=1, padx=20, pady=10)

# bouton suivant
suiv_button = tk.Button(frame, text=">",command = num_suivant) 
suiv_button.place(x=585, y=8)

# bouton precedent
pre_button = tk.Button(frame, text="<" ,command=num_precedent)
pre_button.place(x=450, y=8)

# Champ d'entrée pour l'ID VOIE PADA
label_id = tk.Label(frame, text="ID VOIE PADA :")
label_id.grid(row=1, column=0, padx=10, pady=5)
entry_id = tk.Entry(frame, width=50, font=("Arial", 20))
entry_id.grid(row=1, column=1, padx=20, pady=10)

# Bouton pour récupérer les données
fetch_button = tk.Button(frame, text="Récupérer les données", command=fetch_id_voie)
fetch_button.grid(row=1, column=2, padx=10, pady=5)

# Créer les étiquettes et les champs de saisie
label_commune = tk.Label(frame, text="COMMUNE :")
label_commune.grid(row=2, column=0, padx=10, pady=5)
entry_commune = tk.Entry(frame, width=50, font=("Arial", 20))
entry_commune.grid(row=2, column=1, padx=20, pady=10)

label_nom_pada = tk.Label(frame, text="NOM PADA :")
label_nom_pada.grid(row=3, column=0, padx=10, pady=5)
entry_nom_pada = tk.Entry(frame, width=50, font=("Arial", 20))
entry_nom_pada.grid(row=3, column=1, padx=20, pady=10)

label_typologie = tk.Label(frame, text="TYPOLOGIE :")
label_typologie.grid(row=4, column=0, padx=10, pady=5)
typologie_values = ["Element de la nature", "Personnalité communale", "Personnalité nationale", "Riverain", "faune et flore", "Ville/Pays/Continent", "Personnalité internationale", "Concept", "Valeur morale", ""]  # Liste des valeurs
entry_typologie = ttk.Combobox(frame, values=typologie_values, font=("Arial", 20), width=49, state="readonly")
entry_typologie.grid(row=4, column=1, padx=20, pady=10)

# Création de la liste déroulante (Combobox)

label_statut = tk.Label(frame, text="STATUT :")
label_statut.grid(row=5, column=0, padx=10, pady=5)
statut_values = ["Attribué", "Non Attribué", ""]  # Liste des valeurs de statut
entry_statut =  ttk.Combobox(frame, values=statut_values, font=("Arial", 20), width=49, state="readonly")
entry_statut.grid(row=5, column=1, padx=20, pady=10)


label_nom_toponyme = tk.Label(frame, text="NOM TOPONYME :")
label_nom_toponyme.grid(row=6, column=0, padx=10, pady=5)
entry_nom_toponyme = tk.Entry(frame, width=50, font=("Arial", 20))
entry_nom_toponyme.grid(row=6, column=1, padx=20, pady=10)

label_etat = tk.Label(frame, text="ETAT :")
etat_values = ["Décédé", "Vivant", "Null", ""]  # Liste des valeurs d'état
label_etat.grid(row=7, column=0, padx=10, pady=5)
entry_etat= ttk.Combobox(frame, values=etat_values, font=("Arial", 20), width=49, state="readonly")
entry_etat.grid(row=7, column=1, padx=20, pady=10)

# Création de la liste déroulante (Combobox) pour l'état


label_desc = tk.Label(frame, text="DESCRIPTION  :")
label_desc.grid(row=8, column=0, padx=10, pady=5)
entry_desc = tk.Text(frame, width=50, height=10,font=("Arial", 20), wrap='word')
entry_desc.grid(row=8, column=1, padx=10, pady=5)


# Bouton pour soumettre les données
submit_button = tk.Button(frame, text="Soumettre", command=submit_client)
submit_button.grid(row=9, column=0, columnspan=2, padx=10, pady=5)


    # Mettre à jour la région scrollable du Canvas
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))
    
  # Capturer les événements de molette de souris pour le défilement
root.bind_all("<MouseWheel>", on_mouse_wheel)



root.mainloop()

