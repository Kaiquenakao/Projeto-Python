import PySimpleGUI as sg
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%d/%m/%Y %H:%M:%S")
print(current_time)

produto = []
pedido = []
preco = []


def somar():
    preco.extend(list(map(lambda x: x[-1], pedido)))
    pedido.clear()
    window['pedido'].Update(pedido)



class Produto:

    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

    def adicionar(self):
        produto.append([self.nome.upper(), '-', self.preco])
        print(produto)


def janela_adicionar():
    #Layout
    layout = [
        [sg.Text(text="Nome:"), sg.Input(key="usuario", size=(15, 0))],
        [sg.Text(text="Preço:"), sg.Input(key="preco", size=(15, 0))],
        [sg.Button("Enviar"), sg.Button('Voltar')]
    ]
    return sg.Window("Adicionar Produto", layout=layout, finalize=True)


def janela_lista():
    sg.theme("Reddit")
    # Menu
    menu_def = [
        ['&File', ['&Adicionar', '&Editar', '&Remover', '!Disabled', '&Exit']]
    ]

    # Layout
    layout = [
        [sg.Menu(menu_def, tearoff=False, key='menu')],
        [sg.Text(text="Restaurante", justification="center", font=('Arial', 19, 'bold'))],
        [
            sg.Text(text="Comidas", font=('Arial', 15, 'bold')),
            sg.Text(size=(15, 0)),
            sg.Text(text="Pedidos", font=('Arial', 15, 'bold'), pad=(20, 2))
        ],
        [sg.Listbox(produto, size=(20, 10), key="item"), sg.Button("Pedir"), sg.Listbox(pedido, size=(20, 10),
                                                                                            key="pedido")],
        [
            sg.Button("Gerar Preço", pad=(155, 0), disabled=True, key='gerar')
        ],

        [
            sg.Text(text="Quantidade:", font=('Arial', 10, 'bold')),
            sg.Input(key='quantidade', size=(5, 0), disabled=True)
        ],

        [
            sg.Text(text="Preço: ", font=('Arial', 10, 'bold')),
            sg.Input(key='preco', size=(5, 0), disabled=True)
        ]


    ]
    return sg.Window("Restaurante", layout=layout, finalize=True)


#janelas
lista, adicionar = janela_lista(), None


while True:
    window, event, values = sg.read_all_windows()
    window.refresh()
    if (window == lista or window == adicionar) and event == sg.WIN_CLOSED:
        break

    # Menu
    if window == lista and values['menu'] == 'Adicionar':
        adicionar = janela_adicionar()
        lista.hide()

    if window == lista and values['menu'] == 'Exit':
        sg.Popup("Finalizando o programa")
        break

    if window == adicionar and event == "Enviar":
        try:
            if len(values['preco']) > 0 and len(values['usuario']) > 0:
                pessoa = Produto(values['usuario'], float(values['preco']))
                pessoa.adicionar()
                window['usuario'].Update(value="")
                window['preco'].Update(value="")
                sg.Popup("Item adicionado com sucesso")
            else:
                sg.Popup("Campos não preenchidos")
        except ValueError:
            sg.Popup("O preço tem que ser númerico")

    if window == adicionar and event == 'Voltar':
        lista = janela_lista()
        adicionar.hide()

    if window == lista and event == "Pedir":
        try:
            pedido.append(values['item'][0])
            window.Element('pedido').Update(values=pedido)
        except IndexError:
            sg.Popup("Escolha um item")

    if window == lista and len(pedido) > 0:
        window['gerar'].Update(disabled=False)

    if window == lista and event == "gerar":
        window['quantidade'].Update(value=len(pedido))
        somar()
        print(preco)
        window['preco'].Update(value=sum(preco))
        preco.clear()











