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

        ok = Button(text='OK', on_press=pop.dismiss, on_release=self.changer)

        botoes.add_widget(ok)

        atencao = Image(source='ok.png')

        box.add_widget(atencao)
        box.add_widget(botoes)

        anim = Animation(size=(300, 220), duration=0.2, t='out_circ')
        anim.start(pop)

        pop.open()

    def changer(self, *args):
        self.manager.current = 'Screen2'

    def clear_txt(self):
        for txt in (self.ids.ti_nome.text, self.ids.ti_diretor.text, self.ids.ti_lancamento.text, self.ids.ti_valor.text, self.ids.ti_nota.text):
            txt = ''

class Screen_Listar(Screen):
    #rows = ListProperty([('id', 'Nome', 'Diretor', 'Lancamento', 'Valor', 'Nota', 'Genero')])

    def att_data(self):
        for row in cursor.execute('''SELECT * FROM dados'''):
            print("ID: ", row[0])
            print("NOME: ", row[1])
            print("DIRETOR: ", row[2])
            print("LANCAMENTO: ", row[3])
            print("VALOR: ", row[4])
            print("NOTA: ", row[5])
            print("GENERO: ", row[6])
            print('=-=' *32)

    def listData(self):
        rows = []
        for row in cursor.execute('''SELECT * FROM dados'''):
            r1 = 'ID: ' + str(row[0]) + '\n'
            r2 = 'Nome do Filme: ' + str(row[1]) + '\n'
            r3 = 'Diretor: ' + str(row[2]) + '\n'
            r4 = 'Lançamento: ' + str(row[3]) + '\n'
            r5 = 'Valor: ' + str(row[4]) + 'R$' + '\n'
            r6 = 'Nota: ' + str(row[5]) + '\n'
            r7 = 'Genero: ' + str(row[6]) + '\n'
            Mrow = r1 + r2 + r3 + r4 + r5 + r6 + r7
            rows.append(Mrow)
            return Mrow


class app(App):
    title = "Cadastro de Filmes"
    def build(self):
        return Screenmanager()

app().run()