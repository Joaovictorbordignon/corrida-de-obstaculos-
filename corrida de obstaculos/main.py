import os
import random
import pygame
import tkinter as tk
from tkinter import messagebox
from recursos.basico import inicializarBancoDeDados
from recursos.basico import escreverDados

pygame.init()
inicializarBancoDeDados()

# Dimensões da janela
largura, altura = (1000, 700)
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Corrida de obstáculos")

# Caminhos de imagem
CAMINHO_IMAGENS = os.path.join("assets/imagens")
img_fundo = pygame.image.load("assets/fundo.png")
img_personagem = pygame.image.load("assets/personagem.png")
img_obstaculo = pygame.image.load("assets/obstaculo.png")
img_item = pygame.image.load("assets/item.png")

# Redimensionamento das imagens
img_fundo = pygame.transform.scale(img_fundo, (largura, altura))
img_personagem = pygame.transform.scale(img_personagem, (50, 50))
img_obstaculo = pygame.transform.scale(img_obstaculo, (140, 100))
img_item = pygame.transform.scale(img_item, (30, 30))

# Variáveis do personagem
x_personagem = 100
y_personagem = altura - 100
velocidade_y = 0
pulando = False
gravidade = 1

# Obstáculos e itens
obstaculos = []
item = []
tempo_obstaculo = 0
tempo_item = 0
velocidade_objetos = 7

# Pontuação
pontos = 0
itens_coletados = 0
fonte = pygame.font.SysFont("Arial", 28)

# Botão de pause
pausado = False
botao_pausar = pygame.Rect(largura - 120, 10, 100, 40)

# Relógio e estado do jogo
relogio = pygame.time.Clock()
jogando = True

# Função para desenhar a tela
def desenhar_tela():
    tela.blit(img_fundo, (0, 0))
    tela.blit(img_personagem, (x_personagem, y_personagem))
    def obter_nome():
        global nome
        nome = entry_nome.get()
        if not nome:
            messagebox.showwarning("Aviso", "Digite seu nome:")
        else:
            print(f"nome digitado:{nome}")
            janela.destroy()
    for obst in obstaculos:
        tela.blit(pygame.transform.scale(img_obstaculo, (obst.width, obst.height)), (obst.x, obst.y))
    for lata in item:
        tela.blit(img_item, (lata.x, lata.y))
    janela = tk.Tk()
    janela.title("Informe seu nome")
    janela.protocol("WM_DELETE_WINDOW", obter_nome)
    tk.Label(janela, text="informe seu nome!").pack()
    

    entry_nome = tk.Entry(janela)
    entry_nome.pack()

    botao = tk.Button(janela, text="Enviar", command=obter_nome)
    botao.pack()
    janela.destroy ()
    

    # Texto de pontuação
    texto_pontos = fonte.render(f"Pontos: {pontos}", True, (0, 0, 0))
    texto_latas = fonte.render(f"Latas: {itens_coletados}", True, (0, 0, 0))
    tela.blit(texto_pontos, (10, 10))
    tela.blit(texto_latas, (10, 40))

    # Botão de pause
    pygame.draw.rect(tela, (200, 200, 200), botao_pausar)
    texto_pause = fonte.render("Pausar" if not pausado else "Retomar", True, (0, 0, 0))
    tela.blit(texto_pause, (botao_pausar.x + 5, botao_pausar.y + 5))

    pygame.display.update()
    

# Loop principal
while jogando:
    relogio.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogando = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if botao_pausar.collidepoint(evento.pos):
                pausado = not pausado

    if pausado:
        desenhar_tela()
        continue

    # Atualizações de tempo e pontuação
    tempo_obstaculo += 1
    tempo_item += 1
    pontos += 1

    # Entrada do jogador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_SPACE] and not pulando:
        velocidade_y = -15
        pulando = True

    velocidade_y += gravidade
    y_personagem += velocidade_y

    # Criação de obstáculos
    if tempo_obstaculo > 90:
        tempo_obstaculo = 0
        altura_random = random.choice([40, 60, 80, 100])
        largura_random = random.choice([80, 100, 120, 140])
        y_obstaculo = altura - 50 - altura_random
        obstaculos.append(pygame.Rect(largura, y_obstaculo, largura_random, altura_random))

    # Criação de itens
    if tempo_item > 120:
        tempo_item = 0
        y_lata = random.randint(altura - 200, altura - 130)
        item.append(pygame.Rect(largura, y_lata, 30, 30))

    # Colisões com obstáculos
    personagem = pygame.Rect(x_personagem, y_personagem, 50, 50)
    no_chao = True
    for obst in list(obstaculos):
        obst.x -= velocidade_objetos
        if obst.right < 0:
            obstaculos.remove(obst)

        if personagem.colliderect(obst):
            if velocidade_y >= 0 and personagem.bottom <= obst.top + 10:
                y_personagem = obst.top - 50
                velocidade_y = 0
                pulando = False
                no_chao = False
            else:
                jogando = False

    # Verifica se o personagem está no chão
    if no_chao and y_personagem >= altura - 100:
        pulando = False
        y_personagem = altura - 100

    # Atualiza e verifica colisões com itens
    for lata in list(item):
        lata.x -= velocidade_objetos
        if lata.right < 0:
            item.remove(lata)
        if personagem.colliderect(lata):
            item.remove(lata)
            itens_coletados += 1
            pontos += 100

    desenhar_tela()

pygame.quit()
print(f"Fim de jogo! Pontos: {pontos} | Latas: {itens_coletados}")
