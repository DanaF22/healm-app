# import kivymd
# import jnius as jnius
import platform

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
#: import get_color_from_hex kivy.utils.get_color_from_hex
from kivymd.uix.button import MDRoundFlatIconButton, MDFloatingActionButton, MDRectangleFlatButton, MDFlatButton
from functools import partial

import webbrowser
# from plyer import call


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
        size_hint : None, None
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
            on_press: root.manager.current = 'menu'
        Widget:
            size_hint_y : None
            height : 30
            
<SigninScreen>:
    name: "signin"

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
    pass

class BandageInfo(Screen):
    pass

class PhoneNumScreen1(Screen):
    pass

class PhoneNumScreen2(Screen):
    pass

class MainBandageScreen(Screen):
    pass




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
        screen = Builder.load_string(screen_helper)

        return screen

    # adding the bandages onto screen

    # what happens when press one of the bandage icons
    def pressed(self, *args):
        self.root.get_screen('menu').manager.current = 'mainbandage'

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
            box.add_widget(button)
            remove_button = MDRectangleFlatButton(
                text='-', text_color='red', line_color='red', size_hint=(None, 1), size=(50, 70),
                on_press=partial(delete_id, rows[i][0], numbers, box))
            box.add_widget(remove_button)
            numbers.add_widget(box)


        self.root.get_screen('phonenumbers1').manager.current = 'phonenumbers1'

    #
    # def make_phone_call(self, phone_number):
    #     # formatted_phone_number = ''.join(filter(str.isdigit, phone_number))
    #
    #     call_url =  f"tel:{phone_number}"
    #
    #     try:
    #         webbrowser.open(call_url)
    #     except Exception as e:
    #         print("Error:", e)

DemoApp().run()
