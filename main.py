# import kivymd
# import jnius as jnius
import platform

import auth as auth
import requests
import pyrebase
# import firebase
from kivyauth.google_auth import initialize_google, login_google, logout_google
import firebase_admin
from firebase_admin import credentials, initialize_app, auth
from firebase import firebase
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.garden.matplotlib import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.clock import Clock

#: import get_color_from_hex kivy.utils.get_color_from_hex
from kivymd.uix.button import MDRoundFlatIconButton, MDFloatingActionButton, MDRectangleFlatButton, MDFlatButton
from functools import partial

from kivy.utils import platform
import webbrowser
from plyer import call

import bluetooth
import asyncio
import bleak

import sqlite3

# from jnius import autoclass
# from jnius import cast


Window.size = (300, 500)

"""BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
UUID = autoclass('java.util.UUID')


def get_socket_stream(name):
    paired_devices = BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
    socket = None
    recv_stream = ''
    send_stream = ''
    for device in paired_devices:
        if device.getName() == name:
            socket = device.createRfcommSocketToServiceRecord(UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
            recv_stream = socket.getInputStream()
            send_stream = socket.getOutputStream()
            break
    socket.connect()
    return recv_stream, send_stream"""

screen_helper = """
ScreenManager:
    LoginScreen:
    SigninScreen:
    MenuScreen:
    PhoneNumScreen1:
    PhoneNumScreen2:
    CloudScreen:
    BandageInfo:
    MainBandageScreen:

<LoginScreen>:
    name: 'login'
    md_bg_color : [1,0,0,1]
    MDCard:
        size_hint : 1, 1
        size: "200dp", "300dp"
        pos_hint : {"center_x":.5, "center_y":.5}
        elevation: 3
        # md_bg_color: [0, 0, 0, 1]
        # md_bg_color: [99/255, 188/355, 243/355, 1]
        # md_bg_color: [1/255, 6/255, 61/255, 1]
        padding: 20
        spacing: 30
        orientation: "vertical"
        MDLabel : 
            text: 'LOGIN'
            font_style : 'Button'
            font_size : 45
            halign : "center"
            size_hint_y : None
            height : self.texture_size[1]
        MDTextField :
            id: email1
            hint_text: "Email"
            # mode: "round"
            icon_right : "account"
            size_hint_x: None
            width : 220
            font_size: 20
            pos_hint : {"center_x":.5}
            icon_left_color : [1,0,1,1]
            # line_color_focus:1,0,1,1
            # color_active: [1,1,1,1]
        MDTextField:
            id: password1
            hint_text: "Password"
            icon_right: "eye-off"
            size_hint_x: None
            width: 220
            pos_hint: {"center_x":.5}
            # line_color_focus:1,0,1,1
            # color_active:[1,1,1,1]
            password: True
            Image:
                source: "assests/google.png"
                center_x: self.parent.center_x
                center_y: self.parent.center_y
                size: root.width, root.height
        MDRoundFlatButton:
            text: "LOGIN"
            text_color: "blue"
            line_color: "black"
            pos_hint: {"center_x":.5}
            font_size: 15
            on_press: app.login_callback(email1.text, password1.text)
        MDFloatingActionButton:
            icon: "google"
            pos_hint: {"center_x": .5}
            # on_release: app.google_signin("276399253320-eho7bjps4fcq38ni566g2ccihdg5e19h.apps.googleusercontent.com")
            on_release: app.login()
        MDRoundFlatButton:
            text: "SIGN-UP"
            text_color: "blue"
            line_color: "black"
            pos_hint: {"center_x":.5}
            font_size: 15
            on_press: root.manager.current = 'signin'
        Widget:
            size_hint_y : None
            height : 30

<SigninScreen>:
    name: "signin"
    md_bg_color : [1,0,1,1]
    MDCard:
        size_hint : 1, 1
        size: "200dp", "800dp"
        pos_hint : {"center_x":.5, "center_y":.5}
        elevation: 3
        # md_bg_color: [99/255, 188/355, 243/355, 1]
        # md_bg_color: [1/255, 6/255, 61/255, 1]
        padding: 20
        spacing: 30
        orientation: "vertical"
        MDLabel : 
            text: 'SIGN-UP'
            font_style : 'Button'
            font_size : 45
            halign : "center"
            size_hint_y : None
            height : self.texture_size[1]
        MDTextField:
            id: name
            hint_text: "Name"
            icon_right: "account"
            size_hint_x: None
            width: 220
            pos_hint: {"center_x":.5}
            # line_color_focus:1,0,1,1
            # color_active:[1,1,1,1]
        MDTextField :
            id: email
            hint_text: "Email"
            # mode: "round"
            icon_right : "email"
            size_hint_x:None 
            width : 220
            font_size: 20
            pos_hint : {"center_x":.5}
            icon_left_color : [1,0,1,1]
            # line_color_focus:1,0,1,1
            # color_active: [1,1,1,1]
        MDTextField:
            id: password
            hint_text: "Password"
            icon_right: "eye-off"
            size_hint_x: None
            width: 220
            pos_hint: {"center_x":.5}
            # line_color_focus:1,0,1,1
            # color_active:[1,1,1,1]
            password: True
        MDRoundFlatButton:
            text: "SIGN-UP"
            text_color: "blue"
            line_color: "black"
            pos_hint: {"center_x":.5}
            font_size: 15
            on_press: app.auth_email(email.text, password.text)
            # on_press: app.email_database(email.text, password.text)
            on_press: root.manager.current = 'menu'
        MDRoundFlatButton:
            text: "BACK"
            text_color: "blue"
            line_color: "black"
            pos_hint: {"center_x":.5}
            font_size: 15
            on_press: root.manager.current = 'login'


<MenuScreen>:
    name: 'menu'
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Heal'm"
            # left_action_items: [["menu",lambda x: app.navigation_draw()]]
            right_action_items: [["bandage",lambda x: app.navigation_draw()]]
            elevation: 4
        # MDLabel:
        #     text: 'addlist'
        #     halign: 'center'

        # bandages on main screen
        ScrollView:
            size_hint:1,6
            MDGridLayout:
                id: container1
                cols: 3
                padding: [12,12,12,12]
                spacing:[10,10]
                size_hint: None, None
                width: root.width
                height: self.minimum_height


        MDBottomNavigation:
            panel_color: 0,(145/255.0),(237/255.0),1
            text_color_active:get_color_from_hex("F5F5F5")



            MDBottomNavigationItem:
                name: 'screen 2'
                icon: 'cog'
                on_tab_release: root.manager.current = 'bandageinfo'

            MDBottomNavigationItem:
                name: 'screen 1'
                icon: 'cloud'
                on_tab_press: root.manager.get_screen('cloudscreen').bluetooth_discovery()
                on_tab_release: root.manager.current = 'cloudscreen'

            MDBottomNavigationItem:
                name: 'screen 3'
                icon: 'phone'
                #click the button
                # on_tab_release: root.manager.current = 'phonenumbers2'
                on_tab_release: app.go_to_phonenums()

<MainBandageScreen>:
    name: 'mainbandage'
    id: bandages

    MDLabel:
        id: trythis
        text: '* Bandage Info *'
        halign: 'center'
        size_hint_y: 1.8
    MDLabel:
        id: pH
        text: 'Current pH level: 2.3'
        halign: 'center'
        size_hint_y: 1.65
        font_size: 45
        theme_text_color: 'Custom'
        text_color: 0,0,1,1
    MDLabel:
        id: location
        text: 'Bandage Location: Shoulder'
        halign:'center'
        font_size: 25
        size_hint_y: 1.48
    MDLabel:
        text: 'History of Wound (Past 7 Days)'
        halign: 'center'
        font_size: 25
        size_hint_y: 1.41
    BoxLayout:
        orientation: 'vertical'
        id: graph_container
        # size_hint_y: .3
        # height: "20"
    MDLabel:
        id: woundstatus
        text: 'Your wound is healing!'
        halign: 'center'
        font_size:30
        size_hint_y: .6
        theme_text_color: 'Custom'
        text_color: 0,1,0,1
    MDLabel:
        id: woundinfo
        text: '*Below 7- wound is doing okay \\n *7- borderline healing/getting worse \\n *Above 7- wound is not well'
        halign: 'center'
        font_size: 22
        size_hint_y: .45
        theme_text_color:
    # MDCard:
    #     orientation: 'vertical'
    #     padding: "8dp"
    #     size_hint: None, None
    #     size: "200dp", "100dp"
    #     pos_hint: {"center_x":0.5, "center_y": 0.15}
    #     elevation: 0

    MDFlatButton:
        pos_hint: {"center_x":0.5, "center_y": 0.15}
        font_size: 23
        theme_text_color:"Custom"
        text_color: "blue"
        text: 'Click here for more information.'
        size_hint_y: 0.25
        on_release:
            import webbrowser
            
            webbrowser.open('https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10182338')

    MDIconButton:
        icon:'arrow-left'
        pos_hint: {"center_x": 0.090, "center_y": 0.95}
        on_press: root.manager.current = 'menu'

<BandageInfo>:
    name: 'bandageinfo'
    id: container2
    MDIconButton:
        icon:'home-account'
        pos_hint: {"center_x": 0.5, "center_y": 0.95}
        on_press: root.manager.current = 'menu'
    MDRectangleFlatButton:
        text: "Log-out"
        text_color: "blue"
        line_color: "blue"
        pos_hint: {"center_x": 0.5, "center_y": 0.8}
        size_hint: (0.5, None)
        size: (200, 100)
        on_press: app.pressed_login()
        on_press: root.manager.current = 'login'
    MDRectangleFlatButton:
        text: "Reset Password"
        text_color: "blue"
        line_color: "blue"
        pos_hint: {"center_x": 0.5, "center_y": 0.7}
        size_hint: (0.5, None)
        size: (200, 100)
        on_press: app.pressed_login()
        on_press: root.manager.current = 'login'
    MDRectangleFlatButton:
        text: "Delete Account"
        text_color: "blue"
        line_color: "blue"
        pos_hint: {"center_x": 0.5, "center_y": 0.6}
        size_hint: (0.5, None)
        size: (200, 100)
        # self.root.get_screen('login').ids.email1.text = ''
        # self.root.get_screen('login').ids.password1.text = ''
        on_press: app.delete_account()
        on_press: app.pressed_login()
        on_press: root.manager.current = 'login'


<CloudScreen>:
    name: 'cloudscreen'
    id: container3

    MDIconButton:
        icon:'arrow-right'
        pos_hint: {"center_x": 0.92, "center_y": 0.95}
        on_press: root.manager.current = 'menu'

    ScrollView:  # Add ScrollView to wrap the container
        size_hint_y: 0.9  # Make the ScrollView take 90% of the available height
        pos_hint: {'top': 0.9}  # Position it below the top bar

        GridLayout:
            id: container3  # Give the GridLayout the same ID as the parent screen
            cols: 1  # Set the number of columns to 1
            padding: [12, 12, 12, 12]
            spacing: [10, 10]
            size_hint_y: None  # Disable height size_hint
            height: self.minimum_height  # Set a fixed height to allow scrolling


<PhoneNumScreen1>:
    name: 'phonenumbers1'
    id: container
    MDIconButton:
        icon: 'plus'
        pos_hint: {"center_x":0.92, "center_y":0.95}
        on_press: root.manager.current = 'phonenumbers2'
    MDIconButton:
        icon:'arrow-left'
        pos_hint: {"center_x": 0.090, "center_y": 0.95}
        on_press: root.manager.current = 'menu'
    ScrollView:
        size_hint:1,0.9
        pos_hint: {'top': 0.9}

        BoxLayout: 
            size_hint: None, None
            id: numbers
            width: root.width
            height: self.minimum_height
            pos_hint: {'center_x': .5, 'center_y': .5}
            orientation: 'vertical'
            padding: [12,12,12,12]
            spacing: 10
            MDRectangleFlatButton:
                text: 'Police/Fire department \\n 911'
                size_hint: (1,0.05)
            MDRectangleFlatButton:
                text: 'Poison Control \\n 1-800-222-1222'
                size_hint: (1,0.05)
            MDRectangleFlatButton:
                text: 'Animal Poison Control \\n 888-426-4435'
                size_hint: (1,0.05)

<PhoneNumScreen2>:
    name: 'phonenumbers2'
    #input line
    GridLayout:
        id: phonescreen2
    MDTextField:
        id: name
        hint_text: "Enter Name:"
        pos_hint: {'center_x': 0.5, 'center_y':0.55}
        size_hint_x: 0.8
        width: 300
    MDTextField:
        id: number #providing id to text field
        hint_text: "Enter phone number:"
        helper_text: "(emergency contacts)"
        helper_text_mode: "on_focus"
        input_filter: 'int'
        icon_right: "phone-alert"
        #color_mode = 'accent'
        #line_color_number:1,1,1,1 -->use this if you want to change line color
        pos_hint: {'center_x':0.5, 'center_y': 0.4}
        #makes line bigger for input
        size_hint_x: 0.8
        width: 300

    # enter button
    MDRectangleFlatButton:
        text: 'Enter'
        pos_hint:{'center_x':0.5, 'center_y':0.2}
        on_press: app.get_data()
        # on_press: name.text = ''
        # on_press: number.text = ''

    MDIconButton:
        icon:'arrow-left'
        pos_hint: {"center_x": 0.090, "center_y": 0.95}
        on_press: root.manager.current = 'phonenumbers1'

"""


