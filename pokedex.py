import requests
import json
from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO
import webbrowser #webbrowser library for connecting to the browser
from tkinter import messagebox
from playsound import playsound #installed playsound library for adding audio

main = Tk()
main.title("Pokedex")
main.geometry("400x650")
main.resizable(0,0)
main['bg']='#A1C0EF'
#to change the icon of tk window
main.iconphoto(False, ImageTk.PhotoImage(file='pokeball.png'))

file_name = 'pokemon_info.json' #json file where the info from api is stored

def audio():
    playsound("game_audio.mp3") #installed playsound library for playing audio

#function to display general pokemon info
def pokemon_info(pokemon_name): #name or id can be used
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}/'
    response = requests.get(url) #to get the content from the url
    response.raise_for_status() #returns HTTPError if an error occurs
    data = response.json() #converting data into json format
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4) #dumping data into the json file

    global id
    id = data["id"] #pokemon id

    name_label.config(text = data["name"].upper()) #used config to display data in widget
    id_label.config(text = data["id"])
    img_url = data["sprites"]["front_default"]
    img_response = requests.get(img_url)
    if img_response.status_code ==200: 
        image = Image.open(BytesIO(img_response.content)) #to display img from url
        image = image.resize((200,200))
        image = ImageTk.PhotoImage(image)
        image_label = Label(canvas1, image=image)
        image_label.image = (image)
        image_label.place(x=70, y=38)

    type_label.config(text = data["types"][0]["type"]["name"])
    weight_label.config(text = data["weight"])
    height_label.config(text = data["height"])
    for i in data["moves"]: #loop made to display all moves possible for the pokemon
       x = i['move']['name']+'\n'
       moves_label.insert(END, x)

#function to display where the pokemon is found in the game
def location(id):
    url = f'https://pokeapi.co/api/v2/pokemon/{id}/encounters'
    response = requests.get(url)
    response.raise_for_status() 
    data = response.json()
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

    x = data[0]["location_area"]["name"]
    loca_label.insert(END, x) 
    #the api does not have the location of all pokemon, hence sometimes the field will be empty

#function to display pokemon characteristics
def pokemon_characteristic(id):
    url = f'https://pokeapi.co/api/v2/characteristic/{id}/'
    response = requests.get(url)
    if response.status_code==404: #no content available - error code 404
        messagebox.showinfo("showinfo", "No Information Found")
        response.raise_for_status() 
    data = response.json()
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

    gene_label.config(text=data["gene_modulo"])
    stat_label.config(text=data["highest_stat"]["name"])
    x = data["descriptions"][7]['description']+'\n' #[7] is to display content in en language from the json file
    descpt_label.insert(END, x)
    #the api does not have the characteristics of all pokemon, hence sometimes the field will be empty

    location(id) #function call, to display location with characteristics of the pokemon

def switchFrame(frame): #function to switch frames
    frame.tkraise() 

def get_data(): #function to store the pokemon name in a global variable
   global pokemon_name
   pokemon_name=input_poke_name.get()

#first frame, where the user has to enter pokemon name/id
frame1 = Frame(main, width=380, height=630) 
frame1.place(x=10, y=10)

#second frame, to display the info of pokemon name/id entered
frame2 = Frame(main, width=380, height=630, bg='#C6A969',highlightbackground="blue", highlightthickness=2)
frame2.place(x=10, y=10)

bg_img = Image.open('bg img.png') #background img for frame1
resized_image= bg_img.resize((380,630))
bg_img= ImageTk.PhotoImage(resized_image)
Label(frame1, image=bg_img).place(x=0, y=0)

Label(frame1, text="LET THE BATTLE BEGIN!",font=('Lucida Console', 14),bg='#C6A969',border=8).place(x=60, y=430)
Label(frame1, text='POKEMON NAME :',font=('Lucida Console', 12)).place(x=30, y=480)

#entry field for user to input pokemon name/id 
input_poke_name = Entry(frame1, width=25)
input_poke_name.place(x=200,y=480)

def link(): #webbrowser library to open browser tab
    webbrowser.open_new("https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number")

#instructions
Label(frame1, text="Search for Pokemon name/id",font=('Lucida Console', 10),bg='#C6A969',border=2).place(x=60, y=520)
Button(frame1, text='here',font=('Lucida Console', 10), bg='#C6A969',border=2,command=lambda:link()).place(x=280, y=520)
Label(frame1, text="Or try bulbasaur, in all lower case",font=('Lucida Console', 10),bg='#C6A969',border=2).place(x=50, y=545)

