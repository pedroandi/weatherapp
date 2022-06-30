'''
libs usadas:
os - uso do sistema operacional p/ manipulação de arquivos
win32 - funções do e-mail
'''

import os
import win32com.client as win32

def files(zonatempo,hrconsultabrt,sunrisebrt,sunsetbrt,tempatualint,sensacaoint,pressao,umidade,uvi,vento,direcaovento,main,chuvaatual, email):
    
    #abre o arquivo, cria as frases e adiciona ao arquivo, método 'w' faz que sobrescreva toda vez que usado
    arquivo = open('./assets/temperatura.txt', 'w')
    frases = list()
    frases.append(f'O fuso-horário está seguindo a região {zonatempo} e a consulta foi efetuada em {hrconsultabrt}\n')
    frases.append(f'O sol está nascendo às {sunrisebrt} e se pondo às {sunsetbrt}\n')
    frases.append(f'A temperatura atual é de {"%.1f"%tempatualint}°C e a sensação térmica é de {"%.1f"%sensacaoint}°C.\n')
    frases.append(f'A pressão está em {"%.1f"%pressao}atm e a umidade está em {umidade}%, com UVI de {uvi}.\n')
    frases.append(f'A velocidade do vento está em {vento}m/s e a direção está em {direcaovento} graus metereológicos.\n')
    frases.append(f'*** Detalhes do Clima: {main}\n*** Detalhes sobre chuva: {chuvaatual}\n')
    arquivo.writelines(frases)
    arquivo.close()
    
    #obtém o local onde o arquivo foi criado
    path = os.path.realpath(arquivo.name)
    pathstr = str(path)
    
    #função do e-mail, tem que passar como parametro o local do arquivo e endereço de email
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