class LoginScreen(Screen):
    pass


class SigninScreen(Screen):
    pass


class MenuScreen(Screen):
    pass


class CloudScreen(Screen):

    def bluetooth_discovery(self):
        async def discover_devices():
            devices = await bleak.discover()
            return devices

        # print("Performing inquiry...")

        loop = asyncio.get_event_loop()
        nearby_devices = loop.run_until_complete(discover_devices())

        # print("Found {} devices".format(len(nearby_devices)))

        grid_layout = self.ids.container3
        grid_layout.clear_widgets()

        for device in nearby_devices:
            try:
                label_text = "{} - {}".format(device.address, device.name)
            except UnicodeEncodeError:
                label_text = "{} - {}".format(device.address, device.name.encode("utf-8", "replace"))

            button = MDRectangleFlatButton(text=label_text, size_hint=(1, 0.05))
            grid_layout.add_widget(button)


class BandageInfo(Screen):

    # self.root.get_screen('login').ids.email1.text = ''
    # self.root.get_screen('login').ids.password1.text = ''
    def get_email(self):
        email = self.root.get_screen('login').ids.email1.text
        return email
    def get_pass(self):
        password = self.root.get_screen('login').ids.password1.text
        return password



class PhoneNumScreen1(Screen):
    pass


class PhoneNumScreen2(Screen):
    pass


