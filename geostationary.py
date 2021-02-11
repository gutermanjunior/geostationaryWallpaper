import os
import datetime
import requests

# Data agora
def fdatahora(delay = 20): # Retorna 'YYYYdddHHmm'
    agoraGOES = datetime.datetime.utcnow() - datetime.timedelta(minutes = delay)
    ano = agoraGOES.timetuple().tm_year
    diaAno = agoraGOES.timetuple().tm_yday
    if diaAno < 100:
        diaAno = '0' + str(diaAno)
    hora = agoraGOES.timetuple().tm_hour
    if hora == 0:
        hora = '00'
    elif hora > 0 and hora < 10:
        hora = '0' + str(hora)
    minuto = agoraGOES.timetuple().tm_min
    minutoGOES = minuto - (minuto%10)
    if minutoGOES == 0:
        minutoGOES = '00'
    elif minutoGOES > 0 and minutoGOES < 10:
        minutoGOES = '0' + str(minutoGOES)
    datahora = str(ano) + str(diaAno) + str(hora) + str(minutoGOES)
    
    return datahora

# Data Lista das ultimas H horas
def fdeltas(horas = 2): # Retorna lista de deltas
    deltas = []
    for delta in range(int(horas*60+20), 10, -10):
        deltas.append(delta)
    #for delta in deltas:
    #    print(fdatahora(delta))
    return deltas

# Arquivo GOES
def fdownload_file(delay = 20): # Retorna nome do arquivo
    return fdatahora(delay) + '_GOES16-ABI-FD-GEOCOLOR-5424x5424.jpg'

def furl(nome_arquivo, delay = 20): # Retorna o URL do arquivo a ser baixado
    url_directory = 'https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/GEOCOLOR/'
    return url_directory + nome_arquivo

# Verifica se o arquivo já existe
def fexiste(nome_arquivo): # Retorna True ou False, entra o nome de um arquivo
    existe = False
    arquivos = flistapasta()
    for arquivo in arquivos:
        if nome_arquivo == arquivo:
            existe = True
            if existe:
                print(nome_arquivo + ' já existe')
    return existe

# Download
def fdownload(nome, url, existe):
    if existe == False:
        r = requests.get(url)
        if r.status_code == 200:
            open(nome, 'wb').write(r.content)
            print('Baixado o arquivo ' + nome)
        elif r.status_code == 404:
            print('Erro 404 - Arquivo não encontrado: ' + nome)
        else:
            print('Erro desconhecido')

# Arquivos da Pasta
def flistapasta(mostrar = False): # Retorna lista de arquivos da pasta
    entries = os.listdir()
    entries.sort()
    """ print(os.path.basename(__file__))
    print(os.path.dirname(__file__))
    print(__file__) """
    arquivos = entries.copy()
    arquivos.remove(os.path.basename(__file__))
    if mostrar == True:
        for i in arquivos:
            print(i)
    return arquivos

def entrada_horas():
    entrada = input('Baixar arquivo de quantas horas atras? ')
    if entrada == '':
        horas = 1/3
    else:
        horas = int(entrada)
    return horas

def main():
    deltas = fdeltas(entrada_horas())
    for delta in deltas:
        nome = fdownload_file(delta)
        url = furl(nome)
        fdownload(nome, url, fexiste(nome))

main()