# #!/usr/bin/python3

# from gi.repository import Gtk

# import argparse

# from pyramid.paster import bootstrap
# from sqlalchemy import engine_from_config
# from contact.models import DBSession, Base, Contact, Subject

# import transaction


# class GtkContact:
#     def __init__(self, controller):
#         self.controller = controller

#         # Chargement de l'interface dessinée avec Glade
#         interface = Gtk.Builder()
#         interface.add_from_file('contact/templates/contact.glade')

#         # Lien vers les champs utiles        
#         self.email = interface.get_object("email_entry")
#         self.subject = interface.get_object("subject_id_combobox")
#         self.text = interface.get_object("message_textview")

#         # Remplissage de la liste déroulante
#         store = Gtk.ListStore(int, str)
#         for subject in controller.get_subjects():
#             store.append([subject.id, subject.name])

#         self.subject.set_model(store)
#         cell = Gtk.CellRendererText()
#         self.subject.pack_start(cell, True)
#         self.subject.add_attribute(cell, "text", 1)

#         # Rattachement des événements aux méthodes de la classe
#         interface.connect_signals(self)

#         # Affichage de la fenêtre
#         window = interface.get_object("main_window")
#         window.show_all()

#     def on_main_window_destroy(self, widget):
#         Gtk.main_quit()

#     def on_apply_button_clicked(self, widget):
#         # Récupération de la valeur d'un champs texte
#         email = self.email.get_text()

#         # Récupération de la valeur d'une liste déroulante
#         tree_iter = self.subject.get_active_iter()
#         if tree_iter is None:
#             return
#         model = self.subject.get_model()
#         row_id, name = model[tree_iter][:2]
#         subject_id = row_id

#         # Récupération de la valeur d'un champs texte multiligne
#         message = self.text.get_buffer()
#         text = message.get_text(message.get_start_iter(), message.get_end_iter(), False)

#         # Création du contact
#         self.controller.add_contact(email, subject_id, text)


# class Controller:
#     def __init__(self, DBSession):
#         self.DBSession = DBSession
#         GtkContact(self)
#         Gtk.main()

#     def get_subjects(self):
#         return DBSession.query(Subject).all()

#     def add_contact(self, email, subject_id, text):
#         with transaction.manager:
#             DBSession.add(Contact(email=email, subject_id=subject_id, text=text))

# def get_parser():
#     # Étape 1 : définir une fonction proxy vers la fonction principale
#     def proxy_gcontact(args):
#         """Fonction proxy vers contact"""
#         try:
#             env = bootstrap(args.config_uri)
#         except:
#             print('Configuration file is not valid: %s' % args.config_uri)
#             return
#         settings, closer = env['registry'].settings, env['closer']
#         try:
#             engine = engine_from_config(settings, 'sqlalchemy.')
#             DBSession.configure(bind=engine)
#             Base.metadata.bind = engine
#             Controller(DBSession)
#         finally:
#             closer()

#     # Étape 2 : définir l'analyseur général
#     parser = argparse.ArgumentParser(
#         prog = 'contact',
#         description = """Programme permettant de rajouter un Contact""",
#         epilog = """Réalisé pour le livre Python, les fondamentaux du langage"""
#     )

#     # Rajout des options utiles

#     parser.add_argument(
#         'config_uri',
#         help = """fichier de configuration""",
#         type = str,
#     )

#     # Étape 3 : rajouter le lien entre l'analyseur et la fonction proxy pour calcul_capital
#     parser.set_defaults(func=proxy_gcontact)

#     return parser




# def main():
#     parser = get_parser()
#     # Étape 4 : démarrer l'analyse des arguments, puis le programme.
#     args = parser.parse_args()
#     args.func(args)


# # Fin du programme

