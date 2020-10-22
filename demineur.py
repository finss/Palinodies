#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
"""Le démineur est un jeu de réflexion dont le but est de localiser des mines cachées dans un champ
virtuel avec pour seule indication le nombre de mines dans les zones adjacentes. ( voir
https://fr.wikipedia.org/wiki/D%C3%A9mineur_(genre_de_jeu_vid%C3%A9o )
La conception et l’implémentation d’un démineur demandent l’utilisation de plusieurs concepts.
Parmi ceux-ci on note la gestion de tableaux en plusieurs dimensions ou l’utilisation de fonction récursive."""

# pylint: disable=no-member
# pylint : disable=unused-wildcard-import
# pylint: disable=W0614

import pygame
from pygame.locals import *
from random import randint
import pygame_gui

largeur_grille = 80
hauteur_grille = 40

taille_case = 20
nombre_mines = 320

score = (nombre_mines,largeur_grille*hauteur_grille-nombre_mines)

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

"""
red -> drapeau
dark gray -> case couverte
light gray -> case vide
"""

class Demineur :
    def __init__(self, ecran, largeur, hauteur, taille_case, nbmines):
        self.ecran = ecran
        self.largeur = largeur
        self.hauteur = hauteur
        self.taille_case = taille_case
        self.nbmines = nbmines        
        self.tableau = [[0] * hauteur for _ in range(largeur)]
        self.score = (nbmines,largeur*hauteur - nbmines)
        self.interface = Interface(ecran, self.tableau, largeur*taille_case, hauteur*taille_case, taille_case)

    def remplit_grille(self) :
        for i in range(self.largeur) : 
            for j in range(self.hauteur) :
                self.tableau[i][j] = [0,False,0] # couverte, pas de mine, aucune mine voisine
        for i in range(self.nbmines) :
            mine_place = False
            while not mine_place  :
                x =randint(0,self.largeur-1)
                y = randint(0,self.hauteur-1)            
                if self.tableau[x][y] != [0,True,1] : #couverte, présence de mine, aucune mine voisine
                    self.tableau[x][y] = [0,True,1] 
                    mine_place = True
            for j in range(x-1,x+2) :
                for k in range(y-1,y+2) :
                    if j>=0 and k>=0 and j<len(self.tableau) and k<len(self.tableau[j]) :
                        if self.tableau[j][k][1] == 0 :
                            self.tableau[j][k][2] += 1
        return self.tableau   

    def decouvre_mine(self, pos) :
        (x,y) = pos
        self.score = (self.score[0],self.score[1]- 1)
        if self.tableau[x][y][1] == True :              # présence de mine -> GAME OVER
            self.tableau[x][y][0] = 3
            return True                   # True : partie perdue
        else :
            self.tableau[x][y][0] = 1
            self.tableau = self.decouvre(pos)
        return False    

    def decouvre(self, pos) :
        x,y = pos
        for i in range(x-1,x+2) :
            for j in range(y-1,y+2) :
                if i>=0 and j>=0 and i<=len(self.tableau)-1 and j<=len(self.tableau[0])-1 :
                    if self.tableau[i][j][1] == 0 :         # absence de mine
                        if self.tableau[i][j][2] == 0 and self.tableau[i][j][0] == 0 :      # pas de mine voisine et case couverte 
                            self.tableau[i][j][0] = 1                # découvre case
                            self.score = (self.score[0],self.score[1]- 1)
                            self.decouvre((i,j))
                        if self.tableau[i][j][2] != 0 and self.tableau[i][j][0] == 1:        # une ou plusieurs mines autour et case découverte
                            pass
                        if self.tableau[i][j][2] != 0 and self.tableau[i][j][0] == 0:        # une ou plusieurs mines autour et case couverte
                            self.tableau[i][j][0] = 1
                            self.score = (self.score[0],self.score[1]- 1)
        return self.tableau

class Interface :
    def __init__(self, ecran, tableau, largeur, hauteur, taille_case):
        self.ecran = ecran
        self.tableau = tableau
        self.largeur = largeur                  # en pixels
        self.hauteur = hauteur
        self.taille_case = taille_case
        self.ecran

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

