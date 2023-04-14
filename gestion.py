from tkinter import messagebox
import mysql.connector
from tkinter import *


class GestionStock:
    def __init__(self):
        self.screen = Tk()
        self.screen.title("Gestion de stock Boutique")
        self.screen.geometry("400x310")
        self.screen.configure(bg='grey')
        self.ma_bdd = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="boutique",
        )
        self.result_listbox = Listbox(self.screen)
        self.result_listbox.place(x=10, y=40)
        self.result_listbox.config(width=63)
        self.title = Label(self.screen, text="GESTION DE STOCK :", font=("arial", 15, "bold"), fg="black")
        self.title.place(x=90, y=5)
        self.boutique = self.ma_bdd.cursor()
        self.boutique.execute("select * from produit")
        self.resultat_stock = self.boutique.fetchall()
        self.result_listbox.insert(END, f"{'ID'} {'Nom'} {'Stock'} {'Prix'} {'ID_Catégorie'}")
        for resultat in self.resultat_stock:
            id = resultat[0]
            produit = resultat[1]
            prix = resultat[2]
            stock = resultat[3]
            id_catégorie = resultat[4]
            self.result_listbox.insert(END, f"{id}: {produit}: {stock}: {prix} : {id_catégorie}")
        self.boutton_add = Button(self.screen, text="Ajouter un produit", fg="green", command=self.ajouter_produit)
        self.boutton_add.place(x=50, y=220, height=30, width=140)
        self.boutton_del = Button(self.screen, text="Supprimer un produit", fg="red", command=self.supp_produit)
        self.boutton_del.place(x=50, y=255, height=30, width=140)
        self.boutton_edit = Button(self.screen, text="Modifier un produit", fg="blue", command=self.modifier_produit)
        self.boutton_edit.place(x=210, y=220, height=30, width=140)
        self.boutton_add_categ = Button(self.screen, text="Ajouter une catégorie", fg="purple", command=self.ajouter_categorie)
        self.boutton_add_categ.place(x=210, y=255, height=30, width=140)

    def run(self):
        if self.ma_bdd.is_connected():
            print("Connexion à la BDD réussie.")
        else:
            print("Connexion à la BDD échoué.")
        self.screen.mainloop()

    def ajouter_produit(self):
        fenetre = Toplevel(self.screen)
        fenetre.title("Ajouter un produit")
        fenetre.geometry("300x140")
        label_nom = Label(fenetre, text="Nom du produit :")
        label_nom.grid(row=0, column=0)
        champ_nom = Entry(fenetre)
        champ_nom.grid(row=0, column=1)
        label_description = Label(fenetre, text="Description :")
        label_description.grid(row=1, column=0)
        champ_description = Entry(fenetre)
        champ_description.grid(row=1, column=1)
        label_prix = Label(fenetre, text="Prix :")
        label_prix.grid(row=2, column=0)
        champ_prix = Entry(fenetre)
        champ_prix.grid(row=2, column=1)
        label_quantite = Label(fenetre, text="Quantité :")
        label_quantite.grid(row=3, column=0)
        champ_quantite = Entry(fenetre)
        champ_quantite.grid(row=3, column=1)
        label_categorie = Label(fenetre, text="ID catégorie :")
        label_categorie.grid(row=4, column=0)
        champ_categorie = Entry(fenetre)
        champ_categorie.grid(row=4, column=1)
        bouton_valider = Button(fenetre, text="Valider", command=lambda:
        self.enregistrer_produit(champ_nom.get(),
                                 champ_description.get(),
                                 champ_prix.get(),
                                 champ_quantite.get(),
                                 champ_categorie.get()))
        bouton_valider.grid(row=5, column=1)

    def afficher_produits(self):
        self.boutique.execute("select * from produit")
        resultat_stock = self.boutique.fetchall()
        for resultat in self.resultat_stock:
            id = resultat[0]
            produit = resultat[1]
            prix = resultat[2]
            stock = resultat[3]
            id_categorie = resultat[4]
            self.result_listbox.insert(END, f"{id}: {produit}: {stock}: {prix} : {id_categorie}")

    def effacer_affichage(self):
        self.result_listbox.delete(0, END)

    def enregistrer_produit(self, nom, description, prix, quantite, id_categorie):
        curseur = self.ma_bdd.cursor()
        requete = "INSERT INTO produit (nom, description, prix, quantite, id_categorie) VALUES (%s, %s, %s, %s, %s)"
        valeurs = (nom, description, prix, quantite, id_categorie)
        curseur.execute(requete, valeurs)
        self.ma_bdd.commit()
        self.effacer_affichage()
        self.afficher_produits()

    def supp_produit(self):
        fenetre = Toplevel(self.screen)
        fenetre.title("Supprimer un produit")
        fenetre.geometry("300x80")

        label_nom = Label(fenetre, text="Nom du produit :")
        label_nom.grid(row=0, column=0)
        champ_nom = Entry(fenetre)
        champ_nom.grid(row=0, column=1)

        bouton_valider = Button(fenetre, text="Valider", command=lambda: self.supprimer_produit(champ_nom.get()))
        bouton_valider.grid(row=1, column=0, columnspan=2)

    def supprimer_produit(self, nom_produit):
        self.boutique.execute("DELETE FROM produit WHERE nom = %s", (nom_produit,))
        self.ma_bdd.commit()
        self.effacer_affichage()
        self.afficher_produits()

    def modifier_produit(self):
        fenetre = Toplevel(self.screen)
        fenetre.title("Modifier un produit")
        fenetre.geometry("300x140")

        label_nom = Label(fenetre, text="Nom du produit :")
        label_nom.grid(row=0, column=0)
        champ_nom = Entry(fenetre)
        champ_nom.grid(row=0, column=1)

        label_description = Label(fenetre, text="Description :")
        label_description.grid(row=1, column=0)
        champ_description = Entry(fenetre)
        champ_description.grid(row=1, column=1)

        label_prix = Label(fenetre, text="Prix :")
        label_prix.grid(row=2, column=0)
        champ_prix = Entry(fenetre)
        champ_prix.grid(row=2, column=1)

        label_quantite = Label(fenetre, text="Quantité :")
        label_quantite.grid(row=3, column=0)
        champ_quantite = Entry(fenetre)
        champ_quantite.grid(row=3, column=1)

        label_categorie = Label(fenetre, text="ID catégorie :")
        label_categorie.grid(row=4, column=0)
        champ_categorie = Entry(fenetre)
        champ_categorie.grid(row=4, column=1)

        bouton_valider = Button(fenetre, text="Valider", command=lambda:
        self.modifier_produit_bd(champ_nom.get(),
                                 champ_description.get(),
                                 champ_prix.get(),
                                 champ_quantite.get(),
                                 champ_categorie.get()))
        bouton_valider.grid(row=5, column=0, columnspan=2)

    def modifier_produit_bd(self, nom_produit, description, prix, quantite, id_categorie):
        self.boutique.execute(
            "UPDATE produit SET description=%s, prix=%s, quantite=%s, id_categorie=%s WHERE nom=%s",
            (description, prix, quantite, id_categorie, nom_produit),
        )
        self.ma_bdd.commit()
        messagebox.showinfo("Produit modifié", "Le produit a été modifié avec succès.")
        self.effacer_affichage()
        self.afficher_produits()

    def ajouter_categorie(self):
        self.categ_window = Toplevel(self.screen)
        self.categ_window.title("Ajouter une catégorie")
        self.categ_window.geometry("300x100")
        self.categ_window.configure(bg='grey')
        self.label_categ = Label(self.categ_window, text="Nom de la catégorie:", font=("arial", 10, "bold"), fg="black")
        self.label_categ.place(x=10, y=10)
        self.entry_categ = Entry(self.categ_window, width=25)
        self.entry_categ.place(x=130, y=10)
        self.btn_valider_categ = Button(self.categ_window, text="Valider", command=self.valider_categorie)
        self.btn_valider_categ.place(x=120, y=60)

    def valider_categorie(self):
        nouvelle_categ = self.entry_categ.get()
        if nouvelle_categ:
            self.boutique.execute("INSERT INTO categorie (nom) VALUES (%s)", (nouvelle_categ,))
            self.ma_bdd.commit()
            self.result_listbox.delete(0, END)
            self.boutique.execute("SELECT * FROM produit")
            self.resultat_stock = self.boutique.fetchall()
            self.effacer_affichage()
            self.afficher_produits()


gestion_stock = GestionStock()
gestion_stock.run()
