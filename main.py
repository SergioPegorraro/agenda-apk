from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.list import ThreeLineListItem, MDList
from kivymd.uix.dialog import MDDialog
from kivymd.theming import ThemeManager
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3

# Conectar a la base de datos SQLite
conn = sqlite3.connect("agenda.db")
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS contactos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    apellido TEXT,
    telefono TEXT
)
""")
conn.commit()

screen_helper = """

ScreenManager:
   
    Principal:
    Listado:


    
<Principal>:
    name: 'principal'
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            #right_action_items: [["dots-vertical", lambda x: app.callback_1(x)]]
            title: "Agenda"
            elevation: 10

        BoxLayout:
            orientation: "vertical"
            padding: dp(10)
            spacing: "10dp"  # Espaciado entre los botones

            MDTextField:
                id: nombre_field
                hint_text: "Nombre"
                size_hint_y: None
                height: dp(40)

            MDTextField:
                id: apellido_field
                hint_text: "Apellido"
                size_hint_y: None
                height: dp(40)

            MDTextField:
                id: telefono_field
                hint_text: "Teléfono"
                size_hint_y: None
                height: dp(40)    
        BoxLayout:
            orientation: "horizontal"
            padding: dp(10)
            spacing: "10dp"  # Espaciado entre los botones

            MDRaisedButton:
                text: "Agregar"
                on_release: root.agregar_contacto()

            MDRaisedButton:
                text: "Consultar"
                on_release: app.root.current = 'listado'             
<Listado>:
    name: 'listado'
    on_enter:root.consultar_contactos()
   
    BoxLayout:
        #size_hint_y: None
        #height: '56'
        #spacing: '10dp'
        #pos_hint: {'center_y': .94}
        orientation: "vertical"
        MDTopAppBar:
            right_action_items: [["home", lambda x: app.callback(x)]]
            title: "Listado de Contactos"
            elevation: 10
            #padding: dp(10)
            #spacing: "10dp"  # Espaciado entre los botones   
        BoxLayout:
            size_hint_y: None
            height: '40'
            spacing: '10dp'
            pos_hint: {'center_y': .99}
            #orientation: "vertical"
            
        MDScrollView:
            bar_width: dp(15) 
            MDList:
                size_hint_x:0.9
                id: lista_contactos
"""
colors = {
    "Teal": {
        "200": "#212121",
        "500": "#212121",
        "700": "#212121",
    },
    "Red": {
        "200": "#C25554",
        "500": "#C25554",
        "700": "#C25554",
    },
    "Light": {
        "StatusBar": "E0E0E0",
        "AppBar": "#202020",
        "Background": "#2E3032",
        "CardsDialogs": "#FFFFFF",
        "FlatButtonDown": "#CCCCCC",
    },
}


class Principal(Screen):
    def agregar_contacto(self):
        nombre = self.ids.nombre_field.text
        apellido = self.ids.apellido_field.text
        telefono = self.ids.telefono_field.text

        # Insertar el nuevo contacto en la base de datos
        cursor.execute("INSERT INTO contactos (nombre, apellido, telefono) VALUES (?, ?, ?)", (nombre, apellido, telefono))
        conn.commit()

        # Limpiar los campos después de agregar el contacto
        self.ids.nombre_field.text = ""
        self.ids.apellido_field.text = ""
        self.ids.telefono_field.text = ""
    
class Listado(Screen):
    def consultar_contactos(self):
        # Limpiar la lista de contactos antes de mostrar los resultados
        self.ids.lista_contactos.clear_widgets()

        # Consultar todos los contactos en la base de datos
        cursor.execute("SELECT * FROM contactos")
        contactos = cursor.fetchall()

        for contacto in contactos:
            # Mostrar cada contacto en la lista
            item = ThreeLineListItem(
                text=contacto[1],
                secondary_text=contacto[2],
                tertiary_text=contacto[3],
                on_release=lambda x, id=contacto[0]: self.mostrar_opciones_contacto(id)
            )
            self.ids.lista_contactos.add_widget(item)

    def mostrar_opciones_contacto(self, contacto_id):
        # Mostrar un cuadro de diálogo con opciones para modificar o eliminar el contacto
        dialog = MDDialog(
            title="Opciones de Contacto",
            buttons=[
               # MDFlatButton(
                #    text="Modificar",
               #     on_release=lambda x: self.modificar_contacto(contacto_id,dialog)
               # ),
                MDFlatButton(
                    text="Eliminar",
                    on_release=lambda x: self.eliminar_contacto(contacto_id)
                ),
                MDFlatButton(
                    text="Cerrar",
                    on_release=lambda x: dialog.dismiss()
                ),
            ]
        )
        dialog.open()
    def eliminar_contacto(self, contacto_id):
        # Eliminar el contacto de la base de datos
        cursor.execute("DELETE FROM contactos WHERE id=?", (contacto_id,))
        conn.commit()

        # Actualizar la lista después de eliminar el contacto
        self.consultar_contactos()
        
    

#Crear el screen manager
sm = ScreenManager()
sm.add_widget(Principal(name='principal'))
sm.add_widget(Listado(name='listado'))


class TPApp(MDApp,ThemeManager):
    theme_cls = ThemeManager()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        """         items_d = ['Tema Oscuro','Tema Claro']
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i}",
                "height": dp(56),
                "on_release": lambda x=f"{i}": self.menu_callback(x),
             } for i in items_d
        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        ) """
        
    def callback(self, instance_action_top_appbar_button):
         self.root.current = 'principal'  
    def callback_1(self, button):
        self.menu.caller = button
        self.menu.open()
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"  
        return Builder.load_string(screen_helper)    
    """ def menu_callback(self, text_item):
        self.menu.dismiss()
        text=text_item
        if text=="Tema Oscuro":
            self.theme_cls.primary_palette = "Orange"  
            self.theme_cls.theme_style = "Dark" 
        else:
            self.theme_cls.theme_style = "Light" 
            self.theme_cls.primary_palette = "Blue"   
            self.screen = Builder.load_string(screen_helper)   
           # return self.screen
        self.menu.dismiss() """
        
 
     
if __name__ == "__main__":
  TPApp().run()
