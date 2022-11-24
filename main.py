from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from bs4 import BeautifulSoup
import requests
import locale
from datetime import date
import pandas as pd

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def decimal (decimal_str):
    return locale.atof(decimal_str)

window = Tk()
window.title('Carteira Fiis')
window.iconbitmap("icon.ico")
window.geometry("700x255+620+320")

l1 = Label(window, text="Fundos da sua carteira:")
l1.grid(row=0, column=0)
e = Entry(window, borderwidth=3, width=25)
e.grid(row=0, column=1, padx=10)

carteira_usuario = []
cotas = []
rendimentos = []

def add_fundo():
    global label
    while True:
        if e.get() != '':
            if e.get().upper() not in carteira_usuario:
                carteira_usuario.append(e.get().upper())
                label = Label(window, text=f"{e.get().upper()} Adicionado!")
                label.grid(column=0)
                e.delete(0, END)
            else:
                messagebox.showerror("Error", "Fundo ja adicionado")
        else:
            messagebox.showerror("Error", "Digite o código do fundo")
        break

def busca_indicadores():
    if not carteira_usuario:
        messagebox.showerror("Error", "Carteira Vazia, adicione os fundos primeiro")
    else:
        for fundo in carteira_usuario:
            site = f"https://www.fundsexplorer.com.br/funds/{fundo}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            content = requests.get(site, headers=headers)
            soup = BeautifulSoup(content.text, 'html.parser')

            elemento_preco = soup.find("span", class_="price")

            cota = decimal(elemento_preco.text.split()[1])

            indicadores = soup.find_all('span', class_="indicator-value")

            ultimo_rendimento = decimal(indicadores[1].text.split()[1])

            cotas.append(cota)

            rendimentos.append(ultimo_rendimento)
        l2 = Label(window, text="Informações salvas")
        l2.grid()

def salvar():
    if not cotas:
        messagebox.showerror("Error", "Adicione os fundos e busque as informações antes de salvar")
    else:
        infos = list(zip(carteira_usuario, cotas, rendimentos))

        dados = pd.DataFrame(infos, columns=['FUNDO', 'VALOR COTA', 'ÚLTIMO RENDIMENTO'])

        data = date.today().strftime('%b-%d-%Y')

        path = '{}'.format(askdirectory(title="Selecione", initialdir='/'))

        dados.to_excel(rf'{path}/atualizacao {data}.xlsx', index=False)

def limpar():
    carteira_usuario.clear()
    #label.grid_forget()
    for label in window.winfo_children():
        if type(label) == Label :
            label.destroy()

#Botões
btn_add = Button(window, text="Adicionar", command=add_fundo, fg="blue") #state=DISABLED
btn_add.grid(row=0, column=2)

btn_buscar = Button(window, text="Buscar Informações da carteira", command=busca_indicadores, fg="blue")
btn_buscar.grid(row=0, column=3)

btn_salvar = Button(window, text="Salvar Informações", command=salvar, fg="green")
btn_salvar.grid(row=0, column=4)

btn_limpar = Button(window, text="Limpar", command=limpar, fg="red")
btn_limpar.grid(row=0, column=5)

window.mainloop()

