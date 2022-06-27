'''
Projeto de Software II - Universidade Positivo - Eng.Comp.
Alunos: Gabriel França e Pedro Andilossi

Projeto envolvendo Python, APIs e interface para obter o detalhe do clima de um endereço, informar o usuário e se quiser enviar por e-mail.

follow on git @b4ndo
'''

from cProfile import label
import json
from geopy.geocoders import Nominatim
from datetime import datetime
import requests
import pytz
from tkinter import *
import tkinter as tk
import tkinter.font as tkFont
import win32com.client as win32
import os

#token da api do openweather
token = 'e4720729770650b1e075619623c3ffb7'
saidaend = ""
outlook = win32.Dispatch('outlook.application')

def getcoord(x):
    coordenadas = Nominatim(user_agent="Weather")
    return coordenadas.geocode(f"{x}").raw

def weather(x,y):
    weather = requests.get(f'https://api.openweathermap.org/data/3.0/onecall?lat={x}&lon={y}&exclude=minutely,hourly&appid={token}&units=metric&lang=pt_br')
    weatheraw = json.loads(weather.content)
    return weatheraw

def files(zonatempo,hrconsultabrt,sunrisebrt,sunsetbrt,tempatualint,sensacaoint,pressao,umidade,uvi,vento,direcaovento,main,chuvaatual, email):
    
    arquivo = open('temperatura.txt', 'w')
    frases = list()
    frases.append(f'O fuso-horário está seguindo a região {zonatempo} e a consulta foi efetuada em {hrconsultabrt}\n')
    frases.append(f'O sol está nascendo às {sunrisebrt} e se pondo às {sunsetbrt}\n')
    frases.append(f'A temperatura atual é de {"%.1f"%tempatualint}°C e a sensação térmica é de {"%.1f"%sensacaoint}°C.\n')
    frases.append(f'A pressão está em {"%.1f"%pressao}atm e a umidade está em {umidade}%, com UVI de {uvi}.\n')
    frases.append(f'A velocidade do vento está em {vento}m/s e a direção está em {direcaovento} graus metereológicos.\n')
    frases.append(f'*** Detalhes do Clima: {main}\n*** Detalhes sobre chuva: {chuvaatual}\n')
    
    arquivo.writelines(frases)
    arquivo.close()
    
    path = os.path.realpath(arquivo.name)
    pathstr = str(path)
    
    def mailing(caminho, email):
        outlook = win32.Dispatch('outlook.application')
        mensagem = outlook.CreateItem(0)
        mensagem.To = email
        mensagem.Subject = "DETALHES DO CLIMA"
        mensagem.HTMLBody = f"""
        <p>Dados Climáticos</p>
        <p>O fuso-horário está seguindo a região {zonatempo} e a consulta foi efetuada em {hrconsultabrt}.</p>
        <p>O sol está nascendo às {sunrisebrt} e se pondo às {sunsetbrt}.</p>
        <p>A temperatura atual é de {"%.1f"%tempatualint}°C e a sensação térmica é de {"%.1f"%sensacaoint}°C.</p>
        <p>A pressão está em {"%.1f"%pressao}atm e a umidade está em {umidade}%, com UVI de {uvi}.</p>
        <p>A velocidade do vento está em {vento}m/s e a direção está em {direcaovento} graus metereológicos.</p>
        <p>*** Detalhes do Clima: {main}\n*** Detalhes sobre chuva: {chuvaatual}.</p>
        <p></p>
        <p></p>
        <p>esse e-mail é AUTOMÁTICO. Por favor não responda.</p>
        """
        anexo = str(caminho)
        mensagem.Attachments.Add(anexo)
        mensagem.Send()
    
    mailing(pathstr, email)

def operacao(end, email):
    end_coord = getcoord(end)
    global saidaend
    saidaend = str(end_coord.get('display_name'))
    saidaendereco['text'] = saidaend
    latitude = end_coord['lat']
    longitude = end_coord['lon']
    
    detalhamento = weather(latitude, longitude)
    
    #obtém informações da função do clima em seprado e organiza
    zonatempo = detalhamento["timezone"]


    atual = detalhamento["current"]
    hrconsulta =  atual.get('dt')
    sunriseatual =  atual.get('sunrise')
    sunsetatual = atual.get('sunset')
    tempatualint = int(atual.get('temp'))
    tempatual = str(atual.get('temp'))
    tempatual1 = tempatual + '°C'
    sensacao = str(atual.get('feels_like'))
    sensacaoint = int(atual.get('feels_like'))
    sensacao1 = tempatual + '°C'
    uvi = atual.get('uvi')
    pressao = atual.get('pressure')
    pressao = pressao *0.000987
    pressao1 = str(pressao)
    pressao1 = (pressao1 + ' atm.')
    umidade = atual.get('humidity')
    umidadefinal = str(umidade)
    umidadefinal = umidadefinal + '%'
    clima = atual.get('weather')
    climamain = clima[0]
    main = climamain.get('description')
    vento = atual.get('wind_speed')
    direcaovento = atual.get('wind_deg')
    chuvaatual = atual.get('rain')
    

    time_zone = pytz.timezone("America/Sao_Paulo")
    saida_timezone['text'] = time_zone


    hrconsultabrt = datetime.fromtimestamp(hrconsulta, time_zone).strftime('%a - %d/%m/%Y - %H:%M')
    saida_hrconsultabrt['text'] = hrconsultabrt
    sunrisebrt = datetime.fromtimestamp(sunriseatual, time_zone).strftime('%H:%M')
    saida_sunrisebrt['text'] = sunrisebrt
    sunsetbrt = datetime.fromtimestamp(sunsetatual, time_zone).strftime('%H:%M')
    saida_sunsetbrt['text'] = sunsetbrt
    saida_tempatual['text'] = tempatual1
    saida_sensacao['text'] = sensacao1
    saida_pressao['text'] = pressao1
    saida_umidade['text'] = umidadefinal
    saida_detalhes['text'] = main
    
    files(zonatempo,hrconsultabrt,sunrisebrt,sunsetbrt,tempatualint,sensacaoint,pressao,umidade,uvi,vento,direcaovento,main,chuvaatual, email)


