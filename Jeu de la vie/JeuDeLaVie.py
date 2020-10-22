#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=no-member
# pylint : disable=unused-wildcard-import
# pylint: disable=W0614

import pygame
from pygame.locals import *
from random import randint
import pygame_gui

largeur_grille = 80
hauteur_grille = 80

largeur_case = 10

WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0,0,0)
RED = pygame.Color(255,0,0)
GREEN = pygame.Color(0,255,0)
BLUE = pygame.Color(0,0,255)

def determine_position_carre( pos ) :
    x = 10 * int(pos[0]/10)
    y = 10 * int(pos[1]/10)
    return x,y

def dessine_carre_grille(fen,pos,couleur) :
    x,y = determine_position_carre(pos)
    carre = pygame.Rect(x, y, 8, 8)
    pygame.draw.rect(fen, couleur, carre)
    return fen

def dessine_plateau_aleatoire(fen, largeur,hauteur,alea) :
    for i in range(0,largeur,10) : 
        for j in range(0,hauteur,10) : 
            if randint(0,100) > alea :
                fen = dessine_carre_grille(fen, (i,j), WHITE)
    return fen
'''
place_forme
'''
def place_forme( fen, pos, forme ) :
    for i in range(len(forme)) : 
        for j in range(len(forme[i])) :
            couleur = forme[i][j]
            fen = dessine_carre_grille(fen, (pos[0]-5+i*10,pos[1]-5+j*10), couleur)
    return fen
'''
fonction nombre_voisions : calcule le nombre de voisins d'une case (lui non-compris)
'''
def nombre_voisins(tab, x, y) :
    nb_voisins = 0
    for i in range(3) :
        for j in range(3) : 
            if x+i-1 >= 0 and x+i < len(tab) and y+j-1 >= 0 and y+j < len(tab[i])+1 :
                if tab[x+i-1][y+j-1] != BLACK and tab[x+i-1][y+j-1] != RED :
                    if j!=1 or i!=1 :
                        nb_voisins = nb_voisins + 1            
    return nb_voisins
'''
fonction evolution : calcule l'état suivant 
'''
def evolution(fenetre, largeur, hauteur) :
    tableau1 = [[0] * hauteur for _ in range(largeur)]
    tableau2 = [[0] * hauteur for _ in range(largeur)]
    
    for i in range(largeur) : 
        for j in range(hauteur) : 
                tableau1[i][j] = fenetre.get_at((i*10+5,j*10+5))
    for i in range(largeur) : 
        for j in range(hauteur) : 
                nb_voisins = nombre_voisins(tableau1, i, j)
                couleur = tableau1[i][j]
                if nb_voisins == 3 and (couleur == BLACK or couleur == RED):
                    tableau2[i][j] = GREEN
                elif nb_voisins == 3 and (couleur != BLACK and couleur != RED) :
                    tableau2[i][j] = WHITE                    
                elif nb_voisins == 2 and (couleur != BLACK and couleur != RED) :
                    tableau2[i][j] = WHITE                    
                elif nb_voisins == 2 and couleur == BLACK :
                    tableau2[i][j] = BLACK                    
                elif nb_voisins == 2 and couleur == RED :
                    tableau2[i][j] = BLACK                    
                elif nb_voisins == 1 and couleur != BLACK and couleur != RED:
                    tableau2[i][j] = RED                    
                elif nb_voisins == 1 and couleur == RED :
                    tableau2[i][j] = BLACK                    
                elif nb_voisins == 0 and couleur == RED :
                    tableau2[i][j] = BLACK                    
                elif nb_voisins < 1  and couleur != BLACK :
                    tableau2[i][j] = BLACK 
                elif couleur == RED :                  
                    tableau2[i][j] = BLACK                    
                else : 
                    tableau2[i][j] = BLACK                    
    return tableau2

'''
Programme principal
'''

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Jeu de la vie')
    myfont = pygame.font.SysFont('dejavusansmono', 50)
    fenetre = pygame.display.set_mode((largeur_grille*largeur_case+200,hauteur_grille*largeur_case))
    manager = pygame_gui.UIManager((largeur_grille*largeur_case+200,hauteur_grille*largeur_case))
    clock = pygame.time.Clock()

#Placement des boutons avec pygame_gui

    start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((largeur_grille*largeur_case, 0), (98, 49)),
                                             text='Départ',
                                             manager=manager)
    RAZ_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((largeur_grille*largeur_case+100, 0), (98, 49)),
                                             text='RAZ',
                                             manager=manager)
    relance_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((largeur_grille*largeur_case, 50), (98, 49)),
                                             text='Peuple',
                                             manager=manager)
    pause_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((largeur_grille*largeur_case+100, 50), (98, 49)),
                                             text='Pause',
                                             manager=manager)
    texte_etat = pygame_gui.elements.UITextBox(html_text="Etat : <b>en pause</b>",
                                             relative_rect=pygame.Rect((largeur_grille*largeur_case, 100), (198, 49)),
                                             manager=manager)
    texte_generation = pygame_gui.elements.UITextBox(html_text="Génération n°0",
                                             relative_rect=pygame.Rect((largeur_grille*largeur_case, 150), (198, 49)),
                                             manager=manager)
    texte_formes = pygame_gui.elements.UITextBox(html_text="Formes prédéfinies<br>Sélectionnez une forme, puis cliquez sur la grille",
                                             relative_rect=pygame.Rect((largeur_grille*largeur_case, 200), (198, 98)),
                                             manager=manager)
    planeur_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((largeur_grille*largeur_case, 300), (98, 49)),
                                             text='Planeur',
                                             manager=manager)
    canon_button1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((largeur_grille*largeur_case+100, 300), (98, 49)),
                                             text='Canon vert.',
                                             manager=manager)
    canon_button2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((largeur_grille*largeur_case+100, 350), (98, 49)),
                                             text='Canon hor.',
                                             manager=manager)
