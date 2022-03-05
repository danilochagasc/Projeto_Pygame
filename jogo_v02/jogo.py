#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Curso: PyGame
# Prof. Douglas Machado Tavares
# Ministrado em 2020


import pygame
import random as rd
from ator import Ator
from cenario import Cenario
from pygame.constants import *


class Jogo:
    """ Define um Jogo """

    def __init__(self):
        """ __init__() -> instancia de jogo """
        pygame.init()
        self.fim_jogo = False
        self.tela = pygame.display.set_mode((1000, 600))
        self.cenario = Cenario(self.tela)
        self.cenario.camada.fill((70, 70, 140))
        self.cenario.construir()
        self.__configurar_sons()
        self.num_colisoes = 0


    def __configurar_sons(self):
        """ Realiza as configuraçoes dos sons """
        self.som_pulo = pygame.mixer.Sound("dados/sons/pulo.ogg")
        self.som_pulo.set_volume(0.30)
        self.som_trilha = pygame.mixer.Sound("dados/sons/trilha.ogg")
        self.som_trilha.set_volume(0.07)
        self.som_falha = pygame.mixer.Sound("dados/sons/falha.ogg")
        self.som_falha.set_volume(0.30)
        self.som_deslisando = pygame.mixer.Sound("dados/sons/deslizando.ogg")
        self.som_deslisando.set_volume(0.10)
        self.som_comemoracao = pygame.mixer.Sound("dados/sons/comemoracao.ogg")
        self.som_comemoracao.set_volume(0.08)


    def __criar_estado(self, estado, num_poses):
        """ Cria um estado preenche as poses """
        nome_arq = "dados/imagens/robo/robo_{}_{:02d}.png"
        self.robo.inserir_estado(estado)
        for i in range(1, num_poses+1):
            self.robo.inserir_pose(estado, nome_arq.format(estado, i))


    def criar_atores(self):
        """ Cria os atores do jogo """
        self.robo = Ator(350, 500-178)
        self.robo.mochila["k"] = 1
        self.robo.mochila["k_max"] = 1
        self.robo.mochila["dx"] = 22
        self.robo.mochila["dy"] = 20
        self.__criar_estado("deslizando", 10)
        self.__criar_estado("saltando", 12)
        self.__criar_estado("recuperando", 9)
        self.__criar_estado("esperando", 10)
        self.__criar_estado("comemorando", 10)
        self.__criar_estado("correndo", 8)
        self.grupo_atores = pygame.sprite.RenderPlain((self.robo))
        self.robo.alterar_estado("esperando")


    def atualizar_atores(self):
        """ Atualiza os atores """
        if self.robo.esta("correndo"):
            self.__rb_correr()
        elif self.robo.esta("saltando"):
            self.__rb_saltar()
        elif self.robo.esta("deslizando"):
            self.__rb_deslizar()
        elif self.robo.esta("recuperando"):
            self.__rb_recuperar()
        rtg = self.robo.image.get_bounding_rect()
        rtg.x += self.robo.rect.x
        rtg.y += self.robo.rect.y
        i_colisao = rtg.collidelist(self.cenario.obstaculos)
        if i_colisao != -1:
            simbolo = self.cenario.obstaculos_simbolos[i_colisao]
            if simbolo == "F":
                self.__rb_comemorar()
            else:
                self.robo.mochila["k"] = 1
                self.robo.alterar_estado("recuperando")
                self.num_colisoes += 1


    def __rb_comemorar(self):
        """ Faz o robô comemorar """
        self.robo.alterar_estado("comemorando")
        self.som_trilha.stop()
        self.som_comemoracao.play()
        self.robo.rect.x += 160
        self.robo.rect.y = 500 - self.robo.rect.h
        self.cenario.mover(-160, 0)


    def __rb_correr(self):
        """ Faz o robô correr """
        dx = self.robo.mochila["dx"]
        self.cenario.mover(-dx, 0)
        self.robo.rect.x += dx


    def __rb_saltar(self):
        """ Faz o robô saltar """
        dx = self.robo.mochila["dx"]
        dy = self.robo.mochila["dy"]
        if self.robo.mochila["k"] <= 5:
            self.robo.rect.y -= dy
            self.robo.mochila["k"] += 1
        elif self.robo.mochila["k"] <= 5 + 4:
            self.robo.mochila["k"] += 1
        elif self.robo.mochila["k"] <= 5 + 4 + 5:
            self.robo.rect.y += dy
            self.robo.mochila["k"] += 1
        else:
            self.som_pulo.play()
            self.robo.alterar_estado("correndo")
            self.robo.mochila["k"] = 1
            self.robo.rect.y = 500 - self.robo.rect.h
        self.cenario.mover(-dx, 0)
        self.robo.rect.x += dx


    def __rb_deslizar(self):
        """ Faz o robô deslizar """
        dx = self.robo.mochila["dx"]
        if self.robo.mochila["k"] == 1:
            self.som_deslisando.play()
            self.robo.mochila["k"] += 1
            self.robo.mochila["k_max"] = 12
        elif self.robo.mochila["k"] <= self.robo.mochila["k_max"]:
            self.robo.mochila["k"] += 1
        else:
            self.robo.alterar_estado("correndo")
            self.robo.mochila["k"] = 1
            self.robo.rect.y = 500 - self.robo.rect.h
        self.cenario.mover(-dx, 0)
        self.robo.rect.x += dx


    def __rb_recuperar(self):
        """ Faz o robô recuperar energia """
        if self.robo.mochila["k"] == 1:
            self.som_falha.play()
            self.robo.rect.x += 200
            self.robo.rect.y = 500 - self.robo.rect.h
            self.cenario.mover(-200, 0)
            self.robo.mochila["k_max"] = rd.randint(20, 60)
            self.robo.mochila["k"] += 1
        elif self.robo.mochila["k"] <= self.robo.mochila["k_max"]:
            self.robo.mochila["k"] += 1
        else:
            self.robo.alterar_estado("correndo")
            self.robo.mochila["k"] = 1


    def repintar_tela(self):
        """ Repinta a tela """
        self.cenario.limpar()
        self.grupo_atores.update()
        self.grupo_atores.draw(self.cenario.camada)
        self.cenario.update()
        pygame.display.update()


    def tratar_eventos_teclado(self, evento):
        """ Observa e trata os eventos """
        tecla = evento.key
        if tecla == K_ESCAPE or tecla == K_q:
            self.salvar()
        if self.robo.esta("esperando"):
            self.robo.alterar_estado("correndo")
        elif self.robo.esta("correndo"):
            if tecla == K_UP:
                self.robo.alterar_estado("saltando")
            elif tecla == K_DOWN:
                self.robo.alterar_estado("deslizando")


    def tratar_eventos(self):
        """ Observa e trata os eventos """
        for evento in pygame.event.get():
            if evento.type == QUIT:
                self.salvar()
            elif evento.type == KEYDOWN or evento.type == KEYUP:
                self.tratar_eventos_teclado(evento)


    def rodar(self):
        """ Roda o jogo """
        self.criar_atores()
        FPS = 15  # ==>  experimente valores entre 10 a 18
        self.som_trilha.play()
        relogio = pygame.time.Clock()
        while not self.fim_jogo:
            self.tratar_eventos()
            self.atualizar_atores()
            self.repintar_tela()
            relogio.tick(FPS)


    def finalizar(self):
        """ Finaliza o jogo """
        self.som_comemoracao.stop()
        pygame.display.quit()
        raise SystemExit


    def salvar(self):
        """ Tarefas antes de finalizar """
        self.fim_jogo = True
        self.finalizar()


if __name__ == "__main__":
    jg = Jogo()
    jg.rodar()
