#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
IV – Développement d’un casse-brique
Le casse-brique a eu diverses implémentations marquantes dans l’histoire des jeux vidéo. Un certain
S.J., amateur de pommes, en a conçu un quand il travaillait chez Atari. Le titre Arkanoid sur Amstrad
en fut un superbe exemple.
Le principe est de détruire, au moyen d'une ou plusieurs balles, un ensemble de briques se trouvant
dans un niveau pour accéder au niveau suivant. (Voir https://fr.wikipedia.org/wiki/Casse-briques )
La conception et l’implémentation d’un casse-brique demandent l’utilisation de plusieurs concepts.
Parmi ceux-ci on note la gestion de tableaux en 2 dimensions ou la programmation orientée objet.
"""

# pylint: disable=no-member
# pylint : disable=unused-wildcard-import
# pylint: disable=W0614

import pygame
from pygame.locals import *
from random import randint
import pygame_gui

largeur = 800
hauteur = 600

taille_case = 20

WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0,0,0)
RED = pygame.Color(255,0,0)
YELLOW = pygame.Color(255,255,0)
LIGHT_YELLOW = pygame.Color(255,255,128)
GREEN = pygame.Color(0,255,0)
LIGHT_GREEN1 = pygame.Color(43,255,43) 
LIGHT_GREEN2 = pygame.Color(86,255,86)
LIGHT_GREEN3 = pygame.Color(128,255,128)
LIGHT_GREEN4 = pygame.Color(211,255,211)
LIGHT_BLUE = pygame.Color(128,128,255)
BLUE = pygame.Color(0,0,255)
GRAY = pygame.Color(128,128,128)
LIGHT_GRAY = pygame.Color(192,192,192)
DARK_GRAY = pygame.Color(96,96,96)


class Interface :
    def __init__(self, ecran, largeur, hauteur):
        self.ecran = ecran
        self.largeur = largeur                  # en pixels
        self.hauteur = hauteur

    def determine_position_arrondie_ecran(self, pos) :
        x = 10 * int(pos[0]/10)
        y = 10 * int(pos[1]/10)
        return x,y    

    def determine_position_grille(self, pos) :
        (x,y) = self.determine_position_arrondie_ecran(pos)
        x = int( x / self.taille_case )
        y = int( y / self.taille_case )
        return (x,y)

    def dessine_case(self, pos, couleur) :
        x,y = pos
        carre = pygame.Rect(x*self.taille_case , y*self.taille_case, self.taille_case-2, self.taille_case-2)
        pygame.draw.rect(self.ecran, couleur, carre)
        return self.ecran

    def dessine_grille(self) :
        
        rectScreen = self.ecran.get_rect()
        police = pygame.font.Font("theboldfont.ttf",12)    
        for i in range(len(self.tableau)) : 
            for j in range(len(self.tableau[i])) :
                if self.tableau[i][j][0] == 0 :                                  # case couverte
                    self.ecran = self.dessine_case((i,j), DARK_GRAY)
                elif self.tableau[i][j][0] == 1 :                                # case découverte
                    if self.tableau[i][j][2] != 0 :
                        if self.tableau[i][j][2] == 1:
                            self.ecran = self.dessine_case((i,j), LIGHT_GREEN4) 
                        elif self.tableau[i][j][2] == 2:
                            self.ecran = self.dessine_case((i,j), LIGHT_GREEN3) 
                        elif self.tableau[i][j][2] == 3:
                            self.ecran = self.dessine_case((i,j), LIGHT_GREEN2)                     
                        elif self.tableau[i][j][2] == 4:
                            self.ecran = self.dessine_case((i,j), LIGHT_GREEN1)                     
                        elif self.tableau[i][j][2] == 5:
                            self.ecran = self.dessine_case((i,j), GREEN)                     
                        else :
                            self.ecran = self.dessine_case((i,j), BLUE)                     
                        texte = police.render(str(self.tableau[i][j][2]),False,pygame.Color("#000000"))
                        rectTexte = texte.get_rect()
                        rectTexte = rectScreen.move(i*self.taille_case
                                                +int(self.taille_case/2),j*self.taille_case+4) 
                        self.ecran.blit(texte,rectTexte)
                    else :
                        self.ecran = self.dessine_case((i,j), LIGHT_GRAY) 
                elif self.tableau[i][j][0] == 2 :
                    self.ecran = self.dessine_case((i,j), RED) # case avec un drapeau
                elif self.tableau[i][j][0] == 3 :
                    self.ecran = self.dessine_case((i,j), BLACK) # case découverte avec une mine
        pygame.display.update()        
        return self.ecran         

class Casse_briques :
    def __init__(self, ecran, largeur, hauteur) :
        self.ecran = ecran
        self.largeur = largeur
        self.hauteur = hauteur
        self.interface = Interface(self.ecran, largeur, hauteur)
        self.score = 0



def main() :

    pygame.init()
    pygame.display.set_caption('Casse-briques')
    logo = pygame.image.load("monlogo.ico")
    pygame.display.set_icon(logo)
    ecran = pygame.display.set_mode((largeur+200,hauteur))
    manager = pygame_gui.UIManager((largeur+200,hauteur))
    jeu = Casse_briques(ecran,largeur, hauteur)
    clock = pygame.time.Clock()  

    #Placement des boutons avec pygame_gui
    RAZ_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((largeur, 0), (98, 49)),
                                                text='RAZ',
                                                manager=manager)
    texte_score = pygame_gui.elements.UITextBox(html_text="Score : "+str(jeu.score)+" pts",
                                                relative_rect=pygame.Rect((largeur, 50), (198, 98)),
                                                manager=manager)
    pygame.display.update() 
#boucle pincipale 
    x = 400
    y = 400
    perdu = False
    gagne = False
    execution = True
    ecran.fill((128,255,128))
    monimage = pygame.image.load("balle.jpg")
    ecran.blit(monimage, (x,y))
    pygame.display.flip()
    #On crée une zone graphique rectangulaire ayant une certaine longueur et hauteur et on mémorise dans un objet graphique
    fond=pygame.Surface((100,100))
    #On remplit l'objet graphique d'une couleur RGB choisie
    fond.fill((192,0,192))
    #On dépose l'objet graphique rectangulaire précédent dans l'objet screen à la position souhaitée    (x ;y)
    ecran.blit(fond,(100,100))
    pygame.display.flip()
    while execution == True :
        time_delta = clock.tick(60)/1000.0  # 60 FPS
        
#Gestion des evenements pygame

        for event in pygame.event.get():
            if event.type == pygame.QUIT :
               execution = False
            elif event.type == pygame.KEYDOWN:
                #Si la touche appuyée est "flèche droite"
                if event.key == pygame.K_RIGHT:
                    x=x+5
                    #Si la touche appuyée est "flèche gauche"
                if event.key == pygame.K_LEFT:
                    x=x-5
                #Si la touche appuyée est "flèche haute"
                if event.key == pygame.K_UP:
                    y=y-5
                #Si la touche appuyée est "flèche basse"
                if event.key == pygame.K_DOWN:
                    y=y+5                                    
# Gestion des boutons
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == RAZ_button:
                        jeu.remplit_grille()
                        rectScreen = ecran.get_rect()                   # mode flemmard
                        police = pygame.font.Font("theboldfont.ttf",36)
                        texte = police.render("Game Over",False,pygame.Color("#000000"))
                        rectTexte = texte.get_rect()
                        rectTexte.center = rectScreen.center            # positionnement a revoir 
                        ecran.blit(texte,rectTexte)
                        texte = police.render("IT'S A WIN !",False,pygame.Color("#000000"))
                        rectTexte = texte.get_rect()
                        rectTexte.center = rectScreen.center            # positionnement a revoir 
                        ecran.blit(texte,rectTexte)
                        jeu.interface.dessine_grille()
                        jeu.score = 0
                        texte_score.html_text = "Score : "+str(jeu.score)+" pts"
                        texte_score.rebuild()
                        perdu = False
                        gagne = False                                                               
            #Afficher l'image de la balle à la nouvelle position (x;y)
            ecran.blit(monimage,(x,y))
            #Réactualiser l'affichage de l'écran graphique
            pygame.display.flip()
    pygame.quit()

# lancement
main()
