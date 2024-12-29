import json
from datetime import datetime


# Function to load data from a file
def load_data(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# Function to save data to a file
def save_data(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


# Function to display a welcome message and options
def display_welcome():
    print("Bienvenue au QCM Informatique!")
    print("1. Se connecter")
    print("2. Quitter")


# Function to display subjects
def display_subjects():
    print("Choisissez un sujet :")
    print("1. Mathematiques")
    print("2. Python")
    print("3. Java")
    print("4. C")
    print("5. Cybersecurite")


# Function to manage users
def manage_user(users):
    username = input("Entrez votre identifiant (nom ou ID) : ").strip()
    if username in users:
        print(f"Bienvenue, {username}!")
    else:
        print("Nouvel utilisateur détecté. Profil créé.")
        users[username] = {'history': []}
        save_data("users.json", users)
    return username


# Function to load questions from a file
def load_questions(filename):
    return load_data(filename)


# Function to ask questions and evaluate answers
def ask_questions(questions):
    score = 0
    for i, question in enumerate(questions, 1):
        print(f"Question {i}: {question['text']}")
        for option in question['options']:
            print(option)
        answer = input("Votre réponse : ").strip().lower()
        if answer == question['correct']:
            print("Bonne réponse !")
            score += 1
        else:
            print(f"Mauvaise réponse. La bonne réponse était : {question['correct']}")
    return score


# Function to save the user's score
def save_score(users, username, score, subject):
    users[username]['history'].append({
        'date': datetime.now().strftime("%Y-%m-%d"),
        'subject': subject,
        'score': score
    })
    save_data("users.json", users)


# Function to choose a subject
def choose_subject():
    display_subjects()
    subjects = {
        "1": "Mathematiques",
        "2": "Python",
        "3": "Java",
        "4": "C",
        "5": "Cybersecurite"
    }
    choice = input("Votre choix : ").strip()
    return subjects.get(choice, None)


# Function to display user menu
def user_menu():
    print("\nQue voulez-vous faire ?")
    print("1. Consulter l'historique")
    print("2. Passer un QCM")
    print("3. Se déconnecter")
    return input("Votre choix : ").strip()


# Main function
def main():
    users = load_data("users.json")

    while True:
        display_welcome()
        choice = input("Choisissez une option : ").strip()

        if choice == "1":
            username = manage_user(users)
            while True:
                action = user_menu()

                if action == "1":
                    print(f"\nHistorique de {username} :")
                    for entry in users[username]['history']:
                        print(f"- Date: {entry['date']}, Sujet: {entry['subject']}, Score: {entry['score']}")

                elif action == "2":
                    subject = choose_subject()
                    if not subject:
                        print("Sujet invalide. Veuillez réessayer.")
                        continue

                    questions = load_questions(f"questions_{subject.lower()}.json")
                    score = ask_questions(questions)
                    print(f"Votre score final : {score}/{len(questions)}")
                    save_score(users, username, score, subject)
                    print("Merci d'avoir participé !")

                elif action == "3":
                    print("Déconnexion en cours... Retour à l'accueil.")
                    break

                else:
                    print("Option invalide. Veuillez réessayer.")

        elif choice == "2":
            print("Au revoir!")
            break
        else:
            print("Option invalide. Veuillez réessayer.")


if __name__ == "__main__":
    main()
