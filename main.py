# import kivymd
# import jnius as jnius
import platform
# import firebase
from kivyauth.google_auth import initialize_google, login_google, logout_google
import firebase_admin
from firebase_admin import credentials
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
    md_bg_color : [1,0,1,1]
    MDCard:
        size_hint : 1, 1
        size: "200dp", "300dp"
        pos_hint : {"center_x":.5, "center_y":.5}
        elevation: 3
        md_bg_color: [99/255, 188/355, 243/355, 1]
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
        MDRoundFlatButton:
            text: "LOGIN"
            text_color: "white"
            line_color: "white"
            pos_hint: {"center_x":.5}
            font_size: 15
            on_press: app.login_callback(email1.text, password1.text)
        MDFloatingActionButton:
            icon: "google"
            pos_hint: {"center_x": .5}
            on_release: app.login()
        MDRoundFlatButton:
            text: "SIGN-UP"
            text_color: "white"
            line_color: "white"
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
        md_bg_color: [99/255, 188/355, 243/355, 1]
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
            text_color: "white"
            line_color: "white"
            pos_hint: {"center_x":.5}
            font_size: 15
            # on_press: app.auth_email(email.text, password.text)
            on_press: app.email_database(email.text, password.text)
            on_press: root.manager.current = 'menu'
        MDRoundFlatButton:
            text: "BACK"
            text_color: "white"
            line_color: "white"
            pos_hint: {"center_x":.5}
            font_size: 15
            on_press: root.manager.current = 'login'
    

<MenuScreen>:
    name: 'menu'
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Heal'm"
            left_action_items: [["menu",lambda x: app.navigation_draw()]]
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
                name: 'screen 1'
                icon: 'cloud'
                on_tab_press: root.manager.get_screen('cloudscreen').bluetooth_discovery()
                on_tab_release: root.manager.current = 'cloudscreen'

            MDBottomNavigationItem:
                name: 'screen 2'
                icon: 'medication'
                on_tab_release: root.manager.current = 'bandageinfo'

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
        text: '* Bandage Info *'
        halign: 'center'
        size_hint_y: 1.8
    MDLabel:
        text: 'Current pH level: 2.3'
        halign: 'center'
        size_hint_y: 1.65
        font_size: 45
        theme_text_color: 'Custom'
        text_color: 0,0,1,1
    MDLabel:
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
        text: 'Your wound is healing!'
        halign: 'center'
        font_size:30
        size_hint_y: .6
        theme_text_color: 'Custom'
        text_color: 0,1,0,1
    MDCard:
        orientation: 'vertical'
        padding: "8dp"
        size_hint: None, None
        size: "200dp", "100dp"
        pos_hint: {"center_x":0.5, "center_y": 0.15}
        elevation: 3
    
        MDLabel:
            font_size: 28
            outline_color: 0,0,0
            outline_width: 1
            text: 'insert bandage specifics here'
            size_hint_y: .4
    
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

        print("Performing inquiry...")

        loop = asyncio.get_event_loop()
        nearby_devices = loop.run_until_complete(discover_devices())

        print("Found {} devices".format(len(nearby_devices)))

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
    pass

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
sm.add_widget(SigninScreen(name = 'signin'))
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(PhoneNumScreen1(name='phonenumbers1'))
sm.add_widget(PhoneNumScreen2(name='phonenumbers2'))


def delete_id(btn_id, numbers, box, btn):
    phonenums = sqlite3.connect('phoneNums')
    c = phonenums.cursor()
    c.execute('DELETE FROM phoneNums WHERE id=?', (btn_id,))
    phonenums.commit()
    numbers.remove_widget(box)

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



    def build(self):
        # self.theme_cls.primary_palette = 'LightBlue'
        # self.theme_cls.accent_palette = 'Blue'
        client_id = open("client_id.txt")
        client_secret = open("client_secret.txt")
        initialize_google(self.after_login, self.error_listener, client_id.read(), client_secret.read())
        screen = Builder.load_string(screen_helper)
        return screen

    def after_login(self):
        pass

    def error_listener(self):
        pass

    def login(self):
        login_google()

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

        for row in rows:
            print(row)

        for i in range(len(rows)):
        # for i in range(30):
            self.items = MDRoundFlatIconButton(text=str(i + 1), icon='bandage', size_hint=(1, 4))
            self.items.bind(on_press=self.pressed)
            self.root.get_screen('menu').ids.container1.add_widget(self.items)
        # on_press = self.root.get_screen('menu').manager.current = 'mainbandage'

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
                  (self.root.get_screen('phonenumbers2').ids.name.text, self.root.get_screen('phonenumbers2').ids.number.text))
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

        #remove old phone numbers
        numbers.clear_widgets()



        defaultnumbers = ["Police/Fire department \n 911", "Poison Control \n 1-800-222-1222", "Animal Poison Control \n 888-426-4435"]

        for i in range(3):
            box = BoxLayout(size_hint = (1, None), size = (0, 70), orientation = 'horizontal')
            box.add_widget(MDRectangleFlatButton(
                text= defaultnumbers[i], size_hint=(0.7, 1)))
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
                text=str(rows[i][1]) + '\n' + str(rows[i][2]), size_hint=(0.7, 1), size = (0, 70), id=str(i + 1))
            button.bind(on_press = lambda instance: self.make_phone_call(rows, i))
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
            call_url =  f"tel:{phone_number}"

        try:
            webbrowser.open(call_url)
        except Exception as e:
            print("Error:", e)

    # def auth_email(self, email, password):
    #     config = {'apiKey': "AIzaSyAnyPC3n3JHYiTDhmfv-K8MKXA51lR1pZ4",
    #       'authDomain': "healm-2-login.firebaseapp.com",
    #       'projectId': "healm-2-login",
    #       'storageBucket': "healm-2-login.appspot.com",
    #       'messagingSenderId': "276399253320",
    #       'appId': "1:276399253320:web:76b70d687e772cf73ab57d",
    #       'measurementId': "G-D06175F6BW"}
    #
    #     # cred = credentials.Certificate('path/to/healm-2-login-firebase-adminsdk-y8yju-81ad5355d3.json')
    #     app = firebase.initialize_app(config)
    #     auth = app.auth()
    #
    #     Email = email
    #     Password = password
    #
    #     user = auth.create_user_with_email_and_password(email, password)


    def email_database(self, email, password):
        # Initialize Firebase
        self.firebase = firebase.FirebaseApplication('https://healm-login-default-rtdb.firebaseio.com/', None)

        # Importing Data
        data ={
            'Email': email,
            'Password': password
        }

        #Post Data
        #Database Name/Table Name
        self.firebase.post('healm-login-default-rtdb/Users', data)

    def verify_login(self, email, password):
        self.firebase = firebase.FirebaseApplication('https://healm-login-default-rtdb.firebaseio.com/', None)

        #Get data
        self.result = self.firebase.get('healm-login-default-rtdb/Users', '')

        #Get Specific column like email or password
        #Verify email and password
        for i in self.result.keys():
            if self.result[i]['Email'] == email:
                if self.result[i]['Password'] == password:
                    return True
                    print(email+ "logged in!")
            else:
                return False

    def login_callback(self, email, password):
        if self.verify_login(email, password):
            self.root.get_screen('login').manager.current = 'menu'
        else:
            # Handle incorrect login here
            print("Invalid credentials")
DemoApp().run()

