import pygame
pygame.init()
largeurecran=1000
hauteurecran=800
ecran=pygame.display.set_mode((largeurecran,hauteurecran))

#Avec le convert_alpha pour récupérer la transparence enregistrée dans la balle sur le pourtour
balle=pygame.image.load("./balle_raquette.png").convert_alpha()
raquette=pygame.image.load("pad_raquette.png")
brique=pygame.image.load("brique.png")
fond=pygame.Surface((largeurecran,hauteurecran))
fond.fill((0,0,0))
ecran.blit(fond,(0,0))
pygame.display.set_caption("Jeu de casse-briques")
pygame.display.set_icon(balle)


#Effets sonores: charger fichiers sons au format wav depuis fichier
sonrebond=pygame.mixer.Sound("rebond.wav")
sonrebondmur=pygame.mixer.Sound("rebond_mur.wav")
soncasse=pygame.mixer.Sound("casse_brique.wav")
sonperdu=pygame.mixer.Sound("perdu.wav")
songagne=pygame.mixer.Sound("gagne.wav")
sonfond=pygame.mixer.Sound("fond.wav")
#lancement du son en mode boucle: le son recommence dès qu'il est terminé (paramètre=-1)
sonfond.play(-1,0,0)

#Nombre de briques par ligne
nbbriquesparligne=4
#Nombre de lignes de briques
nblignesdebriques=3

#Taille de la balle = hauteur=largeur
taille=28
#Tailles de la raquette
largepad=100
hauteurpad=20
#Position de la balle au milieu d'écran
xb=(largeurecran-taille)//2
yb=100
#Initialisations diverses
espacehorizontal=20
espacevertical=10
largeurbrique=80
hauteurbrique=30
#Position de début gauche et haut de la première ligne de briques sur l'écran
gauche=(largeurecran-(largeurbrique+espacehorizontal)*nbbriquesparligne)//2
droite=(hauteurecran-(hauteurbrique+espacevertical)*nblignesdebriques)//2

#Liste des coordonnées briques contenus sur l'écran pour le jeu de casse-brique: coordonnées [x,y]
liste_briques=[]
for i in range(nbbriquesparligne): #Parcours des lignes
    for j in range(nblignesdebriques): #Parcours des colonnes
        liste_briques.append([gauche+i*(largeurbrique+espacehorizontal),droite+j*(hauteurbrique+espacevertical)])

#Trace à l'écran les briques dont les coordonnées sont dans la liste des briques
def trace_briques():
    for coordbrique in liste_briques:
            ecran.blit(brique,(coordbrique[0],coordbrique[1]))


#Centrage de la raquette au milieu d'écran en largeur mais en bas d'écran en ordonnée 760
xr=(largeurecran-largepad)//2
yr=hauteurecran-40
#initialisation du score
score=0

#Créer un objet police de caractères, ici on ne précise pas de nom de police (police par défaut) et la taille de la police est la taille 32 pixels. pygame.font.Font(None, size) : police par défaut de taille « size »
police=pygame.font.Font(None, 32)

#Créer un objet graphique Texte : paramètres= texte à afficher, antialias, couleur du texte en RGB
#le paramètre antialias=True ici indique de créer une image en RGB 24 bits (sinon en 8 bits en palette bicolore si False, donc mauvaise qualité)
texte_perdu=police.render("Vous avez perdu!",True,(255,0,0))
texte_gagne=police.render("Vous avez gagné!",True,(0,255,0))
texte_score=police.render("Score: "+str(score),True,(255,0,0))

#Tracé de la balle, raquette, des briques
ecran.blit(balle,(xb,yb))
ecran.blit(raquette,(xr,yr))
trace_briques()
pygame.display.flip()
horloge = pygame.time.Clock()

#Initialisation du pas de déplacement de la raquette
pasr=10

#Initialisation des pas de déplacements de la balle
pas1=5
pas2=-5

#Perdu indique si on a perdu ou pas (balle perdue), pour savoir si on doit poursuivre le déplacement de raquette ou pas
#Gagne indique si on a cassé toutes les briques
perdu=False
gagne=False

#Gestion de l'enfoncement de touche pour répétition de déplacement de la raquette
pygame.key.set_repeat(20, 10)

