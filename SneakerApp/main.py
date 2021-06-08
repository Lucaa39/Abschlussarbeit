from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder
from Start import Start
from kivy.uix.popup import Popup
import mysql.connector

db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="sneakerapp")
cur = db.cursor()

global Names


def show_popupFehlerDB():
    show = PDB()
    popupWindow = Popup(title="Fehler", content=show, size_hint=(None, None), size=(400, 150))
    popupWindow.open()


def show_popup():
    show = PLogin()
    popupWindow = Popup(title="Fehler", content=show, size_hint=(None, None), size=(400, 150))
    popupWindow.open()


def show_popupRegister():
    show = PRegister()
    popupWindow = Popup(title="Fehler", content=show, size_hint=(None, None), size=(400, 150))
    popupWindow.open()


class PDB(FloatLayout):
    pass


class PLogin(FloatLayout):
    pass


class PRegister(FloatLayout):
    pass


class FirstScreen(Screen):
    user = ObjectProperty()
    password = ObjectProperty()

    def login_user(self):
        global username
        username = self.user.text
        password = self.password.text
        cur.execute('SELECT * FROM login WHERE username="%s" AND passwort="%s"' % (username.capitalize(), password))
        if (username and password) and cur.fetchall():
            self.manager.current = 'second'
        else:
            show_popup()

    def add_user(self):
        if (self.user.text and self.password.text):
            username = self.user.text
            password = self.password.text
            try:
                cur.execute(""" INSERT INTO login (username, passwort) VALUES ("%s","%s")""" % (
                username.capitalize(), password))
                db.commit()
                self.manager.current = 'second'
            except:
                show_popupRegister()

    pass


class SavesScreen(Screen):
    saveName1 = ObjectProperty()
    saveName2 = ObjectProperty()
    saveName3 = ObjectProperty()
    saveName4 = ObjectProperty()
    preisS1 = ObjectProperty()
    preisR1 = ObjectProperty()
    preisK1 = ObjectProperty()
    preisS2 = ObjectProperty()
    preisR2 = ObjectProperty()
    preisK2 = ObjectProperty()
    preisS3 = ObjectProperty()
    preisR3 = ObjectProperty()
    preisK3 = ObjectProperty()
    preisS4 = ObjectProperty()
    preisR4 = ObjectProperty()
    preisK4 = ObjectProperty()

    def on_enter(self, *args):
        cur.execute("SELECT id FROM login WHERE username = '%s' " % username)
        id = cur.fetchone()
        id = id[0]
        cur.execute("SELECT * FROM saveshoe WHERE login_ID = '%s' " % id)
        i = cur.fetchall()
        try:
            save = i[0]
            self.saveName1.text = save[1]
            self.preisS1.text = str(save[3])
            self.preisR1.text = str(save[4])
            self.preisK1.text = str(save[5])
        except:
            self.saveName1.text = ""
            self.preisS1.text = ""
            self.preisR1.text = ""
            self.preisK1.text = ""
        try:
            save = i[1]
            self.saveName2.text = save[1]
            self.preisS2.text = str(save[3])
            self.preisR2.text = str(save[4])
            self.preisK2.text = str(save[5])
        except:
            self.saveName2.text = ""
            self.preisS2.text = ""
            self.preisR2.text = ""
            self.preisK2.text = ""
        try:
            save = i[2]
            self.saveName3.text = (save[1])
            self.preisS3.text = str(save[3])
            self.preisR3.text = str(save[4])
            self.preisK3.text = str(save[5])
        except:
            self.saveName3.text = ""
            self.preisS3.text = ""
            self.preisR3.text = ""
            self.preisK3.text = ""
        try:
            save = i[3]
            self.saveName4.text = save[1]
            self.preisS4.text = str(save[3])
            self.preisR4.text = str(save[4])
            self.preisK4.text = str(save[5])
        except:
            self.saveName4.text = ""
            self.preisS4.text = ""
            self.preisR4.text = ""
            self.preisK4.text = ""


pass