#button calls switchFrame(frame2), get_data(), and pokemon_info(pokemon_name) function
Button(frame1, text='FIND',font=('Lucida Console', 14), bg='#C6A969',border=8,command=lambda:[switchFrame(frame2), get_data(), pokemon_info(pokemon_name)]).place(x=150, y=570)

#canvas to display pokemon name, id and image
canvas1 = Canvas(frame2, width=335, height=250,highlightbackground="blue", highlightthickness=2)
canvas1.place(x=20, y=15)

#button to return to home
Button(frame2, text='⌂', fg='white', bg='brown',width=3, command=lambda:switchFrame(frame1)).place(x=350, y=0)

name_label = Label(canvas1,font=('Lucida Console', 17))
name_label.place(x=5, y=5)

id_label = Label(canvas1,font=('Lucida Console', 17))
id_label.place(x=290, y=5)

#frame to display characteristics of pokemon
frame4 = Frame(frame2, width=335, height=330, bg='#C6A969',highlightbackground="blue", highlightthickness=2)
frame4.place(x=20, y=280)

#frame to display pokemon abilities
frame3 = Frame(frame2, width=335, height=330, bg='#C6A969',highlightbackground="blue", highlightthickness=2)
frame3.place(x=20, y=280)

Label(frame3,text='⟡ TYPE',font=('Lucida Console', 12)).place(x=20, y=20)
type_label = Label(frame3,font=('Lucida Console', 12))
type_label.place(x=120, y=20)

Label(frame3,text='⟡ WEIGHT',font=('Lucida Console', 12)).place(x=20, y=50)
weight_label = Label(frame3,font=('Lucida Console', 12))
weight_label.place(x=120, y=50)

Label(frame3,text='⟡ HEIGHT',font=('Lucida Console', 12)).place(x=20, y=80)
height_label = Label(frame3,font=('Lucida Console', 12))
height_label.place(x=120, y=80)

Label(frame3,text='⟡ MOVES',font=('Lucida Console', 12)).place(x=20, y=110)
moves_label = Text(frame3, font=('Lucida Console', 12), height=8, width=16)
moves_label.place(x=120, y=110)

#button to call switchFrame(frame4), and pokemon_characteristic(id) function
Button(frame3, text='CHARACTERISTICS',font=('Lucida Console', 11), bg='#C6A969',border=4, command=lambda:[switchFrame(frame4),pokemon_characteristic(id)]).place(x=15, y=260)
#button to switchFrame(frame3)
Button(frame3, text='GENERAL INFO',font=('Lucida Console', 11), bg='#C6A969',border=4, command=lambda:switchFrame(frame3)).place(x=190, y=260)

Label(frame4,text='⟡ GENE MODULO',font=('Lucida Console', 12)).place(x=20, y=20)
gene_label = Label(frame4,font=('Lucida Console', 12))
gene_label.place(x=170, y=20)

Label(frame4,text='⟡ STAT',font=('Lucida Console', 12)).place(x=20, y=50)
stat_label = Label(frame4,font=('Lucida Console', 12))
stat_label.place(x=170, y=50)

Label(frame4,text='⟡ LOCATION',font=('Lucida Console', 12)).place(x=20, y=80)
loca_label = Text(frame4,font=('Lucida Console', 12), width=14, height=4)
loca_label.place(x=170, y=80)

Label(frame4,text='⟡ DESCRIPTION',font=('Lucida Console', 12)).place(x=20, y=160)
descpt_label = Text(frame4,font=('Lucida Console', 12), width=14, height=5)
descpt_label.place(x=170, y=160)

#button to call switchFrame(frame4), and pokemon_characteristic(id) function
Button(frame4, text='CHARACTERISTICS',font=('Lucida Console', 11), bg='#C6A969',border=4, command=lambda:[switchFrame(frame4),pokemon_characteristic(id)]).place(x=15, y=260)
#button to switchFrame(frame3)
Button(frame4, text='GENERAL INFO',font=('Lucida Console', 11), bg='#C6A969',border=4, command=lambda:switchFrame(frame3)).place(x=190, y=260)

#the first display frame is frame1
switchFrame(frame1)
audio() #audio plays before the tk window opens

main.mainloop()