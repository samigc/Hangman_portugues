import random
import csv
import json
import os
from tkinter import LEFT
import PIL.Image


ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", ".",
               '-', '_', '+', '<', '>', '?','\'','¿','!','"','=','¡', 
               '/', '\\', '|', '(', ')', '1', '{', '}', '[', ']',
               '*','&', '%', '$', '#', '@','~','·','¬',' ']

CENTER_SPACE = "\n"+" "*20
LEFT_SPACE = "\n"+" "*10

def resize(image, new_width = 30):
    old_width, old_height = image.size
    new_height = int(new_width * old_height/old_width)
    return image.resize((new_width,new_height))


def to_greyscale(image):
    return image.convert("L")


def pixel_to_ascii(image):
    pixels = image.getdata()
    ascii_str = "";
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel//25]
    ascii_str = ascii_str.replace(","," ")
    return ascii_str


def draw_stickman(image_route):
    image = PIL.Image.open(image_route)
    image = resize(image)
    greyscale_image = to_greyscale(image)
    ascii_str = pixel_to_ascii(greyscale_image)
    img_width = greyscale_image.width
    ascii_str_len = len(ascii_str)
    ascii_img = ""
    #split based in width
    for i in range(0,ascii_str_len,img_width):
        ascii_img += ascii_str[i:i+img_width] + "\n"
    print(ascii_img)
    # with open("./stickman/ascii_img.txt","w") as f:
    #     f.write(ascii_img)


def read_special_characters(route):
    file = open(route)
    data = json.load(file)
    return data['spec_char']


def replace_specials_word(word,special_characters_route):
    special_chars = read_special_characters(special_characters_route)
    for accented, cleaned in special_chars.items():
        word = word.replace(accented,cleaned)
    return word


def replace_specials_dict(dictionary,special_characters_route):
    for key, word in dictionary.items():
        dictionary[key] = replace_specials_word(word, special_characters_route)
    return dictionary


def read_dict(dictionary_route,special_character_route):
    with open(dictionary_route,'r',encoding = 'utf-8') as csvfile:
        csvfile_read = csv.reader(csvfile)
        dict_word = {row[0]:row[0] for row in csvfile_read}
    clean_dictionary = replace_specials_dict(dict_word,special_character_route)
    return clean_dictionary


def get_random_key(dictionary):
    random_key = random.choice(list(dictionary.keys()))
    return random_key


def decorator(word, clean_word,user_letters,turno):
    os.system("clear")
    number_of_lines = len(list(clean_word))
    image_route = "./stickman/stickman"+str(turno)+".png"
    draw_stickman(image_route)
    if len(user_letters)==0:
        print(CENTER_SPACE+"_ "*number_of_lines)
    else:
        drawing = list(map(lambda i: word[i]+" " if clean_word[i] in user_letters else "_ ",range(number_of_lines)))
        print(CENTER_SPACE+"".join(drawing))


def clean_letter():
    letter_ok = False
    while letter_ok == False:
        try:
            user_letter = input("Escribe una letra para adivinar la palabra: ")
            if len(user_letter) == 0 or user_letter.isnumeric() or len(user_letter) > 1 or user_letter in ASCII_CHARS:
                raise ValueError
            user_letter = user_letter.lower()
            letter_ok = True
        except ValueError as ve:
            print('¡Escribe una letra, intenta de nuevo! \n')
    return user_letter


def run_game():
    #definition of constants
    dictionary_route = './Archives/diccionario.csv'
    special_character_route = './Archives/special_characters.json'
    dictionary = read_dict(dictionary_route,special_character_route)
    key_to_play = get_random_key(dictionary)
    value_to_play = dictionary[key_to_play]
    user_letters = []
    is_playing = True
    wrong_letter = 0
    while is_playing:
        decorator(key_to_play ,value_to_play, user_letters, wrong_letter)
        if len(user_letters) !=0 :
            print("the letters already used are: "+ str(user_letters))
        user_letter = clean_letter()
        if user_letter not in list(value_to_play):
            wrong_letter +=1
        if user_letter not in user_letters:
            user_letters.append(user_letter)
        formed_word = list(map(lambda x: x if x in user_letters else "-", list(value_to_play)))
        if "".join(formed_word) == value_to_play:
            decorator(key_to_play, value_to_play,user_letters, wrong_letter)
            print(LEFT_SPACE+"¡S A L V A S T E   A L   A H O R C A D O !")
            is_playing = False
        if wrong_letter == 12 and is_playing:
            decorator(key_to_play, value_to_play,user_letters, wrong_letter)
            print(LEFT_SPACE+"A H O R C A D O :/ La palabra era: "+ key_to_play.capitalize())
            is_playing = False



if __name__ == '__main__':
    run_game()