execution = True
while execution:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            execution = False
        #On peut déplacer la raquette si on n'a pas perdu (et qu'on appuie sur une touche du clavier)
        if event.type==pygame.KEYDOWN and perdu==False and gagne==False:
            if event.key==pygame.K_RIGHT:
                #Changement abscisse de la raquette vers la droite si appui flèche droite
                xr=xr+pasr
                #Blocage pad raquette à droite si en bord d'écran
                if xr>=largeurecran-largepad:
                    xr=largeurecran-largepad
            if event.key==pygame.K_LEFT:
                #Changement abscisse de la raquette vers la gauche si appui flèche gauche
                xr=xr-pasr
                #Blocage pad raquette à gauche si en bord d'écran
                if xr<=0:
                    xr=0
    #Tout ce qui suit permet de faire déplacer la balle, autorisé seulement si on n'a pas perdu
    if perdu==False and gagne==False:
        #On calcule le déplacement la balle du vecteur de déplacement en x et en y
        xb=xb+pas1
        yb=yb+pas2
        #Rebond automatique de la balle sur paroi gauche et droite
        if xb+taille>=largeurecran or xb<=0:
            pas1=-pas1
            sonrebondmur.play()
        #Perdu si la balle arrive sur la paroi du bas (la raquette ne l'a pas attrapé)
        if yb+taille>hauteurecran:
            perdu=True
            sonperdu.play()
            sonfond.stop()
        #Rebond automatique de la balle sur paroi du haut
        if yb<=0:
            pas2=-pas2
            sonrebondmur.play()
        #Rebond de la balle sur la raquette: il faut que le bas de la balle chevauche la raquette
        if (yb+taille>yr) and (yb+taille<=yr+hauteurpad) and ((xr<=xb and xb<=xr+largepad)or(xr<=xb+taille and xb+taille<=xr+largepad)or(xb>=xr and xb+taille<=xr+largepad)):
            #La balle rebondit vers le haut
            pas2=-pas2
            sonrebond.play()

        #Création de la liste provisoire des briques à conserver (les pas cassées)
        nouvelle_liste=[]
        for coordbrique in liste_briques:
            xbr=coordbrique[0]
            ybr=coordbrique[1]
            #Si chevauchement d'une brique et de la balle (pour rebond balle sur brique et brique cassée)
            if ((ybr<=yb and yb<=ybr+hauteurbrique)or(ybr<=yb+taille and yb+taille<=ybr+hauteurbrique)or(yb>=ybr and yb+taille<=ybr+hauteurbrique))and((xbr<=xb and xb<=xbr+largeurbrique)or(xbr<=xb+taille and xb+taille<=xbr+largeurbrique)or(xb>=xbr and xb+taille<=xbr+largeurbrique)):
                #Quand on rebondit sur une brique on augmente le score
                score=score+1
                soncasse.play()
                texte_score=police.render("Score: "+str(score),True,(255,0,0))
                #La balle rebondit vers le haut
                pas2=-pas2
            else:
                #On ne garde que les briques qu'on n'a pas cassées
                nouvelle_liste.append(coordbrique)
        #Mise à jour de la liste des briques pas cassées vers liste définitive
        liste_briques[:]=nouvelle_liste[:]
        #Si il ne reste aucune brique dans la liste c'est qu'on a gagné
        if len(liste_briques)==0 and gagne==False:
            gagne=True
            songagne.play()
            sonfond.stop()


    #Affichage des objets graphiques à leurs nouvelles coordonnées calculées
    ecran.blit(fond,(0,0))
    ecran.blit(balle,(xb,yb))
    ecran.blit(raquette,(xr,yr))
    trace_briques()
    #Si on a perdu: affichage du texte indiquant que c'est perdu
    if perdu==True:
        ecran.blit(texte_perdu,(largeurecran//2-100,hauteurecran-80))
    #Si on a gagné: affichage du texte indiquant que c'est gagné
    if gagne==True:
        ecran.blit(texte_gagne,(largeurecran//2-100,hauteurecran-80))
    ecran.blit(texte_score,(0,0))
    pygame.display.flip()
    horloge.tick(60)
pygame.quit()