class SecondScreen(Screen):
    name_screen2 = ObjectProperty()

    def ChooseSize(self, ausgwGroesse):
        sizes = [35.5, 36, 36.5, 37.5, 38, 38.5, 39, 40, 40.5, 41, 42, 42.5, 43, 44, 44.5, 45, 45.5, 46, 47, 47.5, 48]
        for size in sizes:
            if ausgwGroesse == size:
                global auswahl
                auswahl = sizes.index(size) + 1

    def submitBtn(self, Schuhname, Wunschpreis):
        if auswahl < 9:
            Schuhname = Schuhname + " GS"
        global Daten
        Daten = Start(Schuhname, auswahl, Wunschpreis, auswahl - 1)

    pass


class ThirdScreen(Screen):
    label_screen3 = ObjectProperty()

    def on_enter(self, *args):
        self.label_screen3.text = self.manager.ids.second.name_screen2.text

    def save_shoe(self):
        try:
            cur.execute("SELECT id FROM login WHERE username = '%s' " % username)
            id = cur.fetchone()
            cur.execute(
                "INSERT INTO saveshoe (name, size, pricestockx, pricerestocks, priceklekt, login_id) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (
                    Daten[0], Daten[4], Daten[1], Daten[2], Daten[3], id[0]))
            db.commit()
            self.manager.current = 'save'
        except:
            show_popupFehlerDB()

    pass


class MyScreenManager(ScreenManager):
    pass