class MainBandageScreen(Screen):
    def generate_bar_graph(self):
        x = ["7/09/23", "7/10/23", "7/11/23", "7/12/23", "7/13/23", "7/14/23", "7/15/23"]
        y = [0, 5, 10, 15, 20, 25, 30]

        fig, ax = plt.subplots()
        ax.bar(x, y)

        # plt.ylabel("Level")
        # plt.xlabel("Days")

        plot_widget = FigureCanvasKivyAgg(fig)

        self.ids.graph_container.clear_widgets()
        self.ids.graph_container.add_widget(plot_widget)
        graph_container = self.ids.graph_container
        graph_container.size_hint_y = None  # Disable height size_hint
        graph_container.height = "150dp"  # Set a fixed height (you can adjust the value as needed)
        graph_container.pos_hint = {"center_x": 0.5, "center_y": 0.5}  # Center the container


sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(SigninScreen(name='signin'))
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(PhoneNumScreen1(name='phonenumbers1'))
sm.add_widget(PhoneNumScreen2(name='phonenumbers2'))


def delete_id(btn_id, numbers, box, btn):
    phonenums = sqlite3.connect('phoneNums')
    c = phonenums.cursor()
    c.execute('DELETE FROM phoneNums WHERE id=?', (btn_id,))
    phonenums.commit()
    numbers.remove_widget(box)

