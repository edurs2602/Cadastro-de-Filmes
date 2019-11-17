import kivy
import sys
import os
import sqlite3
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.spinner import Spinner
from kivy.config import Config
from kivy.uix.actionbar import ActionBar
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.core.window import Window

Config.set('kivy', 'exit_on_escape', 0)
Config.set(u'''graphics''', u''''resizable''', True)
Config.write()
Window.size = (800, 600)

connection = sqlite3.connect('teste.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS dados 
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    Nome TEXT, Diretor TEXT, Lancamento TEXT, Valor TEXT, Nota INT, Genero TEXT);''')

class Screenmanager(ScreenManager):         #Tela que comanda todas as outras
    pass

class Screen1(Screen):

    def confirmacao(self, *args):           #Criar um pop-up para perguntar se o usuario desejar sair
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        botoes = BoxLayout(padding=10, spacing=10)

        pop = Popup(title='Deseja mesmo sair? ', content=box,size_hint=(None, None),
                    size=(240, 160))

        sim = Button(text='Sim', on_release=app.get_running_app().stop)
        nao = Button(text='Não', on_release=pop.dismiss)

        botoes.add_widget(sim)
        botoes.add_widget(nao)

        atencao = Image(source='alert.png')

        box.add_widget(atencao)
        box.add_widget(botoes)

        anim = Animation(size=(300, 220), duration=0.2, t='out_circ')
        anim.start(pop)

        pop.open()

class Screen2(Screen):
    pass

class ScreenCDF(Screen):

    def spinner_clicked(self, value):
        print('O Genero Selecionado Foi: ' + value)

    def insert_data(self):
        self.connection = sqlite3.connect('teste.db')
        self.cursor = connection.cursor()

        Nome = str(self.ids.ti_nome.text)
        Diretor = str(self.ids.ti_diretor.text)
        Lancamento = str(self.ids.ti_lancamento.text)
        Valor = str(self.ids.ti_valor.text)
        Nota = str(self.ids.ti_nota.text)
        Genero = str(self.ids.spinner_id.text)

        cursor.execute(f'''INSERT INTO dados VALUES(NULL, '{Nome}', '{Diretor}', '{Lancamento}', '{Valor}', '{Nota}', '{Genero}')''')
        connection.commit()

    def salvo(self, *args):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        botoes = BoxLayout(padding=10, spacing=10)

        pop = Popup(title='Cadastrado com sucesso!', content=box, size_hint=(None, None),
                    size=(240, 160))

        ok = Button(text='OK', on_release=pop.dismiss)

        botoes.add_widget(ok)

        atencao = Image(source='ok.png')

        box.add_widget(atencao)
        box.add_widget(botoes)

        anim = Animation(size=(300, 220), duration=0.2, t='out_circ')
        anim.start(pop)

        pop.open()

class Screen_Listar(Screen):
    rows = ListProperty([('id','Nome','Diretor','Lancamento','Valor','Nota','Genero')])

    def att_data(self):
        self.connection = sqlite3.connect('teste.db')
        self.cursor = connection.cursor()

        cursor.execute('''SELECT * FROM dados''')
        for i in cursor:
            r1 = 'ID: '+str(100000000+i[0])[1:9]+'\n'
            r2 = 'Nome: ' + str(i[1]) + '\n'
            r3 = 'Diretor: ' + str(i[2]) + '\n'
            r4 = 'Lancamento: ' + str(i[3]) + '\n'
            r5 = 'Valor: ' + str(i[4]) + '\n'
            r6 = 'Nota: ' + str(i[5]) + '\n'
            r7 = 'Genero: ' + str(i[6]) + '\n'
            listar = r1 + r2 + r3 + r4 + r5 + r6 + r7

class app(App):
    title = "Cadastro de Filmes"
    def build(self):
        return Screenmanager()

app().run()