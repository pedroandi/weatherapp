'''
Projeto de Software II - Universidade Positivo - Eng.Comp.
Alunos: Gabriel França e Pedro Andilossi

Projeto envolvendo Python, APIs e interface TKINTER.

follow on git @b4ndo
'''

'''

libs usadas
tkinter: interface
datetime - ajuste do tempo do formato unix timestamp para formato comum em strng
pytz - timezone para horário
'''

from tkinter import *
import tkinter as tk
import tkinter.font as tkFont
from filingmailing import files
from getcoordenadas import getcoord
from weather import weather
from datetime import datetime
import pytz

#variável p/ armazenar a saida a ser obtida na API de coordenadas
saidaend = ""

def operacao(end, email): #como parametro dessa função precisaremos do endereço e email apenas, esses sendo solicitados na tela do usuário
    
    end_coord = getcoord(end) #chama a API de geolocalização e
    saidaend = str(end_coord.get('display_name')) #da resposta já tratada de json p/ dic, pega o que está no item 'display_name' para obter o nome completo do local
    saidaendereco['text'] = saidaend
    
    # usando a mesma lógica do item acima, separa a latitude e longitude do endereço em suas respectivas variáveis
    latitude = end_coord['lat']
    longitude = end_coord['lon']
    
    detalhamento = weather(latitude, longitude) #chama a API passando latitude e longitude e armazena em uma variável
    
    #à partir daqui, a usa os dados retornados da API e armazenados na variável detalhamento e armazena cada informação em uma nova variável
    #observe que alguns itens vem como itens de dicionário, entretanto temos listas dentro de dicionários e dicionários dentro de dicionários que precisamos tratar
    zonatempo = detalhamento["timezone"]
    atual = detalhamento["current"]
    hrconsulta =  atual.get('dt')
    sunriseatual =  atual.get('sunrise')
    sunsetatual = atual.get('sunset')
    tempatualint = int(atual.get('temp'))
    tempatual = str(atual.get('temp'))
    tempatual1 = tempatual + '°C'
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
    
    time_zone = pytz.timezone("America/Sao_Paulo") #uso do pytz para fornecer a timezone, no caso gmt-3 - ou horário de Brasília
    saida_timezone['text'] = time_zone

    #tratamento do formato das horas e envio para as 'labels' do TK para serem exibidas na tela do usuário
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
    
    #chamada da função que irá posteriormente escrever no arquivo txt e enviar o e-mail
    files(zonatempo,hrconsultabrt,sunrisebrt,sunsetbrt,tempatualint,sensacaoint,pressao,umidade,uvi,vento,direcaovento,main,chuvaatual, email)


#criação e parametrização da janela
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
tela.iconbitmap('./assets/173620.ico')
fontetitulo = tkFont.Font(family="Arial", size=15)
fontetitulo1 = tkFont.Font(family="Arial bold", size=20)
fontetitulo2 = tkFont.Font(family="Arial bold", size=15)
fontedescricao = tkFont.Font(family="Arial", size=12)

#criação de barra de scroll caso precise descer a tela
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

#titulo da janela, displays e textbox para entrada de dados
instrucao = tk.Label(scndframe, text='PREVISÃO DO TEMPO', font=fontetitulo1).pack()
instrucaoend = tk.Label(scndframe, text='Insira seu endereço:', font=fontetitulo).pack()

#tratamento para passar a entrada como variável de texto
endereco = tk.StringVar(scndframe)
entrada = tk.Entry(scndframe,textvariable = endereco,width=100).pack()
instrucaoem = tk.Label(scndframe, text='Insira seu e-mail:',font=fontetitulo).pack()
email = tk.StringVar(scndframe)
entrada2 = tk.Entry(scndframe, textvariable= email,width=100).pack()

#botão de execução, chama a função operação com os parametros obtidos das entradas acima
botaoexecute = tk.Button(scndframe, text='EXECUTAR',command=lambda:operacao(end=endereco.get(),email=email.get())).pack()

#display das informações
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