tela = tk.Tk()
tela.title('Previsão do Tempo')
window_width = 1200
window_height = 500
screen_width = tela.winfo_screenwidth()
screen_height = tela.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
tela.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
tela.resizable(False,False)
tela.attributes('-alpha',0.9)
tela.attributes('-fullscreen', True)
tela.iconbitmap('./173620.ico')
fontetitulo = tkFont.Font(family="Arial", size=15)
fontetitulo1 = tkFont.Font(family="Arial bold", size=20)
fontetitulo2 = tkFont.Font(family="Arial bold", size=15)
fontedescricao = tkFont.Font(family="Arial", size=12)

mainframe = Frame(tela)
mainframe.pack(fill=BOTH, expand=1)
telas = Canvas(mainframe)
telas.pack(side=LEFT, fill=BOTH, expand=1)
myscrollbar = tk.Scrollbar(mainframe, orient=VERTICAL, command=telas.yview)
myscrollbar.pack(side=RIGHT, fill=Y)

telas.configure(yscrollcommand=myscrollbar.set)
telas.bind('<Configure>', lambda e: telas.configure(scrollregion=telas.bbox("all")))

scndframe = Frame(telas)
telas.create_window((0,0), window=scndframe, anchor='nw')
scndframe.place(anchor="c", relx=.5, rely=.5)

instrucao = tk.Label(scndframe, text='PREVISÃO DO TEMPO', font=fontetitulo1).pack()


instrucaoend = tk.Label(scndframe, text='Insira seu endereço:', font=fontetitulo).pack()

endereco = tk.StringVar(scndframe)
entrada = tk.Entry(scndframe,textvariable = endereco,width=100).pack()

instrucaoem = tk.Label(scndframe, text='Insira seu e-mail:',font=fontetitulo).pack()
email = tk.StringVar(scndframe)
entrada2 = tk.Entry(scndframe, textvariable= email,width=100).pack()

botaoexecute = tk.Button(scndframe, text='EXECUTAR',command=lambda:operacao(end=endereco.get(),email=email.get())).pack()

legendaendereco = Label(scndframe, text='Endereço localizado:',background='LightBlue1',font=fontetitulo2)
legendaendereco.pack()
saidaendereco = Label(scndframe, text='',background='LightBlue1',font=fontedescricao)
saidaendereco.pack()

legenda_timezone = Label(scndframe, text='Os horários à seguir estão seguindo o timezone:',background='LightBlue1', font=fontetitulo2)
legenda_timezone.pack()
saida_timezone = Label(scndframe, text='',background='LightBlue1',font=fontedescricao)
saida_timezone.pack()

legenda_hrconsultabrt = Label(scndframe, text='A hora de consulta é:',background='LightBlue1', font=fontetitulo2)
legenda_hrconsultabrt.pack()
saida_hrconsultabrt = Label(scndframe, text='',background='LightBlue1',font=fontedescricao)
saida_hrconsultabrt.pack()

legenda_sunrisebrt = Label(scndframe, text='O Sol está nascendo às:',background='LightBlue1', font=fontetitulo2)
legenda_sunrisebrt.pack()
saida_sunrisebrt = Label(scndframe, text='',background='LightBlue1',font=fontedescricao)
saida_sunrisebrt.pack()

legenda_sunsetbrt = Label(scndframe, text='O Sol está se pondo às:',background='LightBlue1', font=fontetitulo2)
legenda_sunsetbrt.pack()
saida_sunsetbrt = Label(scndframe, text='',background='LightBlue1',font=fontedescricao)
saida_sunsetbrt.pack()

legenda_tempatual = Label(scndframe, text='A temperatura atual está em:',background='LightBlue1', font=fontetitulo2)
legenda_tempatual.pack()
saida_tempatual = Label(scndframe, text='',background='LightBlue1',font=fontedescricao)
saida_tempatual.pack()

legenda_sensacao = Label(scndframe, text='A temperatura atual está em:',background='LightBlue1', font=fontetitulo2)
legenda_sensacao.pack()
saida_sensacao = Label(scndframe, text='',background='LightBlue1',font=fontedescricao)
saida_sensacao.pack()

legenda_pressao = Label(scndframe, text='A pressão atual está em:',background='LightBlue1', font=fontetitulo2)
legenda_pressao.pack()
saida_pressao = Label(scndframe, text='',background='LightBlue1',font=fontedescricao)
saida_pressao.pack()

legenda_umidade = Label(scndframe, text='A umidade atual está em:',background='LightBlue1', font=fontetitulo2)
legenda_umidade.pack()
saida_umidade = Label(scndframe, text='',background='LightBlue1',font=fontedescricao)
saida_umidade.pack()

legenda_detalhes = Label(scndframe, text='Detalhes sobre o clima:',background='LightBlue1', font=fontetitulo2)
legenda_detalhes.pack()
saida_detalhes = Label(scndframe, text='',background='LightBlue1',font=fontedescricao)
saida_detalhes.pack()


scndframe.mainloop()