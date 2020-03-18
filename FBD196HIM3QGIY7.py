import pygame
from pygame.locals import*
from sys import exit
from random import randint

#starting the pygame     
pygame.init()
#creating the screen 400x400
screen = pygame.display.set_mode((400, 400), 0, 32)
#generating random number to select the background
fundo_number = randint(1,5)
#concatenating 'fundo_number' with the name of background
fundo = 'fundo' + str(fundo_number) + '.png'
#loading the selected background
background = pygame.image.load(fundo).convert()
#setting Win and Lost images
vencer = 'venceu.png'
perder = 'perdeu.png'
#loading the Win and Lost screen
venceu = pygame.image.load(vencer).convert_alpha()
perdeu = pygame.image.load(perder).convert_alpha()
#setting the caption 
pygame.display.set_caption('Capcom VS Capcom!!')
#setting the Clock
clock = pygame.time.Clock()

#generating initial cards, concatening and loading the images
card0 = randint(1, 23)
sprite_card0 = 'Cartas\cartas' + str(card0) + '.png'
card00 = pygame.image.load(sprite_card0).convert_alpha()
card1 = randint(1, 23)
sprite_card1 = 'Cartas\cartas' + str(card1) + '.png'
card01 = pygame.image.load(sprite_card1).convert_alpha()
card2 = randint(1, 23)
sprite_card2 = 'Cartas\cartas' + str(card2) + '.png'
card02 = pygame.image.load(sprite_card2).convert_alpha()
#generating initial cards, concatening and loading the images

#setting the life points
pontos_de_vida = 4000
#setting the enemy life points
pontos_de_vida_op = 4000
#setting the font of texts
font = pygame.font.SysFont("Arial", 50)
#setting coordenates X and Y for cards
x0 = 30
y0 = 304
x1 = 97
x2 = 164
#generating a null image in the battle field
pixel = 'pixel.png'
#Boolean variable that determines if the card is in field
esta_em_campo = False
#Boolean variable that determines if the enemy card is in field
op_em_campo = False
#Damage variable
dano = 0

