import kivymd
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
#: import get_color_from_hex kivy.utils.get_color_from_hex
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import MDList, OneLineListItem, OneLineIconListItem
from kivymd.uix.list import IconLeftWidget
from kivy.uix.scrollview import ScrollView

Window.size = (300, 500)

screen_helper = """
ScreenManager:
    MenuScreen:
    PhoneNumScreen1:
    PhoneNumScreen2:
    
<MenuScreen>:
    name: 'menu'
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Heal'm"
            left_action_items: [["menu",lambda x: app.navigation_draw()]]
            right_action_items: [["bandage",lambda x: app.navigation_draw()]]
            elevation: 4
        MDLabel:
            text: 'addlist'
            halign: 'center'
        MDBottomNavigation:
            panel_color: 0,(145/255.0),(237/255.0),1
            text_color_active:get_color_from_hex("F5F5F5")
            
            MDBottomNavigationItem:
                name: 'screen 1'
                icon: 'cloud'
                                
            MDBottomNavigationItem:
                name: 'screen 2'
                icon: 'medication'
                
            MDBottomNavigationItem:
                name: 'screen 3'
                icon: 'phone'
                #click the button
                on_tab_release: root.manager.current = 'phonenumbers1'
                
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
        

<PhoneNumScreen2>:
    name: 'phonenumbers2'
    #input line
    MDTextField:
        id: data #providing id to text field
        hint_text: "Enter phone number:"
        helper_text: "(emergency contacts)"
        helper_text_mode: "on_focus"
        max_text_length: 12
        icon_right: "phone-alert"
        #color_mode = 'accent'
        #line_color_number:1,1,1,1 -->use this if you want to change line color
        pos_hint: {'center_x':0.5, 'center_y': 0.5}
        #makes line bigger for input
        size_hint_x: 0.8
        width: 300
    # enter button
    MDRectangleFlatButton:
        text: 'Enter'
        pos_hint:{'center_x':0.5, 'center_y':0.4}
        #app.get_data()
        on_press: app.get_screen('phonenumbers1').add_widget(self.root.get_screen('phonenumbers2').ids.data.text)
    # back button
    MDRectangleFlatButton:
        text: 'Back'
        pos_hint:{'center_x':0.5, 'center_y':0.2}
        on_press: root.manager.current = 'phonenumbers1'
        

"""

# list_helper = """
# Screen:
#     ScrollView:
#         MDList:
#             id: container
# """

class MenuScreen(Screen):
    pass

class PhoneNumScreen1(Screen):
    pass

class PhoneNumScreen2(Screen):
    pass



sm = ScreenManager()
sm.add_widget(MenuScreen(name ='menu'))
sm.add_widget(PhoneNumScreen1(name ='phonenumbers1'))
sm.add_widget(PhoneNumScreen2(name ='phonenumbers2'))





class DemoApp(MDApp):

    def build(self):
        #self.theme_cls.primary_palette = 'LightBlue'
        # self.theme_cls.accent_palette = 'Blue'
        screen = Builder.load_string(screen_helper)

        return screen
    def get_data(self):
        self.root.get_screen('phonenumbers1').add_widget(self.root.get_screen('phonenumbers2').ids.data.text)
        print(self.root.get_screen('phonenumbers2').ids.data.text) # address of textfield in kivy

#     def navigation_draw(self):
#         print("Navigation")
#     def on_start(self):
#         for i in range(20):
#             # icon = IconLeftWidget(icon="bandage")
#             items = OneLineListItem(text="Bandage " +str(i+1))
#             #command used to reference id in side list_helper(or any kind of multi-line string)
#             # items.add_widget(icon)
#             self.root.ids.container.add_widget(items)

    # def build(self):
    #     screen = Screen()
    #
    #     scroll = ScrollView()
    #     list_view = MDList()
    #     scroll.add_widget(list_view)
    #
    #     for i in range(20):
    #         icon = IconLeftWidget(icon="bandage")
    #         items = OneLineIconListItem(text='Bandage '+str(i+1))
    #         items.add_widget(icon)
    #         list_view.add_widget(items)
    #
    #     screen.add_widget(scroll)
    #     return screen

DemoApp().run()