def main() :

    pygame.init()
    pygame.display.set_caption('Démineur')
    ecran = pygame.display.set_mode((largeur_grille*taille_case+200,hauteur_grille*taille_case))
    manager = pygame_gui.UIManager((largeur_grille*taille_case+200,hauteur_grille*taille_case))
    jeu = Demineur(ecran,largeur_grille, hauteur_grille,  taille_case, nombre_mines)
    clock = pygame.time.Clock()  
    #Placement des boutons avec pygame_gui
    RAZ_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((largeur_grille*taille_case, 0), (98, 49)),
                                                text='RAZ',
                                                manager=manager)
    texte_score = pygame_gui.elements.UITextBox(html_text="Score : "+str(jeu.score[0])+" mines restantes<br>"+str(jeu.score[1])+" cases à découvrir",
                                                relative_rect=pygame.Rect((largeur_grille*taille_case, 50), (198, 98)),
                                                manager=manager)
#boucle pincipale 

    jeu.remplit_grille()      
    jeu.interface.dessine_grille()
    pygame.display.update() 
    perdu = False
    gagne = False
    execution = True
    while execution == True :
        time_delta = clock.tick(60)/1000.0  # 60 FPS
        
#Gestion des evenements pygame

        for event in pygame.event.get():
            if event.type == pygame.QUIT :
               execution = False
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
                        jeu.score = (nombre_mines,largeur_grille*hauteur_grille-nombre_mines)
                        texte_score.html_text = "Score : "+str(jeu.score[0])+" mines restantes <br>"+str(jeu.score[1])+" cases à découvrir"
                        texte_score.rebuild()
                        perdu = False
                        gagne = False                                                               
# gestion de la souris            
            elif event.type == pygame.MOUSEBUTTONDOWN and not perdu :    # clic de souris
                position = pygame.mouse.get_pos()
                (x,y) = jeu.interface.determine_position_grille(position)
                if x<largeur_grille and y<hauteur_grille :
                    if event.button == 1 :                  # gestion du bouton gauche de la souris
                        if jeu.tableau[x][y][0] == 0 :           # si la mine est couverte sans drapeau
                            perdu = jeu.decouvre_mine((x,y))
                            jeu.ecran = jeu.interface.dessine_case((x,y), BLACK)                            
                            #perdu = False    # TRICHE POUR DEBUG
                    elif event.button == 3 :                # gestion du bouton droit de la souris
                        if jeu.tableau[x][y][0] == 0 :
                            jeu.tableau[x][y][0] = 2              # on met un drapeau
                            jeu.score = (jeu.score[0]-1,jeu.score[1])
                        elif jeu.tableau[x][y][0] == 2 :
                            jeu.tableau[x][y][0] = 0              #on enleve un drapeau
                            jeu.score = (jeu.score[0]+1,jeu.score[1])
                texte_score.html_text = "Score : "+str(jeu.score[0])+" mines restantes <br>"+str(jeu.score[1])+" cases à découvrir"
                texte_score.rebuild()
                if jeu.score == (0,0) :
                    gagne = True
            manager.process_events(event)
# updates
        if perdu :
            rectScreen = jeu.ecran.get_rect()
            police = pygame.font.Font("theboldfont.ttf",36)  
            texte = police.render("Game Over",False,pygame.Color("#FFFF00"))
            rectTexte = texte.get_rect()
            rectTexte.center = rectScreen.center                            # positionnement a revoir 
            jeu.ecran.blit(texte,rectTexte)
        else :
            if gagne :
                jeu.interface.dessine_grille()
                rectScreen = ecran.get_rect()
                police = pygame.font.Font("theboldfont.ttf",36)
                texte = police.render("IT'S A WIN !",False,pygame.Color("#FFFF00"))
                rectTexte = texte.get_rect()
                rectTexte.center = rectScreen.center            # positionnement a revoir 
                ecran.blit(texte,rectTexte)
            else :
                jeu.interface.dessine_grille()            
        manager.update(time_delta)
        manager.draw_ui(ecran)
        pygame.display.update()
        
    pygame.quit()

# lancement
main()
