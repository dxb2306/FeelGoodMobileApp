from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob
from datetime import datetime
from pathlib import Path
import random
from difflib import get_close_matches

data = json.load(open("data.json"))

def translate(x):
    x = x.lower()
    if x in data:
        return data[x]
    elif x.title() in data: #if user entered "texas" this will check for "Texas" as well.
        return data[x.title()]
    elif x.upper() in data: #in case user enters words like USA or NATO
        return data[x.upper()]
    
    else:
        return 'The word doesn\'t exist. Please check it again.'


Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"
    
    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong username or password!"


class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def back_to_login_page(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "Login_Screen"
        
    def add_user(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        
        users[uname] = {'username': uname,
        'password': pword,
        'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        with open("users.json", 'w') as file:
            json.dump(users, file)
        self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def back_to_login_page(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "Login_Screen"

class LoginScreenSucess(Screen):
    def dictionary_page(self):
        self.manager.current = "dictionaryPage"


    def log_out(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "Login_Screen"
    
    def getquote(self, feel):
        #print(feel)
        feel = feel.lower()
        available_feelings = glob.glob("quotes/*txt")
        
        available_feelings = [Path(filename).stem for filename in
        available_feelings]

        if feel in available_feelings:
            with open(f"quotes/{feel}.txt") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling. (happy, sad, unloved))"

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass        


class DictionaryPage(Screen):

    def log_out(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "Login_Screen"

    def getword(self, word):
        
        output = translate(word)
        self.ids.wordtext.text = str(output)




class MainApp(App):
    def build(self):
        return RootWidget()

    

if __name__ == "__main__":
    MainApp().run()