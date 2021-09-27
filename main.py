from tkinter import *
import pandas
import random
import pyttsx3

flash_card_data = {}
current_card = {}
learn_language = ""


# ***************************************** SPEAK LANGUAGE *******************************************************
def speak_language(word):
    global learn_language
    engine = pyttsx3.init()

    # Voice keys for spanish, francias, english
    es_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0"
    fr_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_FR-FR_HORTENSE_11.0"
    en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"

    engine.setProperty("rate", 145)  # Speed percent(can go over 100)
    engine.setProperty("volume", 0.9)  # Volume 0 - 1
    if learn_language == "French":
        engine.setProperty("voice", fr_voice_id)
    elif learn_language == "Spanish":
        engine.setProperty("voice", es_voice_id)

    # NOTE: USE THIS CODE TO GET THE VOICE ID OF YOUR LOCAL MACHINE AND CHANGE THE "es_voice_id" TO YOUR MACHINE ID FOR
    # THE SPEECH TO WORK LOCALLY.
    # voices = engine.getProperty('voices')
    # for voice in voices:
    #     print("Voice:")
    #     print(" - ID: %s" % voice.id)
    #     print(" - Name: %s" % voice.name)
    #     print(" - Languages: %s" % voice.languages)
    #     print(" - Gender: %s" % voice.gender)
    #     print(" - Age: %s" % voice.age)

    engine.say(word)
    engine.runAndWait()


# ***************************************** CHOOSE LANGUAGE *******************************************************
def run_french():
    global flash_card_data, learn_language, flip_timer
    print("french")
    french_btn.place_forget()
    spanish_btn.place_forget()
    try:
        french_english_data = pandas.read_csv("data/French_words_to_learn.csv").to_dict(orient='records')
        if len(french_english_data) == 0:
            french_english_data = pandas.read_csv("data/french_words.csv").to_dict(orient='records')
    except FileNotFoundError:
        french_english_data = pandas.read_csv("data/french_words.csv").to_dict(orient='records')
    finally:
        flash_card_data = french_english_data
        learn_language = "French"
        flip_timer = window.after(4000, func=flip_flash_card)
        generate_flash_cards()
        print(flash_card_data)


def run_spanish():
    global flash_card_data, learn_language, flip_timer
    print("spanish")
    french_btn.place_forget()
    spanish_btn.place_forget()
    try:
        spanish_english_data = pandas.read_csv("data/Spanish_words_to_learn.csv").to_dict(orient='records')
        if len(spanish_english_data) == 0:
            spanish_english_data = pandas.read_csv("data/spanish_words.csv").to_dict(orient='records')
    except FileNotFoundError:
        spanish_english_data = pandas.read_csv("data/spanish_words.csv").to_dict(orient='records')
    finally:
        flash_card_data = spanish_english_data
        learn_language = "Spanish"
        flip_timer = window.after(4000, func=flip_flash_card)
        generate_flash_cards()
        print(flash_card_data)


# ***************************************** GENERATE FLASH CARDS *******************************************************
def generate_flash_cards():
    global current_card, flash_card_data, learn_language, flip_timer
    window.after_cancel(flip_timer)
    # Check if data in the words to learn is finished, then replenish it
    # if len(flash_card_data) == 0:
    #     french_english_data = pandas.read_csv("data/french_words.csv").to_dict(orient='records')
    current_card = random.choice(flash_card_data)
    canvas.itemconfig(word_text, text=current_card[learn_language], fill="black")
    canvas.itemconfig(language_text, text=learn_language, fill="black")
    canvas.itemconfig(canvas_image, image=front_img)

    flip_timer = window.after(4000, func=flip_flash_card)
    speak_language(current_card[learn_language])


# ***************************************** FLIP FLASH CARDS ****************************************************
def flip_flash_card():
    canvas.itemconfig(canvas_image, image=back_img)
    canvas.itemconfig(language_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_card["English"], fill="white")


# ***************************************** SAVE DATA ****************************************************
def save_data():
    global flash_card_data, learn_language
    flash_card_data.remove(current_card)
    if learn_language == "French":
        French_words_to_learn_data = pandas.DataFrame(flash_card_data)
        French_words_to_learn_data.to_csv("data/French_words_to_learn.csv", index=False)
    elif learn_language == "Spanish":
        Spanish_words_to_learn_data = pandas.DataFrame(flash_card_data)
        Spanish_words_to_learn_data.to_csv("data/Spanish_words_to_learn.csv", index=False)


# ***************************************** UI SETUP *******************************************************
# TODO: UI SETUP
BACKGROUND_COLOR = "#B1DDC6"
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=0, bg=BACKGROUND_COLOR)

flip_timer = 0

canvas = Canvas(width=800, height=600, highlightthickness=0, bg=BACKGROUND_COLOR)

# Canvas Image
front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 300, image=front_img)

# Canvas Text
language_text = canvas.create_text(400, 150, text="Choose a language", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 350, text="", font=("Ariel", 48, "bold"))
canvas.grid(column=0, row=0, columnspan=2, padx=0, pady=0)

# Buttons
cancel_img = PhotoImage(file="images/wrong.png")
wrong_btn = Button(image=cancel_img, highlightthickness=0, command=generate_flash_cards)
wrong_btn.grid(column=0, row=1)

correct_img = PhotoImage(file="images/right.png")
right_btn = Button(image=correct_img, highlightthickness=0, command=lambda: [generate_flash_cards(), save_data()])
right_btn.grid(column=1, row=1)

french_img = PhotoImage(file="images/frenchpic250X86.png")
french_btn = Button(window, image=french_img, highlightthickness=0, bd=0, command=run_french)
french_btn.place(x=50, y=270)

spanish_img = PhotoImage(file="images/spanishpic250X85.png")
spanish_btn = Button(window, image=spanish_img, highlightthickness=0, bd=0, command=run_spanish)
spanish_btn.place(x=490, y=270)
# spanish_btn.place_forget()


window.mainloop()