def load_bandage_info(i, screen, btn):
    print(i)
    bandages = sqlite3.connect('bandages')
    c = bandages.cursor()
    c.execute("SELECT * FROM bandages")

    rows = c.fetchall()
    for row in rows:
        print(row)

    screen.ids.pH.text = "Current pH Level: " + str(rows[i][3])
    screen.ids.location.text = "Bandage Location: " + str(rows[i][1])
    if (rows[i][3] < 7):
        screen.ids.woundstatus.text = "Your wound is healing!"
        screen.ids.woundstatus.text_color= (0,1,0,1)
    elif (rows[i][3]>= 7):
        screen.ids.woundstatus.text = "Go see a doctor"
        screen.ids.woundstatus.text_color= (255/255,216/255,0,1)
    screen.manager.current = 'mainbandage'
# def call_num(num, self):
#     intent = autoclass('android.net.Uri')
#     uri = autoclass('android.net.Uri')
#     pythonactivity = autoclass('org.renpy.android.PythonActivity')
#     intent = intent(intent.ACTION_CALL)
#     intent.setData(uri.parse("tel:" + num))
#     currentactivity = cast('android.app.Activity', pythonactivity.mActivity)
#     currentactivity.startActivity(intent)


class DemoApp(MDApp):
    """phoneNums = sqlite3.connect('phoneNums')
    c = phoneNums.cursor()
    c.execute('DROP TABLE phoneNums')
    c.execute(''' CREATE TABLE IF NOT EXISTS phoneNums
                ([id] INTEGER PRIMARY KEY AUTOINCREMENT,
                 [name] TEXT, [number] INTEGER)
                 ''')
    phoneNums.commit()

    bandages = sqlite3.connect('bandages')

    c = bandages.cursor()

    c.execute('''
                    CREATE TABLE IF NOT EXISTS bandages
                    ([bandage_id] INTEGER PRIMARY KEY,
                [name] TEXT, [uric_acid] DOUBLE, [pH] DOUBLE)
                ''')

    c.execute('''
                INSERT OR REPLACE INTO bandages(bandage_id, name,
                uric_acid, pH)

                            VALUES
                            (1,'Arm', 0, 7),
                            (2,'Leg', 0.5 , 8),
                            (3,'Chest', 0.6, 6.7),
                            (4,'Knee', 1, 7.5),
                            (5,'Shoulder', 0.2, 7.1)
                ''')
    bandages.commit()"""
    pyrebaseconfig = {
        "apiKey": "AIzaSyAnyPC3n3JHYiTDhmfv-K8MKXA51lR1pZ4",
        "authDomain": "healm-2-login.firebaseapp.com",
        "databaseURL": "https://databaseName.firebaseio.com",
        "storageBucket": "healm-2-login.appspot.com"
    }
    userEmail = ''
    userId = ''

    def build(self):
        # self.theme_cls.primary_palette = 'LightBlue'
        # self.theme_cls.accent_palette = 'Blue'
        # trying to add the google log in stuff
        client_id = open("client_id.txt")
        client_secret = open("client_secret.txt")
        initialize_google(self.after_login, self.error_listener, client_id.read(), client_secret.read())

        screen = Builder.load_string(screen_helper)
        return screen

    def after_login(self, name, email, photo_uri):
        self.root.ids.label.text = f"Logged in as {name}"
        self.root.transtion.direction = "left"
        self.root.get_screen('login').manager.current = 'menu'
        # self.root.current = "menu"


    def error_listener(self):
        print("Login Failed!")


    def login(self):
        login_google()


    def logout(self):
        logout_google(self.after_logout())

    def after_logout(self):
        self.root.ids.label.text = ""
        self.root.transtion.direction = "right"
        # self.root.current = "login"


    # clearing login stuff once login so when you log out its not there
    def pressed_login(self):

        self.root.get_screen('login').ids.email1.text = ''
        self.root.get_screen('login').ids.password1.text = ''

    # adding the bandages onto screen

    # what happens when press one of the bandage icons
    def pressed(self, *args):
        self.root.get_screen('menu').manager.current = 'mainbandage'
        self.root.get_screen('mainbandage').generate_bar_graph()

    # creating the bandage icons
    def on_start(self):
        # scroll = ScrollView()
        # list_view = MDList()

        bandages = sqlite3.connect('bandages')
        c = bandages.cursor()
        c.execute('''
                            CREATE TABLE IF NOT EXISTS bandages
                            ([bandage_id] INTEGER PRIMARY KEY,
                        [name] TEXT, [uric_acid] DOUBLE, [pH] DOUBLE)
                        ''')
        c.execute("SELECT * FROM bandages")
        bandages.commit()
        rows = c.fetchall()

        wound = ['Your wound is healing!', 'Go see a doctor', 'Your wound is healing', 'Go see a doctor',
                 'Your wound is healing!']
        location = ['Shoulder', 'Knee', 'Hand', 'Elbow', 'Foot']
        pHlevel = ['2.3000', '7.222', '2.3000', '7.222', '2.3000']

        for row in rows:
            print(row)

        for i in range(len(rows)):
            # for i in range(30):
            # creating the bandages
            button = MDRoundFlatIconButton(text=str(i + 1), icon='bandage', size_hint=(1, 4), id=str(i),
                                           on_press=partial(load_bandage_info, i, self.root.get_screen('mainbandage')))
            self.root.get_screen('menu').ids.container1.add_widget(button)
            self.root.get_screen('mainbandage').generate_bar_graph()
    # saving phonenumbers once entered by user
    def get_data(self):

        phonenums = sqlite3.connect('phoneNums')
        c = phonenums.cursor()
        # c.execute(''' CREATE TABLE IF NOT EXISTS phoneNums
        #                 ([id] INTEGER PRIMARY KEY AUTOINCREMENT,
        #                  [name] TEXT, [number] INTEGER)
        #                  ''')
        c.execute(''' INSERT INTO phoneNums (name, number)
                    VALUES (?,?)''',
                  (self.root.get_screen('phonenumbers2').ids.name.text,
                   self.root.get_screen('phonenumbers2').ids.number.text))
        phonenums.commit()
        self.go_to_phonenums()

        if ((self.root.get_screen('phonenumbers2').ids.name.text == '') & (
                self.root.get_screen('phonenumbers2').ids.number.text == '')):
            print('invalid')
        elif (self.root.get_screen('phonenumbers2').ids.name.text == ''):
            print('invalid')

        elif (self.root.get_screen('phonenumbers2').ids.number.text == ''):
            print("hola")
        else:
            # self.root.get_screen('phonenumbers1').ids.numbers.add_widget(MDRectangleFlatButton(text=self.root.get_screen('phonenumbers2').ids.name.text + '\n'+self.root.get_screen('phonenumbers2').ids.number.text,size_hint=(1,0.05)))
            self.root.get_screen('phonenumbers2').ids.number.text = ''
            self.root.get_screen('phonenumbers2').ids.name.text = ''
            # self.root.get_screen('phonenumbers2').manager.current = 'phonenumbers1'
        # print(self.root.get_screen('phonenumbers2').ids.data2.text) # address of textfield in kivy
        #     self.go_to_phonenums()

    def go_to_phonenums(self):

        numbers = self.root.get_screen('phonenumbers1').ids.numbers

        # remove old phone numbers
        numbers.clear_widgets()

        defaultnumbers = ["Police/Fire department \n 911", "Poison Control \n 1-800-222-1222",
                          "Animal Poison Control \n 888-426-4435"]

        for i in range(3):
            box = BoxLayout(size_hint=(1, None), size=(0, 70), orientation='horizontal')
            box.add_widget(MDRectangleFlatButton(
                text=defaultnumbers[i], size_hint=(0.7, 1)))
            box.add_widget(MDRectangleFlatButton(text='-', text_color='gray', line_color='gray', size_hint=(None, 1),
                                                 size=(50, 70)))
            numbers.add_widget(box)

        phonenums = sqlite3.connect('phoneNums')
        c = phonenums.cursor()
        c.execute("SELECT * FROM phoneNums")
        rows = c.fetchall()

        for i in range(len(rows)):
            box = BoxLayout(size_hint=(1, None), size=(0, 70), orientation='horizontal')
            button = MDRectangleFlatButton(
                text=str(rows[i][1]) + '\n' + str(rows[i][2]), size_hint=(0.7, 1), size=(0, 70), id=str(i + 1))
            button.bind(on_press=lambda instance: self.make_phone_call(rows, i))
            box.add_widget(button)
            remove_button = MDRectangleFlatButton(
                text='-', text_color='red', line_color='red', size_hint=(None, 1), size=(50, 70),
                on_press=partial(delete_id, rows[i][0], numbers, box))
            box.add_widget(remove_button)
            numbers.add_widget(box)

        self.root.get_screen('phonenumbers1').manager.current = 'phonenumbers1'

    def make_phone_call(self, rows, index):
        # formatted_phone_number = ''.join(filter(str.isdigit, phone_number))
        phone_number = rows[index][2]

        if platform == 'android':
            call.makecall(phone_number)
        else:
            call_url = f"tel:{phone_number}"

        try:
            webbrowser.open(call_url)
        except Exception as e:
            print("Error:", e)

    def auth_email(self, email, password):
        """config = {'apiKey': "AIzaSyAnyPC3n3JHYiTDhmfv-K8MKXA51lR1pZ4",
                  'authDomain': "healm-2-login.firebaseapp.com",
                  'projectId': "healm-2-login",
                  'storageBucket': "healm-2-login.appspot.com",
                  'messagingSenderId': "276399253320",
                  'appId': "1:276399253320:web:76b70d687e772cf73ab57d",
                  'measurementId': "G-D06175F6BW"}"""

        firebase = pyrebase.initialize_app(DemoApp.pyrebaseconfig)

        auth2 = firebase.auth()

        DemoApp.userEmail = email  # input("Please Enter Your Email Address : \n")
        # password = password5  # getpass("Please Enter Your Password : \n")

        # create users
        user = auth2.create_user_with_email_and_password(email, password)
        print("Success .... ")

        # login = auth2.sign_in_with_email_and_password(email, password)

        # send email verification
        auth2.send_email_verification(user['idToken'])

        """auth_obj = auth
        cred = credentials.Certificate(r"json_file.json")
        firebase_admin.initialize_app(cred)
        # app = initialize_app(cred)
        # app = firebase.initialize_app(config)
        # auth = app.auth()

        # google_provider = firebase.auth.GoogleAuthProvider()
        # user1 = auth.sign_in_with_popup(google_provider)

        Email = email5
        Password = password5

        authenticate = firebase.auth()
        auth.send_email_verification(login['idToken'])

        user = auth.create_user(
            email = Email,
            password = Password
        )"""


    # def email_database(self, email, password):
    #     # Initialize Firebase
    #     self.firebase = firebase.FirebaseApplication('https://healm-login-default-rtdb.firebaseio.com/', None)
    #
    #     # Importing Data
    #     data = {
    #         'Email': email,
    #         'Password': password

    #     }
    #
    #     # Post Data
    #     # Database Name/Table Name
    #     self.firebase.post('healm-login-default-rtdb/Users', data)

    def verify_login(self, email, password):
        # self.firebase = firebase.FirebaseApplication('https://healm-login-default-rtdb.firebaseio.com/', None)

        # Get data
        # self.result = self.firebase.get('healm-login-default-rtdb/Users', '')
        api_key = "AIzaSyAnyPC3n3JHYiTDhmfv-K8MKXA51lR1pZ4"
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
        data = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            login_data = response.json()
            print("Successfully logged in with UID:", login_data['localId'])
            firebase = pyrebase.initialize_app(DemoApp.pyrebaseconfig)

            auth2 = firebase.auth()

            DemoApp.userEmail = email

            # create users

            user = auth2.sign_in_with_email_and_password(email, password)
            user_info = auth2.get_account_info(user['idToken'])
            print(user_info)
            print(user_info['users'][0])
            if not user_info['users'][0]['emailVerified']:
                print("not verified")
                return False

            # send email verification
            print("All good!")
            auth2.send_password_reset_email(email)
            return True
            # login = auth.sign_in_with_email_and_password(email, password)
            # login = 'correct'
            # return True
        except requests.exceptions.RequestException as e:
            print("Login failed with error:", str(e))
            return False

        # if login == 'correct':
        #     return True
        # else:
        #     return False

        # Get Specific column like email or password
        # Verify email and password
        # for i in self.result.keys():
        #     if self.result[i]['Email'] == email:
        #         if self.result[i]['Password'] == password:
        #             return True
        #             print(email + "logged in!")
        #     else:
        #         return False

    def login_callback(self, email, password):
        if self.verify_login(email, password):
            self.root.get_screen('login').manager.current = 'menu'
        else:
            # Handle incorrect login here
            print("Invalid credentials")

    # def verify_login(self, email, password):
    #     # self.firebase = firebase.FirebaseApplication('https://healm-login-default-rtdb.firebaseio.com/', None)
    #
    #     # Get data
    #     # self.result = self.firebase.get('healm-login-default-rtdb/Users', '')
    #     api_key = "AIzaSyAnyPC3n3JHYiTDhmfv-K8MKXA51lR1pZ4"
    #     url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    #     data = {
    #         "email": email,
    #         "password": password,
    #         "returnSecureToken": True
    #     }
    #
    #     # auth_obj = auth
    #     # cred = credentials.Certificate(
    #     #     r"C:\Users\Dana\Desktop\androidapp\healm-2-login-firebase-adminsdk-y8yju-243fa8f58d.json")
    #     # firebase_admin.initialize_app(cred)
    #
    #     try:
    #         response = requests.post(url, json=data)
    #         response.raise_for_status()
    #         login_data = response.json()
    #         # user = auth.get_user('user_uid')
    #         # print("Trying: ",user.toJSON())
    #         # print("Logged in with email:", login_data['email'])
    #         print("Successfully logged in with UID:", login_data['localId'])
    #         return True
    #         # login = auth.sign_in_with_email_and_password(email, password)
    #         # login = 'correct'
    #         # return True
    #     except requests.exceptions.RequestException as e:
    #         print("Login failed with error:", str(e))
    #         return False
    #

    def delete_account(self):

        # self.root.get_screen('login').ids.email1.text = ''
        # self.root.get_screen('login').ids.password1.text = ''

        email = self.root.get_screen('login').ids.email1.text
        password = self.root.get_screen('login').ids.password1.text

        api_key = "AIzaSyAnyPC3n3JHYiTDhmfv-K8MKXA51lR1pZ4"
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
        data = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        response = requests.post(url, json = data)
        response_data = response.json()
        user_uid = response_data["localId"]

        # if "localId" in response_data:
        #     user_uid = response_data["localId"]
        #     return user_uid
        # else:
        #     error_message = response_data.get("error", {}).get("message", "Unknown error")
        #     return None

        email =self.root.get_screen('login').ids.email1.text
        password = self.root.get_screen('login').ids.password1.text

        # firebase.delete(login_data['localId'], None)

        try:
            cred = credentials.Certificate(
                r"C:\Users\Dana\Desktop\androidapp\healm-2-login-firebase-adminsdk-y8yju-243fa8f58d.json")
            firebase_admin.initialize_app(cred)

            # user = auth.get_user_by_email(email)
            # claims = auth.verify_id_token(password)
            auth.delete_user(user_uid)

        except ValueError as e:
            print(f"Error deleting user: {e}")

        except Exception as e:
            print(f"Other error occurred: {e}")



        # Get Specific column like email or password
        # Verify email and password
        # for i in self.result.keys():
        #     if self.result[i]['Email'] == email:
        #         if self.result[i]['Password'] == password:
        #             return True
        #             print(email + "logged in!")
        #     else:
        #         return False


DemoApp().run()