#Printing the controls in console
print """Aperte a tecla Z para colocar a primeira carta da sua mão em campo.
Aperte a tecla X para colocar a segunda carta da sua mão em campo.
Aperte a tecla C para colocar a terceira carta da sua mão em campo.
Aperte a tecla ALT para trocar a carta em campo.
Aperte a tecla SPACE para atacar o oponente com a carta selecionada.
"""
#Main loop:
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            #exit command
            exit()

    #setting the card in battle field
    card_in_battle = pygame.image.load(pixel).convert_alpha()
    #detecting pressed keys
    tecla = pygame.key.get_pressed()
    if tecla[K_z]:
        if esta_em_campo == False:
            #first card in battle
            pixel = sprite_card0
            #generating another card
            aleatoria = randint(1, 23)
            sprite_card0 = 'Cartas\cartas' + str(aleatoria) + '.png'
            card00 = pygame.image.load(sprite_card0).convert_alpha()
            esta_em_campo = True
    if tecla[K_x]:
        if esta_em_campo == False:
            #second card in battle
            pixel = sprite_card1
            #generating another card
            aleatoria = randint(1, 23)
            sprite_card1 = 'Cartas\cartas' + str(aleatoria) + '.png'
            card01 = pygame.image.load(sprite_card1).convert_alpha()
            esta_em_campo = True

    if tecla[K_c]:
        if esta_em_campo == False:
            #third card in battle
            pixel = sprite_card2
            #generating another card
            aleatoria = randint(1, 23)
            sprite_card2 = 'Cartas\cartas' + str(aleatoria) + '.png'
            card02 = pygame.image.load(sprite_card2).convert_alpha()
            esta_em_campo = True

    if op_em_campo == False:
        #when the enemy card is defeated generates another card
        escolha_aleatoria = randint(1, 23)
        op_em_campo = True
    #loading the enemy card
    sprite_op = 'Cartas\cartas' + str(escolha_aleatoria) + '.png'
    carta_do_oponente = pygame.image.load(sprite_op).convert_alpha()   
        
    if tecla[K_SPACE] and op_em_campo == True and esta_em_campo == True:
        #detecting the battle force
        if pixel=='Cartas\cartas1.png':
            battle_force=1000
        elif pixel=='Cartas\cartas2.png':
            battle_force=700
        elif pixel=='Cartas\cartas3.png':
            battle_force=500
        elif pixel=='Cartas\cartas4.png':
            battle_force=700
        elif pixel=='Cartas\cartas5.png':
            battle_force=500
        elif pixel=='Cartas\cartas6.png':
            battle_force=400
        elif pixel=='Cartas\cartas7.png':
            battle_force=400
        elif pixel=='Cartas\cartas8.png':
            battle_force=700
        elif pixel=='Cartas\cartas9.png':
            battle_force=600
        elif pixel=='Cartas\cartas10.png':
            battle_force=500
        elif pixel=='Cartas\cartas11.png':
            battle_force=1000
        elif pixel=='Cartas\cartas12.png':
            battle_force=800
        elif pixel=='Cartas\cartas13.png':
            battle_force=300
        elif pixel=='Cartas\cartas14.png':
            battle_force=400
        elif pixel=='Cartas\cartas15.png':
            battle_force=400
        elif pixel=='Cartas\cartas16.png':
            battle_force=300
        elif pixel=='Cartas\cartas17.png':
            battle_force=300
        elif pixel=='Cartas\cartas18.png':
            battle_force=800
        elif pixel=='Cartas\cartas19.png':
            battle_force=600
        elif pixel=='Cartas\cartas20.png':
            battle_force=700
        elif pixel=='Cartas\cartas21.png':
            battle_force=600
        elif pixel=='Cartas\cartas22.png':
            battle_force=1000
        elif pixel=='Cartas\cartas23.png':
            battle_force=1200
        #detecting the enemy battle force
        if sprite_op=='Cartas\cartas1.png':
            c_battle_force=1000
        elif sprite_op=='Cartas\cartas2.png':
            c_battle_force=700
        elif sprite_op=='Cartas\cartas3.png':
            c_battle_force=500
        elif sprite_op=='Cartas\cartas4.png':
            c_battle_force=700
        elif sprite_op=='Cartas\cartas5.png':
            c_battle_force=500
        elif sprite_op=='Cartas\cartas6.png':
            c_battle_force=400
        elif sprite_op=='Cartas\cartas7.png':
            c_battle_force=400
        elif sprite_op=='Cartas\cartas8.png':
            c_battle_force=700
        elif sprite_op=='Cartas\cartas9.png':
            c_battle_force=600
        elif sprite_op=='Cartas\cartas10.png':
            c_battle_force=500
        elif sprite_op=='Cartas\cartas11.png':
            c_battle_force=1000
        elif sprite_op=='Cartas\cartas12.png':
            c_battle_force=800
        elif sprite_op=='Cartas\cartas13.png':
            c_battle_force=300
        elif sprite_op=='Cartas\cartas14.png':
            c_battle_force=400
        elif sprite_op=='Cartas\cartas15.png':
            c_battle_force=400
        elif sprite_op=='Cartas\cartas16.png':
            c_battle_force=300
        elif sprite_op=='Cartas\cartas17.png':
            c_battle_force=300
        elif sprite_op=='Cartas\cartas18.png':
            c_battle_force=800
        elif sprite_op=='Cartas\cartas19.png':
            c_battle_force=600
        elif sprite_op=='Cartas\cartas20.png':
            c_battle_force=700
        elif sprite_op=='Cartas\cartas21.png':
            c_battle_force=600
        elif sprite_op=='Cartas\cartas22.png':
            c_battle_force=1000
        elif sprite_op=='Cartas\cartas23.png':
            c_battle_force=1200
        #detecting damage
        if battle_force > c_battle_force:
            dano = battle_force - c_battle_force
            pontos_de_vida_op -= dano
            op_em_campo = False
        if battle_force < c_battle_force:
            dano = c_battle_force - battle_force
            pontos_de_vida -= dano
            esta_em_campo = False
            pixel = 'pixel.png'
        if battle_force == c_battle_force:
            op_em_campo = False
            esta_em_campo = False
            pixel = 'pixel.png'
        
    #generating the life points text
    vida1 = font.render(str(pontos_de_vida), 1, (255, 0, 0))
    vida2 = font.render(str(pontos_de_vida_op), 1, (255, 0, 0))
    
    if tecla[K_LALT]:
        #changing the boolean variable to change the card in battle
        esta_em_campo = False

    if pontos_de_vida <= 0 and pontos_de_vida_op > 0:
        #detecting the game winner and displaying the lost mesage
        screen.blit(perdeu, (0,0))
        pygame.display.update()
        pygame.time.wait(3000)
        exit()
    if pontos_de_vida_op <= 0 and pontos_de_vida > 0:
        #detecting the game winner and displaying the win mesage
        screen.blit(venceu, (0,0))
        pygame.display.update()
        pygame.time.wait(3000)
        exit()     
    #displaying the background
    screen.blit(background, (0, 0))
    #displaying the first card
    screen.blit(card00, (x0, y0))
    #displaying the second card
    screen.blit(card01, (x1, y0))
    #displaying the third card
    screen.blit(card02, (x2, y0))
    #displaying the card in battle
    screen.blit(card_in_battle, (x2, 200))
    #displaying the enemy card in battle
    screen.blit(carta_do_oponente, (30, 40))
    #displaying the life points
    screen.blit(vida1, (300, 345))
    #displaying the enemy life points
    screen.blit(vida2, (300, 0))
    #updating
    pygame.display.update()
    #Limiting the fps to 10
    time_passed = clock.tick(10)