widget = Builder.load_string('''
MyScreenManager:
    canvas.before:
        Color:
            rgba: (1,51,61,1)
        Rectangle:
            pos: self.pos
            size: self.size
    FirstScreen:
        id: first
        name: 'first'
    SavesScreen:
        id: save
        name: 'save'
    SecondScreen:
        id: second      
        name: 'second'
    ThirdScreen:
        id: third
        name: 'third'

<FirstScreen>:
    user: user
    password: password
    GridLayout:
        cols: 1
        GridLayout:
            padding: 5
            spacing: 30
            cols:2
            size: root.width-50, root.height-50
            pos: 0,0
            background_color: (1,1,1,1)
            Label:
                color: (0,0,0,1)
                text: "Username:"
            TextInput:
                id: user
                multiline: False
            Label:
                color: (0,0,0,1)
                text: "Passwort:"
            TextInput:
                id: password
                multiline: False
                password: True

        BoxLayout:
            orientation: 'vertical'
            spacing: 20
            background_color: (1,1,1,1)
            Button:
                text: "Login"
                on_press:
                    root.login_user()               
            Button:
                text: "Registrieren"
                on_press: 
                    root.add_user()

<SavesScreen>:
    saveName1: saveName1
    saveName2: saveName2
    saveName3: saveName3
    saveName4: saveName4
    preisS1: preisS1
    preisR1: preisR1
    preisK1: preisK1
    preisS2: preisS2
    preisR2: preisR2
    preisK2: preisK2
    preisS3: preisS3
    preisR3: preisR3
    preisK3: preisK3
    preisS4: preisS4
    preisR4: preisR4
    preisK4: preisK4

    GridLayout:
        padding: 5
        spacing: 20
        cols:1
        size: root.width-50, root.height-50
        pos: 0,0
        Label:
            text: 'Meine gespeicherten Schuhe'
            color: (0,0,0,1)
            font_size: 25
            size_hint_y: 0.2
        GridLayout:
            cols: 2
            Label:
                id: saveName1
                text: saveName1.text
                color: (0,0,0,1)
            BoxLayout:
                Label:
                    id: preisS1
                    text: preisS1.text
                    color: (0,0,0,1)
                Label:
                    id: preisR1
                    text: preisR1.text
                    color: (0,0,0,1)
                Label:
                    id: preisK1
                    text: preisK1.text
                    color: (0,0,0,1)
        GridLayout:
            cols: 2
            Label:
                id: saveName2 
                text: saveName2.text
                color: (0,0,0,1)
            BoxLayout:
                Label:
                    id: preisS2
                    text: preisS2.text
                    color: (0,0,0,1)
                Label:
                    id: preisR2
                    text: preisR2.text
                    color: (0,0,0,1)
                Label:
                    id: preisK2
                    text: preisK2.text
                    color: (0,0,0,1)

        GridLayout:
            background_color: (0.522,0.169,0.788,0.65)
            cols: 2
            Label:
                id: saveName3
                text: saveName3.text
                color: (0,0,0,1)
            BoxLayout:
                Label:
                    id: preisS3
                    text: preisS3.text
                    color: (0,0,0,1)
                Label:
                    id: preisR3
                    text: preisR3.text
                    color: (0,0,0,1)
                Label:
                    id: preisK3
                    text: preisK3.text
                    color: (0,0,0,1)

        GridLayout:
            background_color: (0.522,0.169,0.788,0.65)
            cols: 2
            Label:
                id: saveName4
                text: saveName4.text
                color: (0,0,0,1)
            BoxLayout:
                Label:
                    id: preisS4
                    text: preisS4.text
                    color: (0,0,0,1)
                Label:
                    id: preisR4
                    text: preisR4.text
                    color: (0,0,0,1)
                Label:
                    id: preisK4
                    text: preisK4.text
                    color: (0,0,0,1)            

        Button:
            text: "Zur Suche"
            on_press:
                app.root.current = 'second'


<SecondScreen>: 
    name_screen2: name_screen2 
    GridLayout:
        padding: 5
        spacing: 30
        cols:1
        size: root.width-50, root.height-50
        pos: 0,0
        background_color: (1,1,1,1)

        GridLayout:
            cols:2

            Label:
                text: "Suche nach Schuh:"
                color: (0,0,0,1)

            TextInput:
                id: name_screen2
                multiline: False

            Label:
                text: "Schuhgröße"
                color: (0,0,0,1)

            ScrollView:
                do_scroll_x: False
                do_scroll_y: True

                GridLayout:
                    size:(root.width, root.height)
                    size_hint_y: None
                    cols: 2

                    ToggleButton:
                        text: '35.5 EU'
                        background_normal: ''
                        background_color: (0.522,0.169,0.788,0.65)
                        group: "ausgwGroesse"
                        on_press: root.ChooseSize(35.5)

                    ToggleButton:
                        text: "36 EU"
                        color: (0,0,0,1)
                        background_normal: ''
                        group: "ausgwGroesse"
                        on_press: root.ChooseSize(36)
                    ToggleButton:
                        text: "36.5 EU"
                        color: (0,0,0,1)
                        background_normal: ''
                        group: "ausgwGroesse"
                        on_press: root.ChooseSize(36.5)
                    ToggleButton:
                        text: "37.5 EU"
                        background_normal: ''
                        background_color: (0.522,0.169,0.788,0.65)
                        group: "ausgwGroesse"
                        on_press: root.ChooseSize(37.5)
                    ToggleButton:
                        text: "38 EU"
                        background_normal: ''
                        background_color: (0.522,0.169,0.788,0.65)
                        group: "ausgwGroesse"
                        on_press: root.ChooseSize(38)
                    ToggleButton:
                        text: "38.5 EU"
                        color: (0,0,0,1)
                        background_normal: ''
                        group: "ausgwGroesse"
                        on_press: root.ChooseSize(38.5)
                    ToggleButton:
                        text: "39 EU"
                        color: (0,0,0,1)
                        background_normal: ''
                        group: "ausgwGroesse"
                        on_press: root.ChooseSize(39)
                    ToggleButton:
                        text: "40 EU"
                        background_normal: ''
                        background_color: (0.522,0.169,0.788,0.65)
                        group: "ausgwGroesse"
                        on_press: root.ChooseSize(40)
                    ToggleButton:
                        text: "40.5 EU"
                        background_normal: ''
                        background_color: (0.522,0.169,0.788,0.65)
                        group: "ausgwGroesse"
                        on_press: root.ChooseSize(40.5)
                    ToggleButton:
                        text: "41 EU"
                        color: (0,0,0,1)
                        background_normal: ''
                        group: "ausgwGroesse"
                        on_press: root.ChooseSize(41)
                    ToggleButton:
                        text: "42 EU"
                        color: (0,0,0,1)
                        background_normal: ''
                        group: "ausgwGroesse"
                        on_press: root.ChooseSize(42)
                    ToggleButton:
                        text: "42.5 EU"
                        background_normal: ''
                        background_color: (0.522,0.169,0.788,0.65)
                        group: "ausgwGroesse"
                        on_press: root.ChooseSize(42.5)
                    ToggleButton:
                        text: "43 EU"
                        background_normal: ''
                        background_color: (0.522,0.169,0.788,0.65)
                        group: "ausgwGroesse"
                        on_press: root.ChooseSize(43)
                    ToggleButton:
                        text: "44 EU"
                        color: (0,0,0,1)
                        background_normal: ''
                        group: "ausgwGroesse"
                        on_press: root.ChooseSize(44)
                    ToggleButton:
                        text: "44.5 EU"
                        color: (0,0,0,1)
                        background_normal: ''
                        group: "ausgwGroesse"
                        on_press: root.ChooseSize(44.5)
                    ToggleButton:
                        text: "45 EU"
                        background_normal: ''
                        background_color: (0.522,0.169,0.788,0.65)
                        group: "ausgwGroesse"
                        on_press: root.ChooseSize(45)
                    ToggleButton:
                        text: "45.5 EU"
                        background_normal: ''
                        background_color: (0.522,0.169,0.788,0.65)
                        group: "ausgwGroesse"
                        on_press: root.ChooseSize(45.5)
                    ToggleButton:
                        text: "46 EU"
                        color: (0,0,0,1)
                        background_normal: ''
                        group: "ausgwGroesse"
                        on_press: root.ChooseSize(46)
                    ToggleButton:
                        text: "47 EU"
                        color: (0,0,0,1)
                        background_normal: ''
                        group: "ausgwGroesse"
                        on_press: root.ChooseSize(47)
                    ToggleButton:
                        text: "47.5 EU"
                        background_normal: ''
                        background_color: (0.522,0.169,0.788,0.65)
                        group: "ausgwGroesse"
                        on_press: root.ChooseSize(47.5)
                    ToggleButton:
                        text: "48 EU"
                        background_normal: ''
                        background_color: (0.522,0.169,0.788,0.65)
                        group: "ausgwGroesse"
                        on_press: root.ChooseSize(48)

            Label:
                text: "Wunschpreis:"
                color: (0,0,0,1)

            TextInput:
                id: wunschpreis
                multiline: False


        BoxLayout:
            #cols:2
            orientation: 'vertical'
            spacing: 20

            Button:
                text: "Suche"
                background_normal: ''
                background_color: (0.522,0.169,0.788,0.65)
                on_release:
                    app.root.current = 'third'
                    app.root.transition.direction = "left"
                    root.submitBtn(name_screen2.text, wunschpreis.text)


            Button:
                text: "Zur Wunschliste"
                on_release:
                    app.root.current = 'save'
                    app.root.transition.direction = "right"

            Button:
                text: "Abmelden"
                on_release:
                    app.root.current = 'first'
                    app.root.transition.direction = "right"

<ThirdScreen>:
    label_screen3: label_screen3
    GridLayout:
        cols:1
        Label:
            color: (0,0,0,1)
            background_normal: ''
            font_size: 20
            text: "Diesen Schuh wirklich speichern ?"

        Label:
            id: label_screen3
            color: (0,0,0,1)
            background_normal: ''
            #background_color: (0.522,0.169,0.788,0.65)
            font_size: 40
            text: label_screen3.text

        GridLayout:
            cols: 2
            Button:
                background_normal: ''
                background_color: (0.522,0.169,0.788,0.65)
                text: "Ja"
                on_release:
                    root.save_shoe()


            Button:
                text: "Nein"
                on_release:
                    app.root.current = 'second'

<PLogin>:
    Label:
        text: "Passwort oder Username falsch"
        size_hint: 0.5, 0.5
        pos_hint: {"x": 0.2, "top":1}

<PRegister>:
    Label:
        text: "Username schon vergeben"
        size_hint: 0.5, 0.5
        pos_hint: {"x": 0.2, "top":1}

<PDB>:
    Label:
        text: "Fehler mit der Datenbank"
        size_hint: 0.5, 0.5
        pos_hint: {"x": 0.2, "top":1}

''')


class ScreenManagerApp(App):
    db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="sneakerapp")
    cur = db.cursor()
    cur.execute("""""")
    db.commit()

    def build(self):
        return widget


ScreenManagerApp().run()
