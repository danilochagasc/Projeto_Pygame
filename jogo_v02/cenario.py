#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Curso: PyGame
# Prof. Douglas Machado Tavares
# Ministrado em 2020

import pygame
import os


class Cenario:
    """ Define um Cenario """

    def __init__(self, tela):
        """ __init__() -> instancia de cenario """
        self.tela = tela
        self.__pos_x = 0
        self.__pos_y = 0
        self.__carregar_objetos()
        self.__carregar_mapa()
        num_pixel_x = (len(self.mapa[0]) - 1) * 100
        num_pixel_y = len(self.mapa) * 100
        self.camada = pygame.surface.Surface((num_pixel_x, num_pixel_y))
        self.obstaculos = []
        self.obstaculos_simbolos = []


    def __carregar_objetos(self):
        """ Carrega os objetos ('Tileset') """
        caminho = "dados/imagens/objetos/"
        lista_nomes = os.listdir(caminho)
        self.objetos = {}
        for nome in lista_nomes:
            if nome.endswith(".png"):
                simbolo = nome[-5]
                colisao = nome[-7]
                objeto = pygame.image.load(caminho + nome)
                self.objetos[simbolo] = (objeto, colisao)


    def __carregar_mapa(self):
        """ Carrega o mapa """
        arq_mapa = open("dados/mapas/fabrica.mp", "r")
        self.mapa = arq_mapa.readlines()
        arq_mapa.close()


    def construir(self):
        """ Constroi o cenario """
        y = 0
        for linha in self.mapa:
            x = 0
            for simbolo in linha:
                if simbolo in self.objetos:
                    objeto, colidivel = self.objetos[simbolo]
                    self.camada.blit(objeto, (x, y))
                    if colidivel == 'c':
                        rtg = objeto.get_bounding_rect()
                        rtg.x += x
                        rtg.y += y
                        self.obstaculos.append(rtg)
                        self.obstaculos_simbolos.append(simbolo)
                x = x + 100
            y = y + 100
        self.__camada_original = self.camada.copy()


    def limpar(self):
        """ Volta a superfice 'camada' ao estado original """
        self.camada = self.__camada_original.copy()


    def update(self):
        """ Repinta o cenario """
        self.tela.blit(self.camada, (self.__pos_x, self.__pos_y))


    def mover(self, dx, dy):
        """ Move o cenario """
        if dx > 0:
            if self.__pos_x <= 0:
                self.__pos_x += dx
        else:
            lim = self.camada.get_width() - self.tela.get_width()
            if self.__pos_x >= -lim:
                self.__pos_x += dx
        if dy > 0:
            if self.__pos_y <= 0:
                self.__pos_y += dy
        else:
            lim = self.camada.get_height() - self.tela.get_height()
            if self.__pos_y >= -lim:
                self.__pos_y += dy
