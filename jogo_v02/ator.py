#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Curso: PyGame
# Prof. Douglas Machado Tavares
# Ministrado em 2020

import pygame


class Ator(pygame.sprite.Sprite):
    """ Define um Ator """

    def __init__(self, pos_x=0, pos_y=0):
        """ __init__() -> instancia de ator """
        pygame.sprite.Sprite.__init__(self)
        self.poses = {}
        self.__p = 0    # p eh um ponteiro para pose atual.
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__congelado = False
        self.alterar_estado("")
        self.mochila = {}


    def inserir_estado(self, novo_estado):
        """ Insere um novo estado """
        self.poses[novo_estado] = []
        self.alterar_estado(novo_estado)


    def retornar_estado(self):
        """ Retorna o estado atual """
        return self.__estado_atual


    def alterar_estado(self, novo_estado, k=0):
        """ Altera o estado atual """
        self.__estado_atual = novo_estado
        self.__p = k


    def esta(self, estado):
        """ Verifica se o estado atual eh igual 'estado' """
        return self.retornar_estado() == estado


    def inserir_pose(self, estado, nome_arq_img):
        """ Armazena uma 'surface' dentro da lista poses """
        self.image = pygame.image.load(nome_arq_img)
        self.rect = self.image.get_rect()
        self.rect.x = self.__pos_x
        self.rect.y = self.__pos_y
        self.poses[estado].append(self.image)


    def congelar(self, k=0):
        """ Congela a troca de poses

            Congela na pose de indice 'k'.
        """
        self.__congelado = True
        self.__p = k
        estado_atual = self.retornar_estado()
        self.image = self.poses[estado_atual][self.__p]


    def descongelar(self):
        """ Descongela a troca de poses """
        self.__congelado = False


    def esta_congelado(self):
        """ Verifica se o ator esta congelado """
        return self.__congelado


    def update(self):
        """ Reimplementa o metodo update() da classe mae (classe Sprite) """
        if not self.__congelado:
            estado_atual = self.retornar_estado()
            self.__p  = (self.__p + 1) % len(self.poses[estado_atual])
            self.image = self.poses[estado_atual][self.__p]
