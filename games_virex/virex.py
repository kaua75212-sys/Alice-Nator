#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Alice-inator (versão de boa)
Jogo simples inspirado no Akinator
"""

import pygame
import sys
import random
from pathlib import Path

print("Iniciando Alice-inator...")

pygame.init()

# Tamanho da janela
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Alice-inator")
relogio = pygame.time.Clock()

# Cores
FUNDO = (20, 18, 30)
ROXO = (140, 100, 220)
ROXO_CLARO = (190, 160, 255)
ROSA = (255, 140, 180)
VERDE = (90, 200, 130)
VERMELHO = (220, 90, 110)
CINZA = (120, 120, 140)
BRANCO = (255, 255, 255)
PRETO = (30, 25, 40)

# Fontes
fonte_grande = pygame.font.SysFont("arial", 36, bold=True)
fonte_media = pygame.font.SysFont("arial", 24)
fonte_pequena = pygame.font.SysFont("arial", 18)

# Pasta do jogo
PASTA = Path(__file__).parent

def carregar(nome, altura=260):
    caminho = PASTA / nome
    if caminho.exists():
        img = pygame.image.load(str(caminho)).convert_alpha()
        w, h = img.get_size()
        return pygame.transform.smoothscale(img, (int(w * altura / h), altura))
    # Se não achar a imagem, cria um quadrado roxo
    s = pygame.Surface((160, 260))
    s.fill((100, 60, 150))
    return s

alice_normal = carregar("alice_trans.png")
alice_falando = carregar("alice_talk_trans.png")

# ---------- Dados do jogo ----------
personagens = [
    {"nome": "Goku", "anime": True, "masculino": True, "poderes": True, "vilao": False},
    {"nome": "Naruto", "anime": True, "masculino": True, "poderes": True, "vilao": False},
    {"nome": "Luffy", "anime": True, "masculino": True, "poderes": True, "vilao": False},
    {"nome": "Sailor Moon", "anime": True, "masculino": False, "poderes": True, "vilao": False},
    {"nome": "Pikachu", "anime": True, "masculino": True, "poderes": True, "vilao": False},
    {"nome": "Itachi", "anime": True, "masculino": True, "poderes": True, "vilao": True},
    {"nome": "Batman", "anime": False, "masculino": True, "poderes": False, "vilao": False},
    {"nome": "Homem-Aranha", "anime": False, "masculino": True, "poderes": True, "vilao": False},
    {"nome": "Darth Vader", "anime": False, "masculino": True, "poderes": True, "vilao": True},
    {"nome": "Elsa", "anime": False, "masculino": False, "poderes": True, "vilao": False},
    {"nome": "Mario", "anime": False, "masculino": True, "poderes": False, "vilao": False},
    {"nome": "Thanos", "anime": False, "masculino": True, "poderes": True, "vilao": True},
]

perguntas = [
    {"texto": "É de anime / mangá?", "chave": "anime"},
    {"texto": "É menino / homem?", "chave": "masculino"},
    {"texto": "Tem poderes especiais?", "chave": "poderes"},
    {"texto": "É um vilão?", "chave": "vilao"},
]

# ---------- Estado ----------
estado = "menu"          # menu, pergunta, palpite, fim
indice = 0
lista = []
palpite = None
texto = ""
subtexto = ""
falando = False
timer = 0

# ---------- Funções ----------
def comecar():
    global estado, indice, lista, texto, subtexto, falando, timer
    lista = personagens.copy()
    indice = 0
    estado = "pergunta"
    falando = True
    timer = 40
    fazer_pergunta()

def fazer_pergunta():
    global texto, subtexto, estado
    if indice < len(perguntas) and len(lista) > 1:
        estado = "pergunta"
        q = perguntas[indice]
        texto = q["texto"]
        subtexto = f"Restam {len(lista)} possibilidades"
    else:
        adivinhar()

def responder(sim):
    global indice, lista, falando, timer, estado, texto, subtexto
    if estado != "pergunta":
        return
    chave = perguntas[indice]["chave"]
    lista = [p for p in lista if p[chave] == sim]
    indice += 1
    estado = "pensando"
    falando = True
    timer = 30
    texto = "Hmm..."
    subtexto = "Deixa eu pensar"

def adivinhar():
    global estado, palpite, texto, subtexto, falando, timer
    estado = "palpite"
    falando = True
    timer = 50
    if lista:
        palpite = random.choice(lista)
        texto = "Acho que é..."
        subtexto = palpite["nome"]
    else:
        palpite = None
        texto = "Não consegui adivinhar"
        subtexto = "Você pensou em alguém difícil!"

def resultado(acertou):
    global estado, texto, subtexto, falando, timer
    estado = "fim"
    falando = True
    timer = 60
    if acertou:
        texto = "Acertei!"
        subtexto = f"Era o(a) {palpite['nome']}!"
    else:
        texto = "Errei..."
        subtexto = "Quem era então?"

# ---------- Desenho ----------
def desenhar_botao(x, y, w, h, texto_btn, cor, mouse):
    rect = pygame.Rect(x, y, w, h)
    hover = rect.collidepoint(mouse)
    cor_final = tuple(min(255, c + 30) for c in cor) if hover else cor
    pygame.draw.rect(tela, cor_final, rect, border_radius=12)
    pygame.draw.rect(tela, ROXO_CLARO, rect, 2, border_radius=12)
    t = fonte_media.render(texto_btn, True, BRANCO)
    tela.blit(t, t.get_rect(center=rect.center))
    return rect

def desenhar():
    tela.fill(FUNDO)

    # Alice
    img = alice_falando if falando else alice_normal
    tela.blit(img, (40, 100))

    # Balão de fala
    if estado != "menu":
        pygame.draw.rect(tela, (250, 245, 255), (340, 60, 420, 160), border_radius=16)
        pygame.draw.rect(tela, ROXO_CLARO, (340, 60, 420, 160), 3, border_radius=16)

        t1 = fonte_media.render(texto, True, PRETO)
        tela.blit(t1, (360, 90))
        t2 = fonte_pequena.render(subtexto, True, ROXO)
        tela.blit(t2, (360, 140))

    mouse = pygame.mouse.get_pos()

    if estado == "menu":
        titulo = fonte_grande.render("Alice-inator", True, ROXO_CLARO)
        tela.blit(titulo, (380, 80))
        sub = fonte_media.render("Pense em um personagem!", True, ROSA)
        tela.blit(sub, (380, 140))

        dica1 = fonte_pequena.render("Pode ser de anime, filme, jogo...", True, CINZA)
        tela.blit(dica1, (380, 200))
        dica2 = fonte_pequena.render("A Alice vai tentar adivinhar.", True, CINZA)
        tela.blit(dica2, (380, 230))

        return desenhar_botao(400, 320, 220, 50, "Começar", ROXO, mouse)

    elif estado == "pergunta":
        r1 = desenhar_botao(360, 280, 120, 45, "Sim", VERDE, mouse)
        r2 = desenhar_botao(510, 280, 120, 45, "Não", VERMELHO, mouse)
        return r1, r2

    elif estado == "pensando":
        pontos = "." * ((pygame.time.get_ticks() // 400) % 4)
        t = fonte_media.render("Pensando" + pontos, True, ROXO)
        tela.blit(t, (400, 280))
        return None

    elif estado == "palpite":
        if palpite:
            r1 = desenhar_botao(360, 280, 120, 45, "Sim!", VERDE, mouse)
            r2 = desenhar_botao(510, 280, 120, 45, "Não", VERMELHO, mouse)
            return r1, r2
        else:
            return desenhar_botao(400, 280, 200, 45, "De novo", ROXO, mouse)

    elif estado == "fim":
        return desenhar_botao(400, 280, 200, 45, "Jogar de novo", ROXO, mouse)

    return None

# ---------- Loop principal ----------
print("Tudo pronto! Abrindo a janela...")
rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            rodando = False

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos = evento.pos

            if estado == "menu":
                botao = desenhar()
                if botao and botao.collidepoint(pos):
                    comecar()

            elif estado == "pergunta":
                r1, r2 = desenhar()
                if r1 and r1.collidepoint(pos):
                    responder(True)
                elif r2 and r2.collidepoint(pos):
                    responder(False)

            elif estado == "palpite":
                if palpite:
                    r1, r2 = desenhar()
                    if r1 and r1.collidepoint(pos):
                        resultado(True)
                    elif r2 and r2.collidepoint(pos):
                        resultado(False)
                else:
                    botao = desenhar()
                    if botao and botao.collidepoint(pos):
                        comecar()

            elif estado == "fim":
                botao = desenhar()
                if botao and botao.collidepoint(pos):
                    comecar()

    # Timer da animação de falar
    if timer > 0:
        timer -= 1
        falando = True
    else:
        falando = False
        if estado == "pensando":
            fazer_pergunta()

    desenhar()
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
print("Jogo fechado. Até mais!")
sys.exit()