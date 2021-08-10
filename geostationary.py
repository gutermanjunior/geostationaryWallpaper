import os
import datetime
import time
import requests
import struct
import ctypes
from PIL import Image

# Listar Array
def imprimir(array):
    for iten in array: print(iten)

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

def entrada_horas():
    entrada = 1 #input('Baixar arquivo de quantas horas atras? ')
    if entrada == '':
        horas = 1/3
    else:
        horas = int(entrada)
    return horas

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
    if mostrar == True: imprimir(arquivos)
    return arquivos

# Arquivos da Pasta que começam com data
def flistapasta_Filter():
    entries = flistapasta()
    nome_do_arquivo = [iten for iten in entries if iten[0:11].isnumeric() == True]
    return nome_do_arquivo

def is_64_windows():
    """Find out how many bits is OS. """
    return struct.calcsize('P') * 8 == 64

def get_sys_parameters_info():
    """Based on if this is 32bit or 64bit returns correct version of SystemParametersInfo function. """
    return ctypes.windll.user32.SystemParametersInfoW if is_64_windows() \
        else ctypes.windll.user32.SystemParametersInfoA

def change_wallpaper(WALLPAPER_PATH):
    SPI_SETDESKWALLPAPER = 20
    sys_parameters_info = get_sys_parameters_info()
    r = sys_parameters_info(SPI_SETDESKWALLPAPER, 0, WALLPAPER_PATH, 3)

    # When the SPI_SETDESKWALLPAPER flag is used, SystemParametersInfo returns TRUE unless there is an error (like when the specified file doesn't exist).
    if not r:
        print(ctypes.WinError())

def mudar_Wallpaper():
    CAMINHO = r"C:\Users\Guterman\Pictures\WallpaperGOES"
    Nome = flistapasta_Filter()[-1]
    WALLPAPER_PATH = CAMINHO + "\\" + Nome
    image = Image.open(WALLPAPER_PATH)

    new_image = image.resize((1080,1080))
    new_image.save('TEMP\\1080x1080_' + Nome)
    

    WALLPAPER_PATH = r'C:\Users\Guterman\Pictures\WallpaperGOES\TEMP\\1080x1080_' + str(Nome)
    #time.sleep(3)
    change_wallpaper(WALLPAPER_PATH)
    print(str(datetime.datetime.now()) + ' || Esperado GOES: ' + fdatahora() + ' || Formato de agora: ' + fdatahora(3*60))
    print(str(datetime.datetime.now()) + ' -----> Wallpaper atualizado para o arquivo ' + Nome)

def main():
    while True:
        deltas = fdeltas(entrada_horas())
        for delta in deltas:
            nome = fdownload_file(delta)
            url = furl(nome)
            fdownload(nome, url, fexiste(nome))
        mudar_Wallpaper()
        time.sleep(1*60*10)
        #input('Ok?') # hold final

main()

