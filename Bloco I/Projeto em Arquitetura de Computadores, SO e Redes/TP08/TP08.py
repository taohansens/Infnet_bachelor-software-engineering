# Importação de bibliotecas
import pickle
import platform
import re
import socket
import sys
from datetime import datetime

import cpuinfo
from urllib.request import urlopen

import netifaces
import nmap
import psutil
import pygame
from dateutil.tz import tz
from pygame.locals import *

import os

import sched
import time

# INICIA PYGAME
pygame.init()
CLOCK = pygame.time.Clock()
HZ = 60

# FONTES
pygame.font.init()
FONTE_TITLE = pygame.font.SysFont("segoe-ui-bold", 60)
FONTE_INFO = pygame.font.SysFont("segoe-ui", 18)
FONTE_INFO_BOLD = pygame.font.SysFont("segoe-ui-bold", 26)
FONTE_SUBINFO_BOLD = pygame.font.SysFont("segoe-ui-bold", 20)
FONTE_PERCENT = pygame.font.SysFont("segoe", 26)
FONTE_PERCENT_PROC = pygame.font.SysFont("segoe", 20)

# Iniciando a janela principal
LARGURA_TELA = 600
ALTURA_TELA = 600
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Gerenciador de Recursos")

# CORES
CINZA = (236, 240, 241)
ESCURO = (52, 73, 94)
VERMELHO = (231, 76, 60)
AZUL = (52, 152, 219)
BRANCO = (255, 255, 255)

# CONSTANTES COM O TAMANHO DA TELA
TAM_TELA = (LARGURA_TELA, 500)
TAM_SETA = (LARGURA_TELA, 100)

ESPESSURA_BARRA = 14

info_cpu = cpuinfo.get_cpu_info()


# ************************************************************ #
#                      Processador
# ************************************************************ #
def processador():
    uso_cpu = psutil.cpu_percent(percpu=True)
    surface_02 = pygame.Surface(TAM_TELA)
    surface_02.fill(CINZA)
    # Posições em pixels
    pos_altura_barra = 50

    # Textos Info processador
    # Título
    titulo = FONTE_TITLE.render("Uso do Processador", True, ESCURO)
    surface_02.blit(titulo, (40, 20))
    # Informações
    processor_name = "{}".format(info_cpu['brand_raw'])
    sistema_op = "SO: {} ({})".format(platform.system(), platform.platform())
    processor_cores = "Clock: {} GHz | Palavra: {} bits | Arch: {}".format(psutil.cpu_freq().current / 1000,
                                                                           info_cpu['bits'], info_cpu['arch'])
    freq_info = "Frequência: {}Mhz / {}Mhz".format(psutil.cpu_freq().current, psutil.cpu_freq().max)
    processor_cores_obj = FONTE_INFO.render(processor_cores, True, ESCURO)
    sistema_op_obj = FONTE_INFO.render(sistema_op, True, ESCURO)
    processor_name_obj = FONTE_INFO.render(processor_name, True, ESCURO)
    freq_info_obj = FONTE_INFO.render(freq_info, True, ESCURO)
    surface_02.blit(processor_name_obj, (40, pos_altura_barra + 20))
    surface_02.blit(processor_cores_obj, (40, pos_altura_barra + 45))
    surface_02.blit(sistema_op_obj, (40, pos_altura_barra + 70))
    surface_02.blit(freq_info_obj, (40, pos_altura_barra + 92))

    qtd_nucleos = "{} threads | {} núcleos".format(psutil.cpu_count(), psutil.cpu_count(logical=False))
    qtd_nucleos_obj = FONTE_INFO_BOLD.render(qtd_nucleos, True, ESCURO)
    surface_02.blit(qtd_nucleos_obj, (210, 175))

    # Laço sobre todas os núcleos.
    var_barra = 0
    pos_final_barra = int(LARGURA_TELA - LARGURA_TELA * 0.15)
    for i in uso_cpu:
        # texto da % de cada processador.
        perc_texto = "{}%".format(i)
        percentagem_uso = FONTE_PERCENT_PROC.render(perc_texto, True, ESCURO)
        surface_02.blit(percentagem_uso, (15, 200 + var_barra))

        pygame.draw.rect(surface_02, AZUL, (60, 200 + var_barra, pos_final_barra, ESPESSURA_BARRA))
        pos_final_barra_uso = pos_final_barra * (i / 100)
        pygame.draw.rect(surface_02, VERMELHO, (60, 200 + var_barra, pos_final_barra_uso, ESPESSURA_BARRA))
        var_barra += 25
    TELA.blit(surface_02, (0, 0))


