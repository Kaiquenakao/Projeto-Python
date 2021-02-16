import PySimpleGUI as sg
from datetime import datetime

# Data atual do programa ao ser iniciado
now = datetime.now()
current_time = now.strftime("%d/%m/%Y %H:%M:%S")

produto = []
pedido = []
preco = []
precomenu = []
contador = 0


def nota_fiscal():
    # Produto.contador é usado para colocar na notafiscal(1, 2...)
    Produto.contador = Produto.contador + 1

    with open(f'NotaFiscal{Produto.contador}.txt', "w") as arq:
        arq.write(f'Dia da compra: {current_time}\n')
        produtoteste = list(map(lambda x: x[0], pedido))

        arq.write("----------- Lista de Produtos -----------\n")
        for item in produtoteste:
            arq.write(f'{item}\n')

        arq.write("----------- Informações -----------\n")
        arq.write(f'Quantidade: {len(precomenu)}\n'
                  f'Preço: {sum(precomenu)}\n')

    sg.popup("Nota fiscal gerada")
    print(pedido)
    window['notafiscal'].Update(disabled=True)

    # Após clicar em gerar nota fiscal, limpa as listas preco e pedido
    preco.clear()
    pedido.clear()

    # Limpando os dados após gerar nota fiscal
    window['pedido'].Update(pedido)
    window['quantidade'].Update(value='')
    window['preco'].Update(value='')

def somar():
    preco.extend(list(map(lambda x: x[-1], pedido)))
    window['pedido'].Update(pedido)


class Produto:
    contador = 0

    def __init__(self, nome, precopro):
        self.nome = nome
        self.precopro = precopro

    def adicionar(self):
        produto.append([self.nome.upper(), '-', self.precopro])


# Janela de adicionar produto
def janela_adicionar():
    #Layout
    layout = [
        [sg.Text(text="Nome:"), sg.Input(key="nome", size=(15, 0))],
        [sg.Text(text="Preço:"), sg.Input(key="preco", size=(15, 0))],
        [sg.Button("Enviar"), sg.Button('Voltar')]
    ]
    return sg.Window("Adicionar Produto", layout=layout, finalize=True)

# Janela principal
def janela_lista():
    sg.theme("Reddit")
    # Menu
    menu_def = [
        ['&File', ['&Adicionar', '&Editar', '&Remover', '!Disabled', '&Exit']]
    ]

    # Layout
    layout = [
        [sg.Menu(menu_def, tearoff=False, key='menu')],
        [sg.Text(text="Mercado", justification="center", font=('Arial', 19, 'bold'))],
        [
            sg.Text(text="Produto(s)", font=('Arial', 15, 'bold')),
            sg.Text(size=(10, 0)),
            sg.Text(text="Pedido(s)", font=('Arial', 15, 'bold'), pad=(20, 2))
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
        ],

        [
            sg.Button("Gerar nota fiscal", key="notafiscal", disabled=True, pad=(144, 0))
        ]


    ]
    return sg.Window("Mercado", layout=layout, finalize=True)


#janelas
lista, adicionar = janela_lista(), None


while True:
    window, event, values = sg.read_all_windows()
    window.refresh()
    if (window == lista or window == adicionar) and event == sg.WIN_CLOSED:
        break

    # Menu
    if window == lista and values['menu'] == 'Adicionar':
        # Após sair da janela principal, limpar o pedido
        pedido.clear()
        window['pedido'].Update(pedido)

        adicionar = janela_adicionar()
        lista.hide()

    if window == lista and values['menu'] == 'Exit':
        sg.Popup("Finalizando o programa")
        break

    if window == adicionar and event == "Enviar":
        try:
            if len(values['preco']) > 0 and len(values['nome']) > 0:
                pessoa = Produto(values['nome'], float(values['preco']))
                pessoa.adicionar()
                window['nome'].Update(value="")
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
        window['gerar'].Update(disabled=True)
        window['pedido'].Update(pedido)
        somar()
        precomenu = preco.copy()
        preco.clear()
        window['quantidade'].Update(value=len(precomenu))
        window['preco'].Update(value=sum(precomenu))
        window['notafiscal'].Update(disabled=False)

    if window == lista and event == "notafiscal":
        nota_fiscal()













