# import kivymd
# import jnius as jnius
import platform

import auth as googleauth
import requests
import pyrebase
# import firebase
from datetime import date, timedelta
from kivyauth.google_auth import initialize_google, login_google, logout_google
import firebase_admin
from firebase_admin import credentials, initialize_app, auth, db
from firebase import firebase
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock
from kivy.garden.matplotlib import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import datetime
import numpy as np
from matplotlib.dates import drange, DateFormatter



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
import json
import random
#from PyObjCTools import KeyValueCoding

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
        MDLabel:
            id: errorLabel
            text: ""
            halign: "center"
            theme_text_color: "Custom"
            text_color: "red"
        MDRoundFlatButton:
            text: "LOGIN"
            text_color: "blue"
            line_color: "black"
            pos_hint: {"center_x":.5}
            font_size: 15
            on_press: app.login_callback(email1.text, password1.text)
        # MDFloatingActionButton:
        #     icon: "google"
        #     pos_hint: {"center_x": .5}
        #     # on_release: app.google_signin("276399253320-eho7bjps4fcq38ni566g2ccihdg5e19h.apps.googleusercontent.com")
        #     on_release: app.login()
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
            #on_press: root.manager.current = 'menu'
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
        text: 'pH Level: 2.3'
        halign: 'center'
        size_hint_y: 1.60
        font_size: 45
        theme_text_color: 'Custom'
        text_color: 0,0,1,1
    # MDLabel:
    #     id: location
    #     text: 'Bandage Location: Shoulder'
    #     halign:'center'
    #     font_size: 25
    #     size_hint_y: 1.48
    MDLabel:
        text: 'History of Wound (Past 7 Days)'
        halign: 'center'
        font_size: 25
        size_hint_y: 1.41
    BoxLayout:
        orientation: 'vertical'
        id: graph_container
        size_hint_y: .3
        #padding: 1.5
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
        on_press: app.reset_password()
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
    def __init__(self, **kwargs):
        super(CloudScreen, self).__init__(**kwargs)
        self.devices = []
        self.connected_device = None


    # look up a certain bluetooth device
    #target_name == bluetooth.lookup_name( bdaddr )

    def bluetooth_discovery(self):
        print("test")

        async def discover_devices():
            try:
                nearby_devices = await bleak.discover()


                # print("Found {} devices".format(len(nearby_devices)))

                grid_layout = self.ids.container3
                grid_layout.clear_widgets()

                for device in nearby_devices:
                    try:
                        label_text = "{} - {}".format(device.address, device.name)
                    except UnicodeEncodeError:
                        label_text = "{} - {}".format(device.address, device.name.encode("utf-8", "replace"))

                    button = MDRectangleFlatButton(text=label_text, size_hint=(1, 0.05))
                    if device.name is not None and "Bandage" in device.name:
                        connect_to = device
                        button.bind(on_press = lambda instance, device= device: self.connect_device(device))
                    grid_layout.add_widget(button)
            except Exception as e:
                print(f"Exception: {e}")
                return None

        asyncio.create_task(discover_devices())

    def connect_device(self, connect_to):
        """async def connect():
            async with bleak.BleakClient(connect_to) as client:
                svcs = await client.get_services()
                print("Services: ")
                for service in svcs:
                    print(service)
                self.connected_device = connect_to
                # await asyncio.sleep(1)
                # Perform your communication with the device here

        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(connect())
        asyncio.run(connect())"""
        """exists = False
        for bandage in DemoApp.bandages:
            if connect_to == bandage:
                exists = True
                DemoApp.bandages.remove(bandage)
        if exists:"""
        #DemoApp.bandages.append(connect_to.address)
        DemoApp.bandages[connect_to.address] = -1
        DemoApp.bandages_prev_data[connect_to.address] = [0,0,0,0,0,0,0]
        bandage_ref = db.reference(f"users/{DemoApp.uid}/bandages/{connect_to.address}")

        uuid_battery_service = '0000180f-0000-1000-8000-00805f9b34fb'
        uuid_battery_level_characteristic = '00002a19-0000-1000-8000-00805f9b34fb'
        uuid_uart_service = '12340001-0000-1000-8000-00805f9b34fb'

        async def connect():
            try:
                async with bleak.BleakClient(connect_to) as client:
                    """svcs = await client.get_services()
                    for service in svcs:
                        print(service)
                        for characteristic in svcs.characteristics.items():
                            print(characteristic[1].uuid)
                            print(characteristic[1].description)
                            print(characteristic[1].properties)
                        print("")"""
                    bluetooth_value = str(await client.read_gatt_char(uuid_uart_service), "utf-8")
                    bandage_ref.set({"name": connect_to.name,
                                     "pH": bluetooth_value,
                                     "uic acid": "1"})
                    print(bluetooth_value)
                    DemoApp.bandages[connect_to.address] = bluetooth_value
                    DemoApp.bandages_prev_data[connect_to.address][6] = bluetooth_value
                    DemoApp.set_bandage_buttons(self)
                    #print(int.from_bytes(battery_level, byteorder='little'))
                    #print(battery_level.decode())
                    return None
            except Exception as e:
                print(f"Exception: {e}")
                return None

        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(connect())
        asyncio.create_task(connect())

    def show_connected_popup(self, device_address):
        content = Label(text = f"Connected to {device_address}")
        popup = Popup(title = "Device Connected", content = content, size_hint=(None, None), size = (300, 200))
        popup.open()


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
        screen = DemoApp.screen_manager.get_screen('mainbandage')
        today = date.today()
        date2 = (today + datetime.timedelta(days=1))

        date1 = (today + datetime.timedelta(days=-6))

        # date1 = datetime.datetime(element1, element2, element3)
        delta = datetime.timedelta(hours=24)
        dates = drange(date1, date2, delta)

        #x = ["7/09/23", "7/10/23", "7/11/23", "7/12/23", "7/13/23", "7/14/23", "7/15/23"]
        #y = [0, 5, 10, 15, 20, 25, 30]
        #if DemoApp.cur_bandage != None:
        y = list(map(float, DemoApp.bandages_prev_data[DemoApp.cur_bandage]))#[0, 5, 10, 15, 20, 25, 30]

        # y = np.arange(len(dates))

        fig, ax = plt.subplots()
        ax.plot_date(dates, y)
        plt.xticks(rotation=8)
        date_form = DateFormatter("%m-%d")
        ax.xaxis.set_major_formatter(date_form)

        # fig, ax = plt.subplots()
        #plt.plot_date(x,y,xdate=True)
        # ax.plot(dates, y)

        plot_widget = FigureCanvasKivyAgg(fig, size_hint_y=0.8)

        screen.ids.graph_container.clear_widgets()
        screen.ids.graph_container.add_widget(plot_widget)
        graph_container = screen.ids.graph_container
        #graph_container.size_hint_y = None  # Disable height size_hint

        #graph_container.height = "150dp"  # Set a fixed height (you can adjust the value as needed)
        graph_container.pos_hint = {"center_x": 0.5, "center_y": 0.5}  # Center the container


sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(SigninScreen(name='signin'))
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(PhoneNumScreen1(name='phonenumbers1'))
sm.add_widget(PhoneNumScreen2(name='phonenumbers2'))
sm.add_widget(MainBandageScreen(name='mainbandage'))


def delete_id(btn_id, numbers, box, btn):
    phone_ref = db.reference(f"users/{DemoApp.uid}/phoneNums")
    phone_ref.child(btn_id).delete()
    numbers.remove_widget(box)


def load_bandage_info(bandage, screen, btn):
    bandage_ref = db.reference(f"users/{DemoApp.uid}/bandages")
    rows = str(bandage_ref.get())
    if rows != "None":
        rows = json.loads(str(bandage_ref.get()).replace('\'', '"'))

        if float(DemoApp.bandages[bandage]) < 0:
            screen.ids.pH.text = "pH Level: " + str(rows[bandage]['pH'])
        else:
            screen.ids.pH.text = "pH Level: " + str(DemoApp.bandages[bandage])


        if float(rows[bandage]['pH']) < 7:
            screen.ids.woundstatus.text = "Your wound is healing!"
            screen.ids.woundstatus.text_color = (0, 1, 0, 1)
        elif float(rows[bandage]['pH']) >= 7:
            screen.ids.woundstatus.text = "Your doctor would like to see you!"
            screen.ids.woundstatus.text_color = (255 / 255, 216 / 255, 0, 1)
    DemoApp.cur_bandage = bandage
    DemoApp.screen_manager.get_screen('mainbandage').generate_bar_graph()
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
    pyrebaseconfig = {
        "apiKey": "AIzaSyAnyPC3n3JHYiTDhmfv-K8MKXA51lR1pZ4",
        "authDomain": "healm-2-login.firebaseapp.com",
        "databaseURL": "https://healm-2-login-default-rtdb.firebaseio.com/",
        "storageBucket": "healm-2-login.appspot.com"
    }
    #firebase_admin.initialize_app()
    firebase = pyrebase.initialize_app(pyrebaseconfig)
    #db = firebase.database()
    firebase_auth = firebase.auth()
    user = {}
    email = ""
    uid = ""
    cred = credentials.Certificate(
        r"json_file.json")
    firebase_admin.initialize_app(cred, {'databaseURL': "https://healm-2-login-default-rtdb.firebaseio.com/"})
    ref = db.reference("/")
    bandages = {}
    bandages_prev_data = {}
    cur_bandage = None
    screen_manager = None

    def build(self):
        # self.theme_cls.primary_palette = 'LightBlue'
        # self.theme_cls.accent_palette = 'Blue'
        # trying to add the google log in stuff
        client_id = open("client_id.txt")
        client_secret = open("client_secret.txt")
        initialize_google(self.after_login, self.error_listener, client_id.read(), client_secret.read())

        screen = Builder.load_string(screen_helper)
        DemoApp.screen_manager = screen

        #Clock.schedule_interval(self.read_data_loop_sync, 10)
        return screen

    async def connect(self):
        uuid_uart_service = '12340001-0000-1000-8000-00805f9b34fb'
        for bandage in DemoApp.bandages:
            print(bandage)
            try:
                async with bleak.BleakClient(bandage) as client:
                    """svcs = await client.get_services()
                    for service in svcs:
                        print(service)
                        for characteristic in svcs.characteristics.items():
                            print(characteristic[1].uuid)
                            print(characteristic[1].description)
                            print(characteristic[1].properties)
                        print("")"""
                    bluetooth_value = str(await client.read_gatt_char(uuid_uart_service), "utf-8")
                    DemoApp.bandages[bandage] = bluetooth_value
                    i = 0
                    while i < 6:
                        DemoApp.bandages_prev_data[bandage][i] = DemoApp.bandages_prev_data[bandage][i+1]
                        i += 1
                    DemoApp.bandages_prev_data[bandage][6] = bluetooth_value
                    if DemoApp.cur_bandage == bandage:
                        #DemoApp.screen_manager.get_screen("mainbandage").ids.pH.text = bluetooth_value
                        Clock.schedule_once(lambda dt: self.update_pH(bluetooth_value), 0)
            except Exception as e:
                print(f"Exception: {e}")

    async def read_data_loop(self):
        while True:
            try:
                await self.connect()
            except Exception as e:
                print(f"Exception: {e}")
            await asyncio.sleep(10)

    def read_data_loop_sync(self, dt):
        print("every 10 seconds")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.connect())

    def update_pH(self, bluetooth_pH):
        print(f"updating ph to {bluetooth_pH}")
        DemoApp.screen_manager.get_screen("mainbandage").ids.pH.text = f"pH Level: {bluetooth_pH}"
        MainBandageScreen.generate_bar_graph(self)

    async def kivyCoro(self):
        await self.async_run(async_lib='asyncio')

    async def run_tasks(self):
        (done, pending) = await asyncio.wait({asyncio.create_task(self.kivyCoro()),
                                              asyncio.create_task(self.read_data_loop())},
                                             return_when='FIRST_COMPLETED')

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
        #self.root.get_screen('mainbandage').generate_bar_graph()

    # creating the bandage icons
    def on_start(self):
        print("started")
        # does nothing lol

    # saving phonenumbers once entered by user
    def get_data(self):
        phone_ref = db.reference(f"users/{DemoApp.uid}/phoneNums")

        if ((self.root.get_screen('phonenumbers2').ids.name.text == '') & (
                self.root.get_screen('phonenumbers2').ids.number.text == '')):
            print('invalid')
        elif (self.root.get_screen('phonenumbers2').ids.name.text == ''):
            print('invalid')

        elif (self.root.get_screen('phonenumbers2').ids.number.text == ''):
            print("hola")
        else:
            # self.root.get_screen('phonenumbers1').ids.numbers.add_widget(MDRectangleFlatButton(text=self.root.get_screen('phonenumbers2').ids.name.text + '\n'+self.root.get_screen('phonenumbers2').ids.number.text,size_hint=(1,0.05)))
            phone_ref.push().set({
                'name': self.root.get_screen('phonenumbers2').ids.name.text,
                'number': self.root.get_screen('phonenumbers2').ids.number.text
            })
            self.root.get_screen('phonenumbers2').ids.number.text = ''
            self.root.get_screen('phonenumbers2').ids.name.text = ''
            self.go_to_phonenums()
            # self.root.get_screen('phonenumbers2').manager.current = 'phonenumbers1'
        # print(self.root.get_screen('phonenumbers2').ids.data2.text) # address of textfield in kivy
        #     self.go_to_phonenums()

    def go_to_phonenums(self):
        phone_ref = db.reference(f"users/{DemoApp.uid}/phoneNums")
        rows = str(phone_ref.get())

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

        if rows != "None":
            rows = json.loads(str(phone_ref.get()).replace('\'', '"'))

            for contact in rows:
                box = BoxLayout(size_hint=(1, None), size=(0, 70), orientation='horizontal')
                button = MDRectangleFlatButton(
                    text=str(rows[contact]['name']) + '\n' + str(rows[contact]['number']), size_hint=(0.7, 1), size=(0, 70), id=contact)
                button.bind(on_press=lambda instance: self.make_phone_call(rows, contact))
                box.add_widget(button)
                remove_button = MDRectangleFlatButton(
                    text='-', text_color='red', line_color='red', size_hint=(None, 1), size=(50, 70),
                    on_press=partial(delete_id, contact, numbers, box))
                box.add_widget(remove_button)
                numbers.add_widget(box)

        self.root.get_screen('phonenumbers1').manager.current = 'phonenumbers1'


    def make_phone_call(self, rows, index):
        # formatted_phone_number = ''.join(filter(str.isdigit, phone_number))
        phone_number = rows[index]['number']

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

        #DemoApp.userEmail = email  # input("Please Enter Your Email Address : \n")
        # password = password5  # getpass("Please Enter Your Password : \n")

        # create users
        try:
            user = DemoApp.firebase_auth.create_user_with_email_and_password(email, password)
            print("Success .... ")

            #login = auth2.sign_in_with_email_and_password(email, password)

            # send email verification
            DemoApp.firebase_auth.send_email_verification(user['idToken'])
            self.root.get_screen('login').ids.errorLabel.text = "User " + email + """ was created. Check your email to 
                verify the account."""

            self.root.get_screen('login').manager.current = 'login'
        except requests.exceptions.HTTPError:
            self.root.get_screen('login').ids.errorLabel.text = "User already exists and was not able to be created."
            self.root.get_screen('login').manager.current = 'login'
        except Exception as e:
            self.root.get_screen('login').ids.errorLabel.text = f"User was not able to be created because of error {e}"
            self.root.get_screen('login').manager.current = 'login'

    def reset_password(self):
        DemoApp.firebase_auth.send_password_reset_email(DemoApp.email)

    def google_signin(self):

        # webbrowser.open('')
        auth_obj = auth

        cred = credentials.Certificate(
            r"json_file.json")
        firebase_admin.initialize_app(cred)

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

            # create users

            user = DemoApp.firebase_auth.sign_in_with_email_and_password(email, password)
            DemoApp.user = user
            print(user)
            user_info = DemoApp.firebase_auth.get_account_info(user['idToken'])
            print(user_info)
            if not user_info['users'][0]['emailVerified']:
                print("not verified")
                self.root.get_screen('login').ids.errorLabel.text = """User not verified, check your email and
                    click on the link sent to verify your account and gain access to Heal'm."""
                return False

            api_key = "AIzaSyAnyPC3n3JHYiTDhmfv-K8MKXA51lR1pZ4"
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
            data = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }

            response = requests.post(url, json=data)
            response_data = response.json()
            DemoApp.uid = response_data["localId"]
            # send email verification
            print("All good!")
            DemoApp.ref = db.reference(f"/users/{DemoApp.uid}")
            DemoApp.ref.update({"email": email})
            #DemoApp.ref.update({"PhoneNums"})

            DemoApp.email = email
            self.set_bandage_buttons()

            return True
            # login = auth.sign_in_with_email_and_password(email, password)
            # login = 'correct'
            # return True
        except requests.exceptions.RequestException as e:
            print("Login failed with error:", str(e))
            DemoApp.screen_manager.get_screen('login').ids.errorLabel.text = "Incorrect email or password. Try again."
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
    def set_bandage_buttons(self):
        bandage_ref = db.reference(f"users/{DemoApp.uid}/bandages")
        """bandage_ref.push().set({
            "name": "Arm Bandage",
            "uric acid": round(random.random(), 2),
            "pH": round(random.random() * 8, 2)
        })"""
        DemoApp.screen_manager.get_screen('menu').ids.container1.clear_widgets()
        rows = str(bandage_ref.get())
        if rows != "None":
            print(str(bandage_ref.get()))
            rows = json.loads(str(bandage_ref.get()).replace('\'', '"'))
            i = 1
            for bandage in rows:
                print(bandage)
                #DemoApp.bandages.append(bandage)
                DemoApp.bandages[bandage] = -1
                DemoApp.bandages_prev_data[bandage] = [0,0,0,0,0,0,0]
                button = MDRoundFlatIconButton(text=str(i), icon='bandage', size_hint=(1, 4), id=bandage,
                                               on_press=partial(load_bandage_info, bandage,
                                                                DemoApp.screen_manager.get_screen('mainbandage')))
                DemoApp.screen_manager.get_screen('menu').ids.container1.add_widget(button)

                i += 1

    def login_callback(self, email, password):
        if self.verify_login(email, password):
            self.root.get_screen('login').manager.current = 'menu'
            self.root.get_screen('login').ids.errorLabel.text = ""
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
    #     #     r"json_file.json")
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

        response = requests.post(url, json=data)
        response_data = response.json()
        print(response_data)
        #user_uid = response_data["localId"]

        # if "localId" in response_data:
        #     user_uid = response_data["localId"]
        #     return user_uid
        # else:
        #     error_message = response_data.get("error", {}).get("message", "Unknown error")
        #     return None

        email = self.root.get_screen('login').ids.email1.text
        password = self.root.get_screen('login').ids.password1.text

        # firebase.delete(login_data['localId'], None)

        try:
            email = DemoApp.user['email']
            auth.delete_user(DemoApp.user['localId'])
            self.root.get_screen('login').ids.errorLabel.text = "User " + email + " was successfully deleted"
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


asyncio.run(DemoApp().run_tasks())