# ************************************************************ #
#                      Memória RAM
# ************************************************************ #
def memoria_ram():
    memoria = psutil.virtual_memory()
    surface_01 = pygame.Surface(TAM_TELA)
    surface_01.fill(CINZA)
    # Posições em pixels
    pos_altura_barra = 110
    pos_final_barra = int(LARGURA_TELA - LARGURA_TELA * 0.15)
    # Desenha barra total (em azul)
    pygame.draw.rect(surface_01, AZUL, (70, pos_altura_barra, pos_final_barra, ESPESSURA_BARRA))
    # Barra de uso (em vermelho)
    pos_final_barra_uso = pos_final_barra * (memoria.percent / 100)
    pygame.draw.rect(surface_01, VERMELHO, (70, pos_altura_barra, pos_final_barra_uso, ESPESSURA_BARRA))

    # Início Textos
    perc_texto = "{}%".format(memoria.percent)

    titulo = FONTE_TITLE.render("Uso Memória RAM", True, ESCURO)
    percentagem_uso = FONTE_PERCENT.render(perc_texto, True, ESCURO)
    surface_01.blit(titulo, (40, 20))
    surface_01.blit(percentagem_uso, (15, pos_altura_barra))

    # Memoria total
    memoria_total = "Memória física total: {:g} GB".format(round(memoria.total / (1024.0 ** 3), 0))
    memoria_total_obj = FONTE_INFO.render(memoria_total, True, ESCURO)
    surface_01.blit(memoria_total_obj, (pos_final_barra - 150, pos_altura_barra - 30))

    # Memoria Física total
    memoria_livre = "Memória em uso: {:.2f} GB | Memória livre: {:.2f} GB".format(memoria.used / (1024.0 ** 3),
                                                                                  memoria.free / (1024.0 ** 3))
    memoria_livre_obj = FONTE_INFO.render(memoria_livre, True, ESCURO)
    surface_01.blit(memoria_livre_obj, (LARGURA_TELA // 5, pos_altura_barra + 20))
    TELA.blit(surface_01, (0, 0))


# ************************************************************ #
#                      Disco
# ************************************************************ #
def disco():
    disk = verifica_discos()
    surface_03 = pygame.Surface(TAM_TELA)
    surface_03.fill(CINZA)
    # Posições em pixels
    pos_altura_barra = 110
    pos_final_barra = int(LARGURA_TELA - LARGURA_TELA * 0.15)
    # Desenha barra total (em azul)
    pygame.draw.rect(surface_03, AZUL, (70, pos_altura_barra, pos_final_barra, ESPESSURA_BARRA))
    # Barra de uso (em vermelho)
    pos_final_barra_uso = pos_final_barra * (disk[5] / 100)
    pygame.draw.rect(surface_03, VERMELHO, (70, pos_altura_barra, pos_final_barra_uso, ESPESSURA_BARRA))

    # Início Textos
    perc_texto = "{}%".format(disk[5])

    titulo = FONTE_TITLE.render("Espaço Total em Disco", True, ESCURO)
    percentagem_uso = FONTE_PERCENT.render(perc_texto, True, ESCURO)
    surface_03.blit(titulo, (40, 20))
    surface_03.blit(percentagem_uso, (15, pos_altura_barra))

    # Espaço total

    qtd_total = "Encontrados: {:g}".format(round(disk[0]))
    qtd_total_obj = FONTE_INFO.render(qtd_total, True, ESCURO)
    mont_hds = "{}".format(disk[1])
    mont_hds_obj = FONTE_INFO.render(mont_hds, True, ESCURO)
    surface_03.blit(qtd_total_obj, (pos_final_barra - 50, pos_altura_barra + 20))
    surface_03.blit(mont_hds_obj, (pos_final_barra - 40, pos_altura_barra + 40))

    # Espaço livre/ocupado no hd
    espaco_livre = "Espaço livre: {:.2f} GB".format(disk[4] / (1024.0 ** 3))
    espaco_ocupado = "Espaço usado: {:.2f} GB".format(disk[3] / (1024.0 ** 3))
    espaco_livre_obj = FONTE_INFO.render(espaco_livre, True, ESCURO)
    espaco_ocupado_obj = FONTE_INFO.render(espaco_ocupado, True, ESCURO)
    surface_03.blit(espaco_livre_obj, (70, pos_altura_barra + 20))
    surface_03.blit(espaco_ocupado_obj, (70, pos_altura_barra + 40))
    TELA.blit(surface_03, (0, 0))


# ************************************************************ #
#                      Surface Rede
# ************************************************************ #
def rede(ip_pub):
    # Interface de rede terá que ser colocada manualmente, variação muito grande.
    dic_interfaces = psutil.net_if_addrs()
    if "Wi-Fi 6" in dic_interfaces:
        INTERFACE_REDE = "Wi-Fi 6"
    elif "Ethernet" in dic_interfaces:
        INTERFACE_REDE = "Ethernet"
    else:
        INTERFACE_REDE = "Wi-Fi 2"

    ip_rede = dic_interfaces[INTERFACE_REDE][1].address
    net_mask = dic_interfaces[INTERFACE_REDE][1].netmask
    ip_local = "IPv4 Local: {}".format(ip_rede)
    ip_public = "IP Público: {}".format(ip_pub)
    ip_netmask = "Máscara de Sub-rede: {}".format(net_mask)
    ip_local_obj = FONTE_TITLE.render(ip_local, True, ESCURO)
    ip_netmask_obj = FONTE_INFO.render(ip_netmask, True, ESCURO)
    ip_pub_obj = FONTE_TITLE.render(ip_public, True, ESCURO)
    surface_04 = pygame.Surface(TAM_TELA)
    surface_04.fill(CINZA)
    titulo = FONTE_TITLE.render("Informações de Rede", True, ESCURO)
    surface_04.blit(titulo, (40, 20))
    surface_04.blit(ip_local_obj, (20, 200))
    surface_04.blit(ip_pub_obj, (20, 240))
    surface_04.blit(ip_netmask_obj, (20, 290))

    TELA.blit(surface_04, (0, 0))


# ************************************************************ #
#                      Surface Resumo
# ************************************************************ #
def resumo():
    surface_05 = pygame.Surface(TAM_TELA)
    surface_05.fill(CINZA)
    pos_altura_barra = 75

    # Título
    titulo = FONTE_TITLE.render("Resumo de Informações", True, ESCURO)
    surface_05.blit(titulo, (40, 20))

    # ************************************************************ #
    #                      Processador
    # ************************************************************ #
    titulo = FONTE_SUBINFO_BOLD.render("Processador", True, ESCURO)
    surface_05.blit(titulo, (40, 80))
    processor_name = "{}".format(info_cpu['brand_raw'])
    sistema_op = "SO: {} ({})".format(platform.system(), platform.platform())
    processor_cores = "Clock: {} GHz | Palavra: {} bits | Arch: {}".format(psutil.cpu_freq().current / 1000,
                                                                           info_cpu['bits'], info_cpu['arch'])
    freq_info = "Frequência: {}Mhz / {}Mhz".format(psutil.cpu_freq().current, psutil.cpu_freq().max)
    processor_cores_obj = FONTE_INFO.render(processor_cores, True, ESCURO)
    sistema_op_obj = FONTE_INFO.render(sistema_op, True, ESCURO)
    processor_name_obj = FONTE_INFO.render(processor_name, True, ESCURO)
    freq_info_obj = FONTE_INFO.render(freq_info, True, ESCURO)
    surface_05.blit(processor_name_obj, (40, pos_altura_barra + 20))
    surface_05.blit(processor_cores_obj, (40, pos_altura_barra + 45))
    surface_05.blit(sistema_op_obj, (40, pos_altura_barra + 70))
    surface_05.blit(freq_info_obj, (40, pos_altura_barra + 92))

    qtd_nucleos = "{} threads | {} núcleos".format(psutil.cpu_count(), psutil.cpu_count(logical=False))
    qtd_nucleos_obj = FONTE_INFO.render(qtd_nucleos, True, ESCURO)
    surface_05.blit(qtd_nucleos_obj, (410, 100))

    uso_cpu = psutil.cpu_percent(interval=0)

    perc_texto = "{}%".format(uso_cpu)
    titulo = FONTE_PERCENT.render("Uso do Processador", True, ESCURO)
    percentagem_uso = FONTE_PERCENT.render(perc_texto, True, ESCURO)
    surface_05.blit(titulo, (410, 85))
    surface_05.blit(percentagem_uso, (460, 130))

    # Desenha barra total (em azul)
    pygame.draw.rect(surface_05, AZUL, (430, 150, 100, ESPESSURA_BARRA))
    # Barra de uso (em vermelho)
    pos_final_barra_uso = 100 * (uso_cpu / 100)
    pygame.draw.rect(surface_05, VERMELHO, (430, 150, pos_final_barra_uso, ESPESSURA_BARRA))

    # ************************************************************ #
    #                      Memória RAM
    # ************************************************************ #
    memoria = psutil.virtual_memory()
    titulo_memoria = FONTE_SUBINFO_BOLD.render("Memória", True, ESCURO)
    surface_05.blit(titulo_memoria, (40, 210))
    perc_texto = "{}%".format(memoria.percent)

    percentagem_uso = FONTE_PERCENT.render(perc_texto, True, ESCURO)
    surface_05.blit(percentagem_uso, (40, 230))

    pos_altura_barra = 230
    pos_final_barra = int(LARGURA_TELA - LARGURA_TELA * 0.2)
    # Desenha barra total (em azul)
    pygame.draw.rect(surface_05, AZUL, (100, pos_altura_barra, pos_final_barra, 20))
    # Barra de uso (em vermelho)
    pos_final_barra_uso = pos_final_barra * (memoria.percent / 100)
    pygame.draw.rect(surface_05, VERMELHO, (100, pos_altura_barra, pos_final_barra_uso, 20))

    memoria_total = "Memória física total: {:g} GB".format(round(memoria.total / (1024.0 ** 3), 0))
    memoria_total_obj = FONTE_INFO.render(memoria_total, True, ESCURO)
    surface_05.blit(memoria_total_obj, (pos_final_barra - 150, pos_altura_barra - 30))

    # Memoria Física total
    memoria_livre = "Memória em uso: {:.2f} GB | Memória livre: {:.2f} GB".format(memoria.used / (1024.0 ** 3),
                                                                                  memoria.free / (1024.0 ** 3))
    memoria_livre_obj = FONTE_INFO.render(memoria_livre, True, ESCURO)
    surface_05.blit(memoria_livre_obj, (LARGURA_TELA // 5, pos_altura_barra + 20))

    # ************************************************************ #
    #                            Discos
    # ************************************************************ #
    disk = verifica_discos()
    # Posições em pixels
    pos_altura_barra = 320
    pos_final_barra = int(LARGURA_TELA - LARGURA_TELA * 0.2)
    # Desenha barra total (em azul)
    pygame.draw.rect(surface_05, AZUL, (100, pos_altura_barra, pos_final_barra, 20))
    # Barra de uso (em vermelho)
    pos_final_barra_uso = pos_final_barra * (disk[5] / 100)
    pygame.draw.rect(surface_05, VERMELHO, (100, pos_altura_barra, pos_final_barra_uso, 20))

    # Início Textos
    perc_texto = "{}%".format(disk[5])

    titulo = FONTE_SUBINFO_BOLD.render("Espaço em Disco", True, ESCURO)
    percentagem_uso = FONTE_PERCENT.render(perc_texto, True, ESCURO)
    surface_05.blit(titulo, (40, 300))
    surface_05.blit(percentagem_uso, (40, pos_altura_barra))

    # Espaço total
    qtd_total = "Encontrados: {:g}".format(round(disk[0]))
    qtd_total_obj = FONTE_INFO.render(qtd_total, True, ESCURO)
    mont_hds = "{}".format(disk[1])
    mont_hds_obj = FONTE_INFO.render(mont_hds, True, ESCURO)
    surface_05.blit(qtd_total_obj, (pos_final_barra - 50, pos_altura_barra + 20))
    surface_05.blit(mont_hds_obj, (pos_final_barra - 40, pos_altura_barra + 40))

    # Espaço livre/ocupado no hd
    espaco_livre = "Espaço livre: {:.2f} GB".format(disk[4] / (1024.0 ** 3))
    espaco_ocupado = "Espaço usado: {:.2f} GB".format(disk[3] / (1024.0 ** 3))
    espaco_livre_obj = FONTE_INFO.render(espaco_livre, True, ESCURO)
    espaco_ocupado_obj = FONTE_INFO.render(espaco_ocupado, True, ESCURO)
    surface_05.blit(espaco_livre_obj, (70, pos_altura_barra + 20))
    surface_05.blit(espaco_ocupado_obj, (70, pos_altura_barra + 40))

    # ************************************************************ #
    #                   Informações de REDE.
    # ************************************************************ #
    dic_interfaces = psutil.net_if_addrs()
    if "Wi-Fi 6" in dic_interfaces:
        INTERFACE_REDE = "Wi-Fi 6"
    elif "Ethernet" in dic_interfaces:
        INTERFACE_REDE = "Ethernet"
    else:
        INTERFACE_REDE = "Wi-Fi"
    ip_rede = obter_ip_local()
    net_mask = dic_interfaces[INTERFACE_REDE][1].netmask
    ip_local = "IPv4 Local: {}".format(ip_rede)
    ip_public = "IP Público: {}".format(ip_publico())
    ip_netmask = "Máscara de Sub-rede: {}".format(net_mask)
    ip_local_obj = FONTE_INFO.render(ip_local, True, ESCURO)
    ip_netmask_obj = FONTE_INFO.render(ip_netmask, True, ESCURO)
    ip_pub_obj = FONTE_INFO.render(ip_public, True, ESCURO)
    titulo = FONTE_SUBINFO_BOLD.render("Informações de Rede", True, ESCURO)
    surface_05.blit(titulo, (40, 400))
    surface_05.blit(ip_local_obj, (40, 420))
    surface_05.blit(ip_pub_obj, (40, 440))
    surface_05.blit(ip_netmask_obj, (40, 460))
    # ************************************************************ #

    TELA.blit(surface_05, (0, 0))


# Verifica todos os discos do usuario:
#   RETORNOS POR POSIÇÃO:
#   qtd_discos[0] [int]
#   string_com_discos[1] [str],
#   espaco_total[2] [int],
#   espaco_usado[3] [int],
#   espaco_livre[4] [int]
#   (TODAS UNIDADES EM BYTES), e a
#   percentagem de uso [5] [int]
def verifica_discos():
    # verifica a quantidade de discos
    qtd_discos = len(psutil.disk_partitions())
    discos = []
    espaco_total = 0
    espaco_usado = 0
    espaco_livre = 0

    # Faz a iteração sobre os retornos do disk_partitions e disk_usage.
    for partition in psutil.disk_partitions():
        discos.append(partition[1])
        espaco_total += psutil.disk_usage(partition[1])[0]
        espaco_usado += psutil.disk_usage(partition[1])[1]
        espaco_livre += psutil.disk_usage(partition[1])[2]

    string_discos = ""
    for i in range(len(discos)):
        string_discos += discos[i] + " "

    # Calcula a porcentagem do uso total.
    percent_usado = round(espaco_usado / espaco_total * 100, 1)
    return qtd_discos, string_discos, espaco_total, espaco_usado, espaco_livre, percent_usado


def timestamp_converter(st_time):
    time = datetime.fromtimestamp(st_time, tz=tz.tzlocal()).strftime('%d/%m/%Y-%H:%M')
    return time


def listagem_diretorio(diretorio):
    class InfoArquivos:
        def __init__(self, nome, tamanho, atime, mtime):
            self.nome = nome
            self.tamanho = tamanho
            self.atime = atime
            self.mtime = mtime

    lista_arquivos = []
    lista_diretorios = []

    if os.path.exists(diretorio):
        l_arquivos = os.listdir(diretorio)
        for arquivo in l_arquivos:
            caminho_arquivo = os.path.join(diretorio, arquivo)
            arquivo_stat = os.stat(caminho_arquivo)
            tamanho = f"{arquivo_stat.st_size // 1024} KB"
            instFile = InfoArquivos(arquivo, tamanho, timestamp_converter(os.stat(caminho_arquivo).st_atime),
                                    timestamp_converter(os.stat(caminho_arquivo).st_mtime))
            if os.path.isfile(caminho_arquivo):
                lista_arquivos.append(instFile)
            elif os.path.isdir(caminho_arquivo):
                lista_diretorios.append(instFile)
            else:
                print('ERROR')

    return lista_arquivos, lista_diretorios


def print_arquivos_terminal(lista):
    header = '{:20}'.format("Nome")
    header = header + '{:20}'.format("Tamanho")
    header = header + '{:20}'.format("Data de Mod.")
    header = header + '{:20}'.format("Data de Cri.")
    print(header)
    for arquivo in lista:
        file = '{:20.20}'.format(arquivo.nome)
        file = file + '{0:20}'.format(arquivo.tamanho)
        file = file + '{:10}'.format(arquivo.atime)
        file = file + '{:>20}'.format(arquivo.mtime)
        print(file)


def arquivos(tipo, l_files):
    surface = pygame.Surface(TAM_TELA)
    surface.fill(CINZA)

    # Posições em pixels
    pos_altura_barra = 50

    # Textos Info processador
    # Título
    titulo = FONTE_TITLE.render(f"Listagem de {tipo}", True, ESCURO)
    subtitulo = FONTE_SUBINFO_BOLD.render(f"Diretório: {os.environ['HOMEPATH']}", True, ESCURO)

    surface.blit(titulo, (40, 20))
    surface.blit(subtitulo, (40, 70))

    header = '{:20}'.format("Nome")
    header = header + '{:20}'.format("Tamanho")
    header = header + '{:25}'.format("Data de Mod.")
    header = header + '{:>25}'.format("Data de Cri.")

    header_table = FONTE_SUBINFO_BOLD.render(header, True, ESCURO)
    surface.blit(header_table, (60, pos_altura_barra + 50))

    # impressão de arquivos
    distancia_px = 10
    for arquivo in l_files:
        distancia_px += 20
        file = '{:10.10}'.format(arquivo.nome)
        file = file + '{0:^30}'.format(arquivo.tamanho)
        file = file + '{0:20}'.format(arquivo.atime)
        file = file + '{:>10}'.format(arquivo.mtime)
        ls_arquivo = FONTE_INFO.render(file, True, ESCURO)
        surface.blit(ls_arquivo, (40, 90 + distancia_px))
    TELA.blit(surface, (0, 0))


def print_processos_terminal(l_process):
    header = '{:8}'.format("PID")
    header = header + '{:20}'.format("Nome Processo")
    header = header + '{:10}'.format("Status")
    header = header + '{:10}'.format("Memória RSS/VMS")
    print(header)
    for process in l_process:
        info = '{:<8}'.format(process['pid'])
        info = info + '{:20}'.format(process['name'])
        info = info + '{:10}'.format(process['status'])
        info = info + '{:10} | {}'.format(process['memory_info'].rss, process['memory_info'].vms)
        print(info)


def processos():
    l_process = []
    for item in psutil.process_iter():
        l_process.append(item.as_dict(attrs=['pid', 'name', 'status', 'cpu_times', 'memory_info']))
    surface = pygame.Surface(TAM_TELA)
    surface.fill(CINZA)
    titulo = FONTE_TITLE.render("Processos em execução", True, ESCURO)
    surface.blit(titulo, (40, 20))
    info = FONTE_INFO_BOLD.render(f"{len(l_process)} Processos listados no terminal.", True, ESCURO)
    surface.blit(info, (40, 120))
    TELA.blit(surface, (0, 0))

    return l_process


def print_network_nmap(network):
    surface = pygame.Surface(TAM_TELA)
    surface.fill(CINZA)
    titulo = FONTE_TITLE.render(f"Nmap Scanner", True, ESCURO)
    surface.blit(titulo, (40, 20))
    qtd_ips = len(network[0])
    info = FONTE_INFO_BOLD.render(f"{qtd_ips} IP(s) localizado(s) na busca.", True, ESCURO)
    info2 = FONTE_INFO_BOLD.render(f"<<< Outros hosts e portas exibidos no console >>>", True, ESCURO)
    surface.blit(info, (40, 80))
    surface.blit(info2, (40, 100))

    y = 180
    x = 200
    title_ip = FONTE_SUBINFO_BOLD.render(f"IP UTILIZADO NA BUSCA", True, ESCURO)
    surface.blit(title_ip, (x, y - 20))

    if network[1] in network[0]:
        ip_localizado = FONTE_TITLE.render(f"{network[1]}", True, AZUL)
        surface.blit(ip_localizado, (x, y))
        y += 80
        title_ports = FONTE_SUBINFO_BOLD.render(f"PORTA | STATUS | NOME", True, VERMELHO)
        surface.blit(title_ports, (x, y - 20))
        for port in network[0][network[1]]:
            info_ip = FONTE_INFO_BOLD.render(
                f"{port} - {network[0][network[1]][port]['state']} - {network[0][network[1]][port]['name']}", True, ESCURO)
            surface.blit(info_ip, (x, y))
            y += 20
    TELA.blit(surface, (0, 0))


def ips_nmap():
    print("Scanner de Rede")
    print("Escolha o IP:")
    print("1. Meu IP\n2. Desejo digitar outro ip.")
    try:
        escolha = int(input("Digite o que você deseja: "))
    except:
        print("Tente novamente.")
        escolha = int(input("Digite o que você deseja: "))

    ip = obter_ip_local()
    if escolha == 1:
        print("IP:", ip)
    if escolha == 2:
        ip_digitado = input("Digite o endereço ip desejado: ")
        ip = ip_digitado

    subnet = input('Digite a máscara de sub-rede CIDR (padrão=25): ')

    nm = nmap.PortScanner()
    nm.scan(hosts=ip + "/" + subnet, arguments="-F -n")

    ips_up = {}
    if nm.all_hosts():
        for host in nm.all_hosts():
            if nm[host].state() == 'up':
                try:
                    ips_up[host] = nm[host]['tcp']
                except:
                    ValueError()
    else:
        print("não encontrado")
    for host in ips_up:
        print("IP: ", host)
        for port in ips_up[host]:
            print(f"{port} - {ips_up[host][port]['state']} - {ips_up[host][port]['name']}")
        print("=========")
    return ips_up, ip


def infor_adapters():
    cont = 1
    list_of_adapters = []
    for rede in psutil.net_if_addrs():
        list_of_adapters.append(rede)
        print(f"{cont}... {rede}")
        cont += 1
    escolha = int(input("Digite qual interface de rede você deseja visualizar: "))
    adapter = psutil.net_if_addrs().get(list_of_adapters[escolha - 1])

    for snicaddr in adapter:
        if snicaddr.family == socket.AF_INET:
            ipv4 = snicaddr.address
            netmask = snicaddr.netmask
        elif snicaddr.family == socket.AF_INET6:
            ipv6 = snicaddr.address
            if snicaddr.address is None:
                ipv6 = "-"
            if snicaddr.netmask is not None:
                netmask = snicaddr.netmask
        else:
            ipv4 = None
            ipv6 = None

    try:
        gateway = netifaces.gateways()['default'][2][0]
    except:
        gateway = None

    dados = {'ip': ipv4, 'ip6': ipv6, 'netmask': netmask, 'gateway': gateway, 'name':
             list_of_adapters[escolha - 1]}
    return dados


def informacoes_rede(rede):
    surface = pygame.Surface(TAM_TELA)
    surface.fill(CINZA)
    titulo = FONTE_TITLE.render(f"Informações de Rede", True, ESCURO)
    surface.blit(titulo, (40, 20))
    title_info = FONTE_SUBINFO_BOLD.render(f"ADAPTADOR ESCOLHIDO", True, ESCURO)
    info = FONTE_TITLE.render(f"{rede['name']}", True, AZUL)
    ip4 = FONTE_INFO_BOLD.render(f"IPv4 {rede['ip']}", True, ESCURO)
    ip6 = FONTE_INFO_BOLD.render(f"IPv6 {rede['ip6']}", True, ESCURO)
    netmask = FONTE_INFO_BOLD.render(f"Netmask {rede['netmask']}", True, ESCURO)
    gateway = FONTE_INFO_BOLD.render(f"Gateway {rede['gateway']}", True, ESCURO)
    surface.blit(title_info, (200, 80))
    surface.blit(info, (200, 100))
    surface.blit(ip4, (200, 140))
    surface.blit(ip6, (200, 160))
    surface.blit(netmask, (200, 180))
    surface.blit(gateway, (200, 200))
    TELA.blit(surface, (0, 0))
    estatisticas_rede()


def estatisticas_rede():
    total_adapter_antes = psutil.net_io_counters(pernic=True)
    time.sleep(1)
    total_adapter_depois = psutil.net_io_counters(pernic=True)

    adapters = list(total_adapter_depois.keys())
    for adapter in adapters:
        status_antes = total_adapter_antes[adapter]
        status_depois = total_adapter_depois[adapter]
        templ = "%-15s %15s %15s"
        print("======== Status do Adaptador ========")
        print(templ % (adapter, "TOTAL", "POR-SEG"))
        print(templ % (
            "Enviados (KB)",
            round(status_depois.bytes_sent / 1024, 2),
            round((status_depois.bytes_sent - status_antes.bytes_sent) / 1024, 2),
        ))
        print(templ % (
            "Recebidos (KB)",
            round(status_depois.bytes_recv / 1024, 2),
            round((status_depois.bytes_recv - status_antes.bytes_recv) / 1024, 2),
        ))
        print(templ % (
            "Pacotes Env.",
            status_depois.packets_sent,
            status_depois.packets_sent - status_antes.packets_sent,
        ))
        print(templ % (
            "Pacotes Rec.",
            status_depois.packets_recv,
            status_depois.packets_recv - status_antes.packets_recv,
        ))
        print("\n")


def uso_redes_processos():
    surface = pygame.Surface(TAM_TELA)
    surface.fill(CINZA)
    titulo = FONTE_TITLE.render("Uso de rede por processo", True, ESCURO)
    surface.blit(titulo, (30, 20))
    info = FONTE_INFO_BOLD.render(f"Processos listados no terminal. Em ordem (PID)", True, ESCURO)
    surface.blit(info, (40, 120))
    TELA.blit(surface, (0, 0))
    print_processos_rede()


def family_type(family):
    if family == socket.AF_INET:
        return "IPv4"
    elif family == socket.AF_INET6:
        return "IPv6"
    elif family == socket.AF_UNIX:
        return "Unix"
    else:
        return '-'


def get_socket_type(sock):
    if sock == socket.SOCK_STREAM:
        return "TCP"
    elif sock == socket.SOCK_DGRAM:
        return "UDP"
    elif sock == socket.SOCK_RAW:
        return "IP"
    else:
        return "-"


def print_processos_rede():
    for i in psutil.pids():
        p = psutil.Process(i)
        conn = p.connections()
        if len(conn) > 0:
            if conn[0].status.ljust(13) != "ESTABLISHED":
                endl = conn[0].laddr.ip.ljust(11)
                portl = str(conn[0].laddr.port).ljust(5)
                try:
                    endr = conn[0].raddr.ip.ljust(13)
                except:
                    endr = "-"
                try:
                    portr = str(conn[0].raddr.port).ljust(5)
                except:
                    portr = "-"
                print(str(i).ljust(5), "End.  Tipo   Status        Endereço L.   Porta L.     Endereço R.     "
                                       "Porta R.")
                print("     ", family_type(conn[0].family), " " + get_socket_type(conn[0].type),
                      "   " + conn[0].status.ljust(13),
                      endl, "  " + portl, "       " + endr, "  " + portr)


def cliente_servidor(dados_server):
    surface = pygame.Surface(TAM_TELA)
    surface.fill(CINZA)
    titulo = FONTE_TITLE.render(f"Informações do servidor", True, ESCURO)
    surface.blit(titulo, (40, 20))

    # ************************************************************ #
    #                      Processador
    # ************************************************************ #
    titulo = FONTE_SUBINFO_BOLD.render("Processador", True, ESCURO)
    surface.blit(titulo, (40, 80))
    processor_name = f"{dados_server[1]['processor']['name']}"
    sistema_op = f"{dados_server[1]['processor']['system']}"
    processor_cores = f"Clock: {round(dados_server[1]['processor']['clock'],2)} GHz | " \
                      f"{dados_server[1]['processor']['word']} bits | Arch: {dados_server[1]['processor']['arch']}"
    freq_info = f"Frequência: {dados_server[1]['processor']['freq_atual']}Mhz"
    processor_cores_obj = FONTE_INFO.render(processor_cores, True, ESCURO)
    sistema_op_obj = FONTE_INFO.render(sistema_op, True, ESCURO)
    processor_name_obj = FONTE_INFO.render(processor_name, True, ESCURO)
    freq_info_obj = FONTE_INFO.render(freq_info, True, ESCURO)
    surface.blit(processor_name_obj, (40, 90))
    surface.blit(processor_cores_obj, (40, 115))
    surface.blit(sistema_op_obj, (40, 140))
    surface.blit(freq_info_obj, (40, 162))
    qtd_nucleos = f"{dados_server[1]['processor']['threads']} threads | " \
                  f"{dados_server[1]['processor']['cores']} núcleos"
    qtd_nucleos_obj = FONTE_INFO.render(qtd_nucleos, True, ESCURO)
    surface.blit(qtd_nucleos_obj, (425, 100))
    uso_cpu = dados_server[1]['processor']['uso_cpu']
    perc_texto = f"{uso_cpu}"
    titulo = FONTE_PERCENT.render("Uso do Processador", True, ESCURO)
    percentagem_uso = FONTE_PERCENT.render(perc_texto, True, ESCURO)
    surface.blit(titulo, (420, 85))
    surface.blit(percentagem_uso, (460, 130))

    # Desenha barra total (em azul)
    pygame.draw.rect(surface, AZUL, (450, 150, 100, ESPESSURA_BARRA))
    # Barra de uso (em vermelho)
    convert_cpu = float(uso_cpu.replace('%', ''))
    pos_final_barra_uso = 100 * (convert_cpu / 100)
    pygame.draw.rect(surface, VERMELHO, [450, 150, pos_final_barra_uso, ESPESSURA_BARRA])

    # ************************************************************ #
    #                      Memória RAM
    # ************************************************************ #
    titulo_memoria = FONTE_SUBINFO_BOLD.render("Memória", True, ESCURO)
    surface.blit(titulo_memoria, (40, 210))
    memory = dados_server[1]['memory']['porcentagem']
    perc_texto = f"{memory}"

    percentagem_uso = FONTE_PERCENT.render(perc_texto, True, ESCURO)
    surface.blit(percentagem_uso, (40, 230))

    pos_altura_barra = 230
    pos_final_barra = int(LARGURA_TELA - LARGURA_TELA * 0.2)
    # Desenha barra total (em azul)
    pygame.draw.rect(surface, AZUL, (100, pos_altura_barra, pos_final_barra, 20))
    # Barra de uso (em vermelho)
    convert_memory = float(memory.replace('%', ''))
    pos_final_barra_uso = pos_final_barra * (convert_memory / 100)
    pygame.draw.rect(surface, VERMELHO, [100, pos_altura_barra, pos_final_barra_uso, 20])

    memoria_total = f"Memória física total: {dados_server[1]['memory']['total']}"
    memoria_total_obj = FONTE_INFO.render(memoria_total, True, ESCURO)
    surface.blit(memoria_total_obj, (pos_final_barra - 150, pos_altura_barra - 30))

    # Memoria Física total
    memoria_livre = f"Memória em uso: {dados_server[1]['memory']['usada']}"
    memoria_livre_obj = FONTE_INFO.render(memoria_livre, True, ESCURO)
    surface.blit(memoria_livre_obj, (LARGURA_TELA // 5, pos_altura_barra + 20))
    info_server = FONTE_INFO_BOLD.render(f"Conectado ao servidor: ", True, ESCURO)
    server = FONTE_TITLE.render(f"{dados_server[0][0]} : {dados_server[0][1]}", True, AZUL)
    surface.blit(info_server, (40, 320))
    surface.blit(server, (40, 350))
    TELA.blit(surface, (0, 0))


def get_server_infos():
    # Digite as informações para conexão
    host = "52.67.6.168"  # Server instanciado na AWS
    porta = 5001  # Rodando o script do Cliente nessa porta

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, porta))
    except ConnectionRefusedError as error:
        print(error)
    s.send(b"Ok")
    dados = pickle.loads(s.recv(10000))
    s.close()
    informacoes = [(host, porta), dados]
    return informacoes


def controle_setas():
    surface_seta = pygame.Surface(TAM_TELA)
    surface_seta.fill(CINZA)
    image = pygame.image.load(r'resources/seta-direita.png')
    imagered = pygame.transform.smoothscale(image, (70, 70))
    surface_seta.blit(imagered, (340, 10))
    surface_seta.blit(pygame.transform.rotate(imagered, 180), (180, 10))
    TELA.blit(surface_seta, (0, 500))


def colisao_setas(mouse):
    # Posições das setas esquerda e direita
    # Posição no eixo x
    if 510 <= mouse[1] <= 580:
        if 180 <= mouse[0] <= 240:
            return 1
        if 350 <= mouse[0] <= 405:
            return 2


# Verifica o IP público que acessou a página do dyndns.
def ip_publico():
    data = str(urlopen('http://checkip.dyndns.com/').read())
    return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)


# Verifica IP Local
def obter_ip_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


# Variável inicializada vazia (IP_Externo)
ip_net = ""
scheduler = sched.scheduler(time.time, time.sleep)


def main():
    controle = 60
    pagina = 0

    # Variável de controle de impressão no terminal.
    printed = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if colisao_setas(pos) == 1:
                    if pagina > 0:
                        pagina -= 1
                if colisao_setas(pos) == 2:
                    if pagina < 12:
                        pagina += 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if pagina > 0:
                        pagina -= 1
                if event.key == pygame.K_RIGHT:
                    if pagina < 12:
                        pagina += 1
                if event.key == pygame.K_SPACE:
                    pagina = 11

        if controle == 60:
            controle_setas()
            if pagina == 0:
                processador()
            if pagina == 1:
                memoria_ram()
            if pagina == 2:
                disco()
            if pagina == 3:
                rede(ip_publico())
            if pagina == 4:
                resumo()
                printed = False
            if pagina == 5:
                print('\nInício em:		', time.ctime(), '    ', time.process_time())
                time.sleep(2)
                lista = listagem_diretorio(os.environ['HOMEPATH'])[0]
                scheduler.enter(0, 5, arquivos, ("Arquivos", lista))
                if not printed:
                    scheduler.enter(1, 1, print_arquivos_terminal, kwargs={'lista': lista})
                    printed = True
                print('\nFim em:         ', time.ctime(), '    ', time.process_time())
            if pagina == 6:
                lista = listagem_diretorio(os.environ['HOMEPATH'])[1]
                scheduler.enter(0, 5, arquivos, ("Pastas", lista))
                if printed:
                    scheduler.enter(0, 1, print_arquivos_terminal, kwargs={'lista': lista})
                    printed = False
            if pagina == 7:
                if not printed:
                    scheduler.enter(0, 5, print_processos_terminal, kwargs={'l_process': processos()})
                    printed = True
            if pagina == 8:
                if printed:
                    scheduler.enter(0, 5, print_network_nmap, kwargs={'network': ips_nmap()})
                    printed = False
            if pagina == 9:
                if not printed:
                    scheduler.enter(0, 5, informacoes_rede, kwargs={'rede': infor_adapters()})
                    printed = True
            if pagina == 10:
                if printed:
                    scheduler.enter(0, 5, uso_redes_processos)
                    printed = False
            if pagina == 11:
                if not printed:
                    scheduler.enter(0, 5, cliente_servidor, kwargs={'dados_server': get_server_infos()})
                    printed = True
            controle = 0
            scheduler.run()
        pygame.display.update()
        controle += 1
        CLOCK.tick(HZ)


if __name__ == '__main__':
    main()
