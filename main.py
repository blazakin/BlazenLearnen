# Main UI for Blaze'n Learn'en spaced repetition tool.

from file_tools import *
import zmq

logo = """
██████╗ ██╗      █████╗ ███████╗███████╗███╗   ██╗    ██╗     ███████╗ █████╗ ██████╗ ███╗   ██╗███████╗███╗   ██╗
██╔══██╗██║     ██╔══██╗╚══███╔╝██╔════╝████╗  ██║    ██║     ██╔════╝██╔══██╗██╔══██╗████╗  ██║██╔════╝████╗  ██║
██████╔╝██║     ███████║  ███╔╝ █████╗  ██╔██╗ ██║    ██║     █████╗  ███████║██████╔╝██╔██╗ ██║█████╗  ██╔██╗ ██║
██╔══██╗██║     ██╔══██║ ███╔╝  ██╔══╝  ██║╚██╗██║    ██║     ██╔══╝  ██╔══██║██╔══██╗██║╚██╗██║██╔══╝  ██║╚██╗██║
██████╔╝███████╗██║  ██║███████╗███████╗██║ ╚████║    ███████╗███████╗██║  ██║██║  ██║██║ ╚████║███████╗██║ ╚████║
╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝    ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═══╝
"""


def send_message(message, port):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://localhost:{port}")

    socket.send_string(message)

    if message == 'Exit':
        return

    message = socket.recv()
    return message.decode()


def prompt(prompts):
    print()
    print("Choose an option below:")
    for index in range(len(prompts)):
        print(f"{index+1}) {prompts[index]}")
    user_input = input("Enter option: ")
    while not user_input.isnumeric() or (int(user_input) < 1 or int(user_input) > len(prompts)):
        print("Invalid option, try again.")
        user_input = input("Enter option: ")
    print()
    return prompts[int(user_input)-1]


def screens(screen_name):
    match screen_name:
        case 'Welcome':
            return welcome()
        case 'Tutorial':
            return tutorial()
        case 'Main Menu':
            return main_menu()
        case 'Add Card':
            return add_card()
        case 'Import/Export Cards':
            return imp_exp_cards()
        case 'Import Cards':
            return import_cards()
        case 'Export Cards':
            return export_cards()
        case 'Learn Cards':
            return learn_cards()
        case 'Search Cards':
            return search_cards()
        case _:
            return error_menu()


def welcome():
    print(logo)
    print("A spaced repetition learning tool.")
    return prompt(['Main Menu', 'Tutorial', 'Exit'])


def tutorial():
    print("Welcome to Blazen Learnen, this tool aims to help you study and memorize topics.")
    print()
    print("Making a Card: From the Main Menu choose \"Add Card\".")
    print("There you input a question and answer that will be saved as a card.")
    print()
    input("Press Enter to continue: ")
    print()
    print("Importing Cards: From the Main Menu choose \"Import/Export Cards\" then \"Import Cards\".")
    print("There, enter the filepath to the text file containing cards.")
    print("Currently only cards exported by this software are compatible.")
    print()
    input("Press Enter to continue: ")
    print()
    print("Exporting Cards: From the Main Menu choose \"Import/Export Cards\" then \"Export Cards\".")
    print("There enter the filepath and filename to export to.")
    print()
    input("Press Enter to continue: ")
    return prompt(['Tutorial', 'Main Menu', 'Exit'])


def main_menu():
    print("Main Menu")
    return prompt(['Learn Cards', 'Add Card', 'Import/Export Cards', 'Search Cards', 'Tutorial', 'Exit'])


def add_card():
    print("Add a card to your collection.")
    question = input("Enter Question: ")
    answer = input("Enter answer: ")
    if prompt(['Save Card', 'Discard card']) == 'Save Card':
        write("cards.txt", f"{question}, {answer};\n")
        print("Card successfully saved.")
        print()
    else:
        print("Card discarded.")
        print()
    return 'Main Menu'


def imp_exp_cards():
    print("Import/Export Cards")
    return prompt(['Import Cards', 'Export Cards', 'Main Menu'])


def import_cards():
    print("Import cards from a compatible text file.")
    print()
    print("Enter the entire filepath to the text file.")
    file_path = input("Filepath: ")

    while send_message("Check; " + file_path, "5554") == "False":
        print("Invalid filepath.")
        if prompt(['Try again', 'Main Menu']) == 'Try again':
            file_path = input("Filepath: ")
        else:
            return 'Main Menu'

    if prompt(['Add cards', 'Do not add cards']) == 'Add cards':
        cards = send_message("Import; " + file_path, "5554")
        write("cards.txt", cards)
        print("Cards successfully added.")
    else:
        print("Cards not added")

    return 'Main Menu'


def export_cards():
    print("Export cards to a text file.\n")

    file_path = input("Enter full filepath (including filename): ")
    send_message("Export; " + file_path + "; " + read("cards.txt"), "5554")
    print("Cards Exported")
    return 'Main Menu'


def learn_cards():
    print("Study your card collection!")
    cards = read("cards.txt")
    while prompt(["Study Card", "Main Menu"]) == "Study Card":
        card_to_study = send_message(cards, "5552")
        print(card_to_study.split(", ")[0])
        input("Press Enter to see answer: ")
        print(card_to_study.split(", ")[1])
        prompt(["Remembered", "Forgot"])
    return 'Main Menu'


def search_cards():
    print("Search for a card in your card collection.")
    cards = read("cards.txt")
    while prompt(["Search Cards", "Main Menu"]) == "Search Cards":
        search_term = input("Enter search term: ")
        search_query = search_term + ";" + cards
        result = send_message(search_query, "5553")
        print(f"Result: {result}")
    return 'Main Menu'


def error_menu():
    print("Error state reached, please contact developer.")
    return prompt(['Main Menu', 'Exit'])


user_screen = "Welcome"
while user_screen != "Exit":
    user_screen = screens(user_screen)
