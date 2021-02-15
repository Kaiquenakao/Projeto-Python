import PySimpleGUI as sg
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%d/%m/%Y %H:%M:%S")
print(current_time)

produto = []
pedido = []


class Produto:

    def __init__(self, nome, descricao, preco):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco

    def adicionar(self):
        produto.append([self.nome.upper(), self.descricao, self.preco])
        print(produto)


def janela():
    # Menu
    menu_def = [
        ['&File', ['&Adicionar', '&Editar', '&Remover', '!Disabled', '&Exit']]
    ]

    # Layout
    sg.theme("Reddit")
    layout = [
        [sg.Menu(menu_def, tearoff=False, key="menu")],
    ]
    return sg.Window('Login', layout=layout, finalize=True)


def janela_adicionar():
    #Layout
    layout = [
        [sg.Text(text="Nome"), sg.Input(key="usuario", size=(15, 0))],
        [sg.Text(text="Descrição"), sg.Input(key="descricao", size=(15, 0))],
        [sg.Text(text="Preço"), sg.Input(key="preco", size=(15, 0))],
        [sg.Button("Enviar"), sg.Button("Ver Lista")]
    ]
    return sg.Window("Adicionar Produto", layout=layout, finalize=True)


def janela_lista():
    sg.theme("Reddit")
    # Layout
    layout = [
        [sg.Text(text="Restaurante", font=('Arial', 19, 'bold'))],
        [
            sg.Text(text="Comidas", font=('Arial', 15, 'bold'), justification="right"),
            sg.Text(size=(15, 0)),
            sg.Text(text="Pedidos", font=('Arial', 15, 'bold'), pad=(20, 2))
        ],
        [sg.Listbox(produto, size=(20, 10), key="item"), sg.Button("Adicionar"), sg.Listbox(pedido, size=(20, 10),
                                                                                            key="pedido")]
    ]
    return sg.Window("Lista de produtos", layout=layout, finalize=True, element_justification='center')

#janelas
janela, produto_adicionar, produto_lista = janela(), None, None

while True:
    window, event, values = sg.read_all_windows()
    window.refresh()
    if (window == janela or window == produto_adicionar or window == produto_lista) and event == sg.WIN_CLOSED:
        break

    # Menu
    if window == janela and values['menu'] == 'Adicionar':
        produto_adicionar = janela_adicionar()
        janela.hide()

    if window == janela and values['menu'] == 'Exit':
        sg.Popup("Finalizando o programa")
        break

    if window == produto_adicionar and event == "Enviar":
        pessoa = Produto(values['usuario'], values['descricao'], float(values['preco']))
        pessoa.adicionar()

    if window == produto_adicionar and event == "Ver Lista":
        produto_lista = janela_lista()
        produto_adicionar.hide()

    if window == produto_lista and event == "Adicionar":
        try:
            pedido.append(values['item'][0])
            window.Element('pedido').Update(values=pedido)
            print(pedido)
        except IndexError:
            sg.Popup("Escolha um item")







