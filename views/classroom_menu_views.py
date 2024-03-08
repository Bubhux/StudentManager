from controllers.classroom_controller import ClassroomDatabaseController
from models.classroom_models import ClassroomModel


class ClassroomView:

    def __init__(self):
        self.database_controller = ClassroomDatabaseController()

    def display_main_menu(self):

        while True:
            print("\nMenu gestion des classes")
            print("1. Afficher les classes")
            print("2. Ajouter une classe")
            print("3. Modifier les informations d'une classe")
            print("4. Calculer la moyenne d'une classe")
            print("5. Supprimer une classe")
            print("r. Retour au menu précedent\n> ")

            choice_menu = input("Choisissez le numéro de votre choix.\n> ")

            if choice_menu == "1":
                self.display_classrooms()

            elif choice_menu == "2":
                self.add_classroom()

            elif choice_menu == "3":
                self.update_classroom_info()

            elif choice_menu == "4":
                self.update_student_info()

            elif choice_menu == "5":
                self.delete_classroom()

            elif choice_menu == "r":
                print("Menu principal !")
                break
            else:
                print("Choix invalide, saisissez un nombre entre 1 et 6 ou r.")

    def display_classrooms(self):
        classrooms = self.database_controller.get_all_classrooms_database_controller()
        if not classrooms:
            print("Il n'y a pas de classes à afficher.")
        else:
            print("Liste des classes :")
            for classroom in classrooms:
                # Affiche le nom de la classe et le nombre d'étudiants dans cette classe
                print(f"- {classroom['classroom_name']}, "
                      f"Nombre de places disponibles : {classroom['number_of_places_available']}, "
                      f"Nombre d'étudiants : {classroom['number_of_students']}")

    def add_classroom(self):
        classroom_name = input("Nom de la classe : ")
        number_of_places_available_input = input("Nombre de places disponibles (appuyez sur Entrée pour laisser vide) : ")
        number_of_students_input = input("Nombre d'étudiants (appuyez sur Entrée pour laisser vide) : ")

        # Vérifie si rien n'est saisi pour le nombre de places disponibles, puis définit 0 comme valeur par défaut
        if number_of_places_available_input:
            number_of_places_available = int(number_of_places_available_input)
        else:
            number_of_places_available = 0

        # Vérifie si rien n'est saisi pour le nombre d'étudiants, puis définit 0 comme valeur par défaut
        if number_of_students_input:
            number_of_students = int(number_of_students_input)
        else:
            number_of_students = 0

        # Créer une instance de ClassroomModel avec les données d'entrée
        new_classroom = ClassroomModel(
            classroom_name,
            number_of_places_available,
            number_of_students
        )

        # Valider les données d'entrée
        if new_classroom.validate_input_data_classroom():
            classroom_data = {
                'classroom_name': classroom_name,
                'number_of_places_available': number_of_places_available,
                'number_of_students': number_of_students
            }
            self.database_controller.add_classroom_database_controller(classroom_data)
            print("La classe a été ajoutée avec succès!")
        else:
            print("Les données d'entrée sont invalides.")

    def update_classroom_info(self):
        classroom_name = input("Nom de la classe à mettre à jour : ")

        # Vérifie si la classe existe
        classroom = self.database_controller.get_classroom_database_controller(classroom_name)
        if not classroom:
            print(f"Aucune classe trouvée avec le nom {classroom_name}. Vérifiez le nom de la classe.")
            return

        # Demande les nouvelles informations
        new_classroom_name = input("Nouveau nom de la classe (appuyez sur Entrée pour conserver le nom actuel) : ").strip()
        new_number_of_places_available = input("Nouveau nombre de places disponibles (appuyez sur Entrée pour conserver le nombre actuel) : ").strip()
        new_number_of_students = input("Nouveau nombre d'étudiants (appuyez sur Entrée pour laisser vide) : ").strip()

        # Vérifie si les nouvelles informations sont fournies, sinon conserve les informations actuelles
        new_classroom_name = new_classroom_name if new_classroom_name else classroom['classroom_name']
        new_number_of_places_available = new_number_of_places_available if new_number_of_places_available else classroom['number_of_places_available']
        new_number_of_students = new_number_of_students if new_number_of_students else classroom['number_of_students']

        # Crée un dictionnaire avec les nouvelles informations de la classe
        new_classroom_data = {
            'classroom_name': new_classroom_name,
            'new_number_of_places_available': new_number_of_places_available,
            'new_number_of_students' : new_number_of_students
        }

        # Mettre à jour les informations de la classe
        self.database_controller.update_classroom_info_database_controller(classroom_name, new_classroom_data)

    def delete_classroom(self):
        classroom_name = input("Nom de la classe à supprimer. : ")
        self.database_controller.delete_classroom_database_controller(classroom_name)

    def calculate_classroom_average(self):
        classroom_name = input("Nom de la classe à calculer la moyenne. : ")
        average = self.database_controller.calculate_classroom_average_database_controller(classroom_name)
        if average is not None:
            print(f"Moyenne de {classroom_name} : {average:.2f}")
        else:
            print(f"Aucune classe trouvé avec le nom {classroom_name}. Vérifiez le nom de la classe.")
