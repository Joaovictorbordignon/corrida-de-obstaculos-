import os
import json
import time
import tkinter as tk
import random
import pygame
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados
from recursos.funcoes import escreverDados

pygame.init()
inicializarBancoDeDados()
LARGURA, ALTURA = (1000,700)
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Corrida de obstáculos")

# Caminhos de imagem
CAMINHO_IMAGENS = os.path.join("imagens")
img_fundo = pygame.image.load(os.path.join(CAMINHO_IMAGENS, "fundo.png"))
img_macaco = pygame.image.load(os.path.join(CAMINHO_IMAGENS, "macaco.png"))
img_obstaculo = pygame.image.load(os.path.join(CAMINHO_IMAGENS, "obstaculo.png"))
img_banana = pygame.image.load(os.path.join(CAMINHO_IMAGENS, "banana.png"))

img_fundo = pygame.transform.scale(img_fundo, (LARGURA, ALTURA))
img_macaco = pygame.transform.scale(img_macaco, (50, 50))
img_obstaculo = pygame.transform.scale(img_obstaculo, (100, 100))
img_banana = pygame.transform.scale(img_banana, (30, 30))

# Variáveis do personagem
x_macaco = 100
y_macaco = ALTURA - 100
velocidade_y = 0
pulando = False
gravity = 1

# Obstáculos e bananas
obstaculos = []
bananas = []
tempo_obstaculo = 0
tempo_banana = 0
velocidade_objetos = 7

# Pontuação
pontos = 0
bananas_coletadas = 0
fonte = pygame.font.SysFont("Arial", 28)

relogio = pygame.time.Clock()
jogando = True

def desenhar_tela():
    tela.blit(img_fundo, (0, 0))
    tela.blit(img_macaco, (x_macaco, y_macaco))
    for obst in obstaculos:
        tela.blit(pygame.transform.scale(img_obstaculo, (obst.width, obst.height)), (obst.x, obst.y))
    for banana in bananas:
        tela.blit(img_banana, (banana.x, banana.y))
    texto_pontos = fonte.render(f"Pontos: {pontos}", True, (0, 0, 0))
    texto_bananas = fonte.render(f"Bananas: {bananas_coletadas}", True, (0, 0, 0))
    tela.blit(texto_pontos, (10, 10))
    tela.blit(texto_bananas, (10, 40))
    pygame.display.update()

# Loop principal
while jogando:
    relogio.tick(60)
    tempo_obstaculo += 1
    tempo_banana += 1
    pontos += 1

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogando = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_SPACE] and not pulando:
        velocidade_y = -15
        pulando = True

    velocidade_y += gravity
    y_macaco += velocidade_y

    # Criação de obstáculos (plataformas)
    if tempo_obstaculo > 90:
        tempo_obstaculo = 0
        altura_random = random.choice([40, 60, 80, 100])
        largura_random = random.choice([80, 100, 120, 140])
        y_obstaculo = ALTURA - 50 - altura_random
        obstaculos.append(pygame.Rect(LARGURA, y_obstaculo, largura_random, altura_random))

    # Criação de bananas
    if tempo_banana > 120:
        tempo_banana = 0
        y_banana = random.randint(ALTURA - 200, ALTURA - 130)
        bananas.append(pygame.Rect(LARGURA, y_banana, 30, 30))

    # Atualização dos obstáculos e colisão
    personagem = pygame.Rect(x_macaco, y_macaco, 50, 50)
    no_chao = True

    for obst in list(obstaculos):
        obst.x -= velocidade_objetos
        if obst.right < 0:
            obstaculos.remove(obst)

        if personagem.colliderect(obst):
            if velocidade_y >= 0 and personagem.bottom <= obst.top + 10:
                y_macaco = obst.top - 50
                velocidade_y = 0
                pulando = False
                no_chao = False
            else:
                jogando = False

    if no_chao and y_macaco >= ALTURA - 100:
        pulando = False
        y_macaco = ALTURA - 100

    # Atualização das bananas
    for banana in list(bananas):
        banana.x -= velocidade_objetos
        if banana.right < 0:
            bananas.remove(banana)
        if personagem.colliderect(banana):
            bananas.remove(banana)
            bananas_coletadas += 1
            pontos += 100

    desenhar_tela()

pygame.quit()
print(f"Fim de jogo! Pontos: {pontos} | Bananas: {bananas_coletadas}")
