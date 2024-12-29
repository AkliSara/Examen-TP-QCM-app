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

# Function to manage users
def manage_user(users):
    username = input("Entrez votre identifiant (nom ou ID) : ").strip()
    if username in users:
        print(f"Historique de {username} :")
        for entry in users[username]['history']:
            print(f"- Date: {entry['date']}, Score: {entry['score']}")
    else:
        print("Nouvel utilisateur détecté. Profil créé.")
        users[username] = {'history': []}
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
def save_score(users, username, score):
    users[username]['history'].append({
        'date': datetime.now().strftime("%Y-%m-%d"),
        'score': score
    })
    save_data("users.json", users)

# Main function
def main():
    users = load_data("users.json")
    questions = load_questions("questions.json")

    while True:
        display_welcome()
        choice = input("Choisissez une option : ").strip()

        if choice == "1":
            username = manage_user(users)
            score = ask_questions(questions)
            print(f"Votre score final : {score}/{len(questions)}")
            save_score(users, username, score)
            print("Merci d'avoir participé !")
        elif choice == "2":
            print("Au revoir!")
            break
        else:
            print("Option invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
