import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import filedialog
import os
import platform
import subprocess
import subprocess

import subprocess
import platform
window = tk.Tk()

window.title("Tranquilosec - T-DDOS")
running = False
processo_terminal = None
flagProxy = False
flagUAM = False
flagCrawl = False
canvas = tk.Canvas(window, width=800, height=600, bg='#36393e')
canvas.pack()
comando = "python doom.py"


icon_image = Image.open('./resources/logo.png')  # Replace with your icon file path
icon_photo = ImageTk.PhotoImage(icon_image)

window.wm_iconphoto(True, icon_photo)

# Variável global para armazenar o processo
processo_terminal = None

import subprocess
import platform

# Variável global para armazenar o processo
processo_terminal = None

def rodar_comando():
    global running
    global processo_terminal

    # Check if the process has terminated
    if processo_terminal is not None:
        if processo_terminal.poll() is not None:
            # The process has terminated
            processo_terminal = None
            running = False

    if not running:
        # Start with the base command
        comando = "python doom.py"

        # Get values from GUI
        header = txtHeader.get()
        url = txtUrl.get()
        thread = txtThread.get()
        proxy = txtProxy.get()

        # Show info
        add_output(f"url: {url}")
        comando += f' -u {url} -t {thread}'
        add_output(f"Proxy: {proxy}")
        add_output(f"Thread: {thread}")
        add_output(f"header: {header}")

        # Verify flags and construct command
        if flagCrawl:
            comando += ' -c'
        if flagProxy:
            comando += ' -p'
            if proxy != '':
                comando += f' -l {proxy}'
        if flagUAM:
            comando += ' -a'
        if header != '':
            comando += f' -e {header}'

        # Show the final constructed command
        add_output(f'{comando}')

        # Execute the command in a separate terminal
        sistema_operacional = platform.system()
        if sistema_operacional == "Windows":
            # Execute the command and ensure the terminal can be closed
            processo_terminal = subprocess.Popen(
                ["cmd.exe", "/c", comando],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        elif sistema_operacional in ["Linux", "Darwin"]:
            processo_terminal = subprocess.Popen(
                ["x-terminal-emulator", "-e", comando],
                shell=False
            )
        else:
            add_output("Sistema operacional não suportado")

        # Update the running state
        running = True

    else:
        # If the process is running, attempt to terminate it
        if processo_terminal:
            try:
                processo_terminal.terminate()  # Closes the terminal
            except Exception as e:
                add_output(f"Error terminating process: {e}")
            processo_terminal = None

        running = False

def escolher_arquivo():
    file_path = filedialog.askopenfilename()  # Abre o diálogo para escolher arquivo
    if file_path:  # Se um arquivo for selecionado
        txtProxy.delete(0, tk.END)  # Limpa o conteúdo atual da Entry
        txtProxy.insert(0, file_path)  # Insere o caminho do arquivo selecionado

def add_output(text):
    txt_cli_area.config(state=tk.NORMAL)  # Habilita edição
    txt_cli_area.insert(tk.END, text + '\n')  # Adiciona o texto no final da área de texto
    txt_cli_area.config(state=tk.DISABLED)  # Desabilita edição
    txt_cli_area.see(tk.END)  # Rola automaticamente para o final


def modifyFlagCrawl():
    global flagCrawl
    if flagCrawl == True:
        flagCrawl = False  # Define a variável como False
        btnUseCrawler.config(bg="#D14242")  # Altera a cor do botão e o texto
        add_output(f"agora a flag Usar Crawler esta {flagCrawl}")  # Exibe o valor da variável no console
    else:
        flagCrawl = True  # Define a variável como False
        btnUseCrawler.config(bg="#60CC69")  # Altera a cor do botão e o texto
        add_output(f"agora a flag Usar Crawler esta {flagCrawl}")  # Exibe o valor da variável no console


def modifyFlagProxy():
    global flagProxy
    if flagProxy == True:
        flagProxy = False  # Define a variável como False
        btnUseProxy.config(bg="#D14242")  # Altera a cor do botão e o texto
        add_output(f"agora a flag Usar Proxy esta {flagProxy}")  # Exibe o valor da variável no console
    else:
        flagProxy = True  # Define a variável como False
        btnUseProxy.config(bg="#60CC69")  # Altera a cor do botão e o texto
        add_output(f"agora a flag Usar Proxy esta {flagProxy}")  # Exibe o valor da variável no console
def modifyFlagUAM():
    global flagUAM
    if flagUAM == True:
        flagUAM = False  # Define a variável como False
        btnUAM.config(bg="#D14242")  # Altera a cor do botão e o texto
        add_output(f"agora a flag Modo Under Attack esta {flagUAM}")  # Exibe o valor da variável no console
    else:
        flagUAM = True  # Define a variável como False
        btnUAM.config(bg="#60CC69")  # Altera a cor do botão e o texto
        add_output(f"agora a flag Modo Under Attack esta {flagUAM}")  # Exibe o valor da variável no console

# Cinza escuro

canvas.create_rectangle(
    494.0,
    49.0,
    769.0,
    300.0,
    fill="#282B30",
    outline="")
# CLI AREA
canvas.create_rectangle(
    30.0,
    316.0,
    769.0,
    574.0,
    fill="#1E2124",
    outline="")
txt_cli_area = canvas.create_rectangle(
    35,
    321,
    764,
    569,
    fill='#1E2124'
)
txt_cli_area = tk.Text(window, bg="#1E2124", fg="White", state=tk.DISABLED, wrap=tk.WORD, bd=0, highlightthickness=0, border=0,borderwidth=0)
output_area_window = canvas.create_window(((35+764)/2), ((321+569)/2), window=txt_cli_area, width=(764-35), height=(569-321))
canvas.create_text(
    49.0,
    298.0,
    anchor="nw",
    text="CLI OUTPUT",
    fill="#FFFFFF",
    font=("Comfortaa Regular", 16 * -1)
)

canvas.create_text(
    322.0,
    111.0,
    anchor="nw",
    text="Headers",
    fill="#FFFFFF",
    font=("Comfortaa Regular", 20 * -1)
)
canvas.create_text(
    49.0,
    195.0,
    anchor="nw",
    text="Proxys",
    fill="#FFFFFF",
    font=("Comfortaa Regular", 20 * -1)
)
canvas.create_text(
    39.0,
    111.0,
    anchor="nw",
    text="Threads",
    fill="#FFFFFF",
    font=("Comfortaa Regular", 20 * -1)
)
canvas.create_text(
    39.0,
    27.0,
    anchor="nw",
    text="Url to Attack",
    fill="#FFFFFF",
    font=("Comfortaa Regular", 20 * -1)
)
#--------------------------------
#Cinza claro
btnAtacar = canvas.create_rectangle(
    506.0,
    243.0,
    759.0,
    289.0,
    fill="#7289DA",
    outline="")
btnStartAttack = tk.Button(window,text="Start Attack", font=("Comforta", 16), bg='#7289da',fg='white',command=rodar_comando, highlightthickness=0, border=0, bd=0)

canvas.create_window(((759+506)/2), ((289+243)/2), window=btnStartAttack, width=(759-506), height=(289-243))
# BOTAO START ATAQUE


canvas.create_rectangle(
    30.0,
    217.0,
    418.0,
    267.0,
    fill="#424549",
    outline="")
txtProxy = tk.Entry(window, bg="#424549", bd=0, highlightthickness=0,border=0, fg='white', font=('Comforta', 16), highlightcolor='white')
canvas.create_window(((30+418)/2), ((217+267)/2), window=txtProxy, width=(368), height=(267-217))
canvas.create_text(
    39.0,
    27.0,
    anchor="nw",
    text="Url to Attack",
    fill="#FFFFFF",
    font=("Comfortaa Regular", 20 * -1)
)

canvas.create_rectangle(
    30.0,
    49.0,
    480.0,
    99.0,
    fill="#424549",
    outline="")
txtUrl = tk.Entry(window, bg="#424549", bd=0, highlightthickness=0,border=0, fg='white', font=('Comforta', 16), highlightcolor='white')
canvas.create_window(((30+480)/2), ((49+99)/2), window=txtUrl, width=430, height=(99-49))

#threads
canvas.create_rectangle(
    30.0,
    133.0,
    310.0,
    183.0,
    fill="#424549",
    outline="")
txtThread = tk.Entry(window, bg="#424549", bd=0, highlightthickness=0,border=0, fg='white', font=('Comforta', 16), highlightcolor='white')
canvas.create_window(((30+310)/2), ((133+183)/2), window=txtThread, width=(270), height=(183-133))

canvas.create_rectangle(
    320.0,
    133.0,
    480.0,
    183.0,
    fill="#424549",
    outline="")
txtHeader = tk.Entry(window, bg="#424549", bd=0, highlightthickness=0,border=0, fg='white', font=('Comforta', 16), highlightcolor='white')
canvas.create_window(((320+480)/2), ((133+183)/2), window=txtHeader, width=(140), height=(183-133))
canvas.create_rectangle(
    430.0,
    217.0,
    480.0,
    267.0,
    fill="#424549",
    outline="")
check_image = ctk.CTkImage(Image.open("./resources/folder.png"), size=(40, 40))
btnOpenProxy = ctk.CTkButton(window,text='', fg_color='transparent',image=check_image,command=escolher_arquivo,bg_color="#424549")
canvas.create_window(((430+480)/2), ((217+267)/2), window=btnOpenProxy, width=(50), height=(50))
canvas.create_rectangle(
    709.0,
    59.0,
    759.0,
    109.0,
    fill="#424549",
    outline="")


canvas.create_rectangle(
    506.0,
    59.0,
    697.0,
    109.0,
    fill="#424549",
    outline="")

canvas.create_rectangle(
    709.0,
    59.0,
    759.0,
    109.0,
    fill="#424549",
    outline="")
canvas.create_rectangle(
    506.0,
    59.0,
    697.0,
    109.0,
    fill="#424549",
    outline="")
canvas.create_rectangle(
    709.0,
    122.0,
    759.0,
    172.0,
    fill="#424549",
    outline="")
canvas.create_rectangle(
    506.0,
    123.0,
    697.0,
    173.0,
    fill="#424549",
    outline="")
canvas.create_text(
    521.0,
    138.0,
    anchor="nw",
    text="Under Attack Mode",
    fill="#FFFFFF",
    font=("Comfortaa Regular", 16 * -1)
)
canvas.create_rectangle(
    506.0,
    183.0,
    697.0,
    233.0,
    fill="#424549",
    outline="")
canvas.create_text(
    521.0,
    199.0,
    anchor="nw",
    text="Use Crawler Mode",
    fill="#FFFFFF",
    font=("Comfortaa Regular", 16 * -1)
)
canvas.create_rectangle(
    709.0,
    183.0,
    759.0,
    233.0,
    fill="#424549",
    outline="")
canvas.create_text(
    521.0,
    75.0,
    anchor="nw",
    text="Use Proxy to attack",
    fill="#FFFFFF",
    font=("Comfortaa Regular", 16 * -1)
)
#--------------------------------------------
# VERDE ______________________________________
canvas.create_rectangle(
    724.0,
    137.0,
    744.0,
    157.0,
    fill="#7EC078",
    outline="")
btnUAM = tk.Button(window, bg='#D14242',command=modifyFlagUAM, bd=0, highlightthickness=0, border=0)
canvas.create_window(((724+744)/2), ((137+157)/2), window=btnUAM, width=(744-724), height=(157-137))
canvas.create_rectangle(
    724.0,
    74.0,
    744.0,
    94.0,
    fill="#7EC078",
    outline="")
btnUseProxy = tk.Button(window, bg='#D14242',command=modifyFlagProxy, bd=0, highlightthickness=0, border=0)
canvas.create_window(((724+744)/2), ((74+94)/2), window=btnUseProxy, width=(744-724), height=(94-74))

canvas.create_rectangle(
    724.0,
    198.0,
    744.0,
    218.0,
    fill="#7EC078",
    outline="")
btnUseCrawler = tk.Button(window, bg='#D14242',command=modifyFlagCrawl, bd=0, highlightthickness=0, border=0)
canvas.create_window(((724+744)/2), ((198+218)/2), window=btnUseCrawler, width=(744-724), height=(94-74))

#----------------------------------------------------
window.resizable(False,False)




add_output("Primeira linha de saída no terminal.")
window.mainloop()