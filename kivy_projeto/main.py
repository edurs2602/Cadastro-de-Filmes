import kivy
import sys
import os
import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.recycleview import RecycleView
from kivy.properties import ObjectProperty, ListProperty, StringProperty, BooleanProperty
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior            #Bibliotecas importadas

Config.set('kivy', 'exit_on_escape', 0)         #Para não fechar o programa ao apertar ESC

connection = sqlite3.connect('cdf.db')          #Cria o banco de dados
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS dados          
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    Nome TEXT, Diretor TEXT, Lancamento TEXT, Valor TEXT, Nota INT, Genero TEXT);''')           #Cria a tabela no banco de dados chamada: dados
                                                                                                #Tem os valores de: (
                                                                                                #Nome, Diretor, Lançamento, Valor, Nota, Genero)
class Screenmanager(ScreenManager):         #Tela que comanda todas as outras
    pass

class Screen1(Screen):

    def confirmacao(self, *args):           #Cria um popup para perguntar se o usuario desejar sair
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

class Screen2(Screen):          #Tela responsavel para saber se o usuario deseja Cadastrar ou Listar
    pass

class ScreenCDF(Screen):            #Tela para Cadastrar um filme

    def spinner_clicked(self, value):           #Mostra no console qual Genero foi escolhido
        print('O Genero Selecionado Foi: ' + value)

    def insert_data(self):          #Adiciona os valores ao Banco de dados
        self.connection = sqlite3.connect('cdf.db')
        self.cursor = connection.cursor()

        Nome = str(self.ids.ti_nome.text)
        Diretor = str(self.ids.ti_diretor.text)
        Lancamento = str(self.ids.ti_lancamento.text)
        Valor = str(self.ids.ti_valor.text)
        Nota = str(self.ids.ti_nota.text)
        Genero = str(self.ids.spinner_id.text)

        cursor.execute(f'''INSERT INTO dados VALUES(NULL, '{Nome}', '{Diretor}', '{Lancamento}', '{Valor}', '{Nota}', '{Genero}')''')
        connection.commit()

    def salvo(self, *args):         #Popup para mostrar que foi cadastrado com sucesso

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

    def changer(self, *args):           #Muda para tela 2 ao clicar em 'ok' no popup
        self.manager.current = 'Screen2'

class TextInputPopup(Popup):            #Popup para mudar os valores dos filmes listados
    obj = ObjectProperty(None)
    obj_text = StringProperty("")

    def __init__(self, obj, **kwargs):
        super(TextInputPopup, self).__init__(**kwargs)
        self.obj = obj
        self.obj_text = obj.text

class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior, RecycleGridLayout):           #Cria um Gridlayour para o RV
    # Adiciona um focus behaviour to the view
    pass

class SelectableButton(RecycleDataViewBehavior, Button):            #Botões onde serão escrito os dados
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):          #Atualiza as mudanças do insert_data
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):         #Faz uma ação ao ser pressionado
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):          #Insere as mudanças
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))

    def on_press(self):         #Vai abrir um popup(TextInputPopup)
        popup = TextInputPopup(self)
        popup.open()

    def update_changes(self, txt):          #Vai atualizar as mudanças
        self.text = txt

class RV(RecycleView, Screen):          #Tela com o RecycleView
    data_list = ListProperty([])

    def __init__(self, **kwargs):           #Construtor da classe
        super(RV, self).__init__(**kwargs)
        self.data_transfer()

    def data_transfer(self):            #Pegará os dados da tabela para jogar no RecycleView
        connection = sqlite3.connect('cdf.db')
        cursor = connection.cursor()

        cursor.execute('''SELECT * FROM dados ORDER BY id ASC''')
        row = cursor.fetchall()

        for rows in row:
            for col in rows:
                self.data_list.append(col)

class app(App):         #Classe principal
    title = "Cadastro de Filmes"

    def build(self):
        return Screenmanager()

app().run()