# Declaration des variables 
                             
    #fenetre = dessine_plateau_aleatoire(fenetre,largeur_grille*largeur_case,hauteur_grille*largeur_case,90)
    execution = True
    pause = True
    tableau = False
    mode_placement = False
    generation = -1
    planeur =  [[BLACK,BLACK,GREEN],
                [GREEN,BLACK,GREEN],
                [BLACK,GREEN,GREEN]]
    """
    canon = [   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
                [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
                [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    """
    canon = [   [BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,GREEN,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK],
                [BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,GREEN,BLACK,GREEN,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK],
                [BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,GREEN,GREEN,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,GREEN,GREEN,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,GREEN,GREEN],
                [BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,GREEN,BLACK,BLACK,BLACK,GREEN,BLACK,BLACK,BLACK,BLACK,GREEN,GREEN,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,GREEN,GREEN],
                [GREEN,GREEN,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,GREEN,BLACK,BLACK,BLACK,BLACK,BLACK,GREEN,BLACK,BLACK,BLACK,GREEN,GREEN,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK],
                [GREEN,GREEN,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,GREEN,BLACK,BLACK,BLACK,GREEN,BLACK,GREEN,GREEN,BLACK,BLACK,BLACK,BLACK,GREEN,BLACK,GREEN,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK],
                [BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,GREEN,BLACK,BLACK,BLACK,BLACK,BLACK,GREEN,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,GREEN,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK],
                [BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,GREEN,BLACK,BLACK,BLACK,GREEN,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK],
                [BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,GREEN,GREEN,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK]]
    canon_horizontal = []
    
    for j in range(len(canon[0])):
        tab = []
        for i in range(len(canon)) :
            tab.append(canon[i][len(canon[0])-j-1])
        canon_horizontal.append(tab)
        
    #pygame.display.flip()
    while execution == True :
        time_delta = clock.tick(60)/1000.0
        

#Gestion du mode hors pause ( le cas général )

        if pause == False : 
            generation += 1
            texte_generation.html_text = "Génération n°"+str(generation)
            texte_generation.rebuild()
            tableau = evolution(fenetre, largeur_grille, hauteur_grille)
            for i in range(largeur_grille) :
                for j in range(hauteur_grille) :
                    fenetre = dessine_carre_grille(fenetre,(i*10,j*10),tableau[i][j])

#Gestion des evenements pygame

        for event in pygame.event.get():
            if event.type == pygame.QUIT :
               execution = False
            elif event.type == pygame.MOUSEBUTTONDOWN :
                position = pygame.mouse.get_pos()
                couleur = fenetre.get_at(position)
                if mode_placement == False :
                    if position[0] < largeur_grille*largeur_case and position[1]< hauteur_grille*largeur_case:
                        if couleur == WHITE :
                            fenetre = dessine_carre_grille(fenetre, position,RED)
                        elif couleur == BLACK :
                            fenetre = dessine_carre_grille(fenetre, position,WHITE)
                        elif couleur == RED :
                            fenetre = dessine_carre_grille(fenetre, position,BLACK)
                else :
                    if position[0] < largeur_grille*largeur_case-len(forme_a_placer[0]) and position[1]< hauteur_grille*largeur_case :
                        fenetre = place_forme(fenetre, position, forme_a_placer)
                        mode_placement = False
                        texte_etat.html_text = "Etat : <b>en pause</b>"                        
                        texte_etat.rebuild()
# Gestion des boutons

            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_button:
                        if not tableau :
                            fenetre = dessine_plateau_aleatoire(fenetre,largeur_grille*largeur_case,hauteur_grille*largeur_case,90)
                            texte_etat.html_text = 'Etat : <b>fonctionne</b>'
                            texte_etat.rebuild()       
                        pause = False
                    elif event.ui_element == RAZ_button:
                        generation = -1
                        if tableau :
                            tableau.clear()                        
                        for i in range(largeur_grille) :
                            for j in range(hauteur_grille) :
                                fenetre = dessine_carre_grille(fenetre,(i*10,j*10),BLACK)                       
                    elif event.ui_element == relance_button:
                        fenetre = dessine_plateau_aleatoire(fenetre,largeur_grille*largeur_case,hauteur_grille*largeur_case,90)
                    elif event.ui_element == pause_button:
                        pause = not pause
                        if pause :
                            texte_etat.html_text = 'Etat : <b>en pause</b>'
                        else :
                            texte_etat.html_text = 'Etat : <b>fonctionne</b>'
                        texte_etat.rebuild()
                    elif event.ui_element == planeur_button:
                        pause = True
                        mode_placement = True
                        forme_a_placer = planeur
                        texte_etat.html_text = "Etat : <b>placement d'un planeur"                        
                        texte_etat.rebuild()
                    elif event.ui_element == canon_button1:
                        pause = True
                        mode_placement = True
                        forme_a_placer = canon
                        texte_etat.html_text = "Etat : <b>placement d'un canon vertical"                        
                        texte_etat.rebuild()
                    elif event.ui_element == canon_button2:
                        pause = True
                        mode_placement = True
                        forme_a_placer = canon_horizontal
                        texte_etat.html_text = "Etat : <b>placement d'un canon horizontal"                        
                        texte_etat.rebuild()
            manager.process_events(event)

# updates

        manager.update(time_delta)
        #window_surface.blit(background, (0, 0))
        manager.draw_ui(fenetre)
        pygame.display.update()
        pygame.display.flip()

# Sortie

    pygame.quit()
    #pygame.quit