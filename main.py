'''
# Reglurnar:
Leikurinn Calculatorr er stærðfræðileikur fyrir 2 spilara.
Á skjánum mun koma Stærðfræði Dæmi.
Spilarar reikna dæmin og setja svörin í borðið og svo smella í stóra takkan til að seta inn svar.
Sá sem fyrstur skrifar rétta svarið vinnur stig. Fyrstur í 10 stig vinnur.
Ef þú setur inn rangt svar fær aðstæðingur 1 stig.

Hvernig á að byrja?
Smelltu á Stóra Græna takkan.
Þú hefur 3 sekúndur til að leikurinn byrji.
Þegar leikur byrjar birtist dæmi á skjánum.


'''

from machine import Pin, SoftI2C
from i2c_lcd import I2cLcd
import time
import random
import neopixel
from buzzer_music import music

# 1. Configuració de la connexió (Pins 13 i 14 segons el teu codi)
i2c = SoftI2C(scl=Pin(13), sda=Pin(14), freq=400000)

# 2. Inicialització de la pantalla
# L'adreça sol ser 0x27 o 0x3f. Si no funciona amb una, prova l'altra.
lcd = I2cLcd(i2c, 0x27, 2, 16)

# Definició de punts:
p1 = 0
p2 = 0

# 3. Escriure a la pantalla
lcd.clear()           # Limpia la pantalla 
lcd.move_to(0, 0)     # Columna 0, Fila 0
lcd.putstr("Hey there!") 
lcd.move_to(0, 1)     # Columna 0, Fila 1
lcd.putstr("Wanna play?")

hjarta = [0b00000,
          0b11011,
          0b11011,
          0b00000,
          0b01010,
          0b01110,
          0b00000,
          0b00000]
# Það er hægt að hafa 8 sértákn, sæti 0 til og með 7.
lcd.custom_char(0, hjarta) # geymum hjartað í sæti 0
lcd.move_to(10, 0)
lcd.putstr(f"{chr(0)}") # skrifum út hjartað sem er í sæti 0


time.sleep_ms(1000)
lcd.clear()         

lcd.move_to(0, 0)
lcd.putstr("How much is:")


# Definició dels teclats:
files2_pins = [4, 5, 6, 7]
cols2_pins = [15, 16, 17, 18]

files1_pins = [8, 3, 46, 9]
cols1_pins = [45, 48, 47, 21]

files1 = [Pin(p, Pin.OUT) for p in files1_pins]
cols1 = [Pin(p, Pin.IN, Pin.PULL_DOWN) for p in cols1_pins]

files2 = [Pin(p, Pin.OUT) for p in files2_pins]
cols2 = [Pin(p, Pin.IN, Pin.PULL_DOWN) for p in cols2_pins]

mapa_tecles1 = [['1','2','3','A'],['4','5','6','B'],['7','8','9','C'],['*','0','#','D']]
mapa_tecles2 = [['1','2','3','A'],['4','5','6','B'],['7','8','9','C'],['*','0','#','D']]

# Botó jugador 1 
boto_p1 = Pin(42, Pin.IN, Pin.PULL_UP)

def llegir_boto_p1():
    if boto_p1.value() == 0:  # premut (a GND)
        time.sleep_ms(30)
        while boto_p1.value() == 0:
            music_tick()
            time.sleep_ms(1)
        time.sleep_ms(30)
        return True
    return False

boto_p2 = Pin(41, Pin.IN, Pin.PULL_UP)

def llegir_boto_p2():
    if boto_p2.value() == 0:  # premut (a GND)
        time.sleep_ms(30)
        while boto_p2.value() == 0:
            music_tick()
            time.sleep_ms(1)
        time.sleep_ms(30)
        return True
    return False

# Primera fila: (0,0)
# Segona fila: (0,1)
# Mig: (8,0)

#Teclado 1:
def llegir_tecla1():
    for f_num, fila in enumerate(files1):
        fila.value(1)
        for c_num, col in enumerate(cols1):
            if col.value() == 1:
                # 1. Petit retard per ignorar les vibracions inicials
                music_tick()
                time.sleep_ms(20) 
                # 2. Esperem que deixis anar la tecla (el teu "pass")
                while col.value() == 1: 
                    music_tick()
                    time.sleep_ms(1)
                # 3. Un altre petit retard perquè en deixar-la anar no reboti
                music_tick()
                time.sleep_ms(20) 
                fila.value(0)
                return mapa_tecles1[f_num][c_num]
        fila.value(0)
    return None

#Teclado 2:
def llegir_tecla2():
    for f_num, fila in enumerate(files2):
        fila.value(1)
        for c_num, col in enumerate(cols2):
            if col.value() == 1:
                # 1. Petit retard per ignorar les vibracions inicials
                music_tick()
                time.sleep_ms(20) 
                # 2. Esperem que deixis anar la tecla (el teu "pass")
                while col.value() == 1: 
                    music_tick()
                    time.sleep_ms(1)
                # 3. Un altre petit retard perquè en deixar-la anar no reboti
                music_tick()
                time.sleep_ms(20) 
                fila.value(0)
                return mapa_tecles2[f_num][c_num]
        fila.value(0)
    return None

# Pin aro
pin_aro = Pin(20, Pin.OUT)
aro = neopixel.NeoPixel(pin_aro, 24)

def compte_enrera():
    # Colors: vermell, ambre, verd
    colors = [(255, 0, 0), (255, 80, 0), (0, 255, 0)]

    for color in colors:
        for i in range(24):
            aro[i] = color
        aro.write()
        time.sleep(1)

    # Apaguem l'aro al final
    for i in range(24):
        aro[i] = (0, 0, 0)
    aro.write()
    
# --- SO (buzzer_music) ---
BUZZER_PIN = 35
song_text ='0 E3 1 0;2 E4 1 0;4 E3 1 0;6 E4 1 0;8 E3 1 0;10 E4 1 0;12 E3 1 0;14 E4 1 0;16 A3 1 0;18 A4 1 0;20 A3 1 0;22 A4 1 0;24 A3 1 0;26 A4 1 0;28 A3 1 0;30 A4 1 0;32 G#3 1 0;34 G#4 1 0;36 G#3 1 0;38 G#4 1 0;40 E3 1 0;42 E4 1 0;44 E3 1 0;46 E4 1 0;48 A3 1 0;50 A4 1 0;52 A3 1 0;54 A4 1 0;56 A3 1 0;58 B3 1 0;60 C4 1 0;62 D4 1 0;64 D3 1 0;66 D4 1 0;68 D3 1 0;70 D4 1 0;72 D3 1 0;74 D4 1 0;76 D3 1 0;78 D4 1 0;80 C3 1 0;82 C4 1 0;84 C3 1 0;86 C4 1 0;88 C3 1 0;90 C4 1 0;92 C3 1 0;94 C4 1 0;96 G2 1 0;98 G3 1 0;100 G2 1 0;102 G3 1 0;104 E3 1 0;106 E4 1 0;108 E3 1 0;110 E4 1 0;114 A4 1 0;112 A3 1 0;116 A3 1 0;118 A4 1 0;120 A3 1 0;122 A4 1 0;124 A3 1 0;0 E6 1 1;4 B5 1 1;6 C6 1 1;8 D6 1 1;10 E6 1 1;11 D6 1 1;12 C6 1 1;14 B5 1 1;0 E5 1 6;4 B4 1 6;6 C5 1 6;8 D5 1 6;10 E5 1 6;11 D5 1 6;12 C5 1 6;14 B4 1 6;16 A5 1 1;20 A5 1 1;22 C6 1 1;24 E6 1 1;28 D6 1 1;30 C6 1 1;32 B5 1 1;36 B5 1 1;36 B5 1 1;37 B5 1 1;38 C6 1 1;40 D6 1 1;44 E6 1 1;48 C6 1 1;52 A5 1 1;56 A5 1 1;20 A4 1 6;16 A4 1 6;22 C5 1 6;24 E5 1 6;28 D5 1 6;30 C5 1 6;32 B4 1 6;36 B4 1 6;37 B4 1 6;38 C5 1 6;40 D5 1 6;44 E5 1 6;48 C5 1 6;52 A4 1 6;56 A4 1 6;64 D5 1 6;64 D6 1 1;68 D6 1 1;70 F6 1 1;72 A6 1 1;76 G6 1 1;78 F6 1 1;80 E6 1 1;84 E6 1 1;86 C6 1 1;88 E6 1 1;92 D6 1 1;94 C6 1 1;96 B5 1 1;100 B5 1 1;101 B5 1 1;102 C6 1 1;104 D6 1 1;108 E6 1 1;112 C6 1 1;116 A5 1 1;120 A5 1 1;72 A5 1 6;80 E5 1 6;68 D5 1 7;70 F5 1 7;76 G5 1 7;84 E5 1 7;78 F5 1 7;86 C5 1 7;88 E5 1 6;96 B4 1 6;104 D5 1 6;112 C5 1 6;120 A4 1 6;92 D5 1 7;94 C5 1 7;100 B4 1 7;101 B4 1 7;102 C5 1 7;108 E5 1 7;116 A4 1 7'

mySong = music(song_text, pins=[Pin(BUZZER_PIN)])
music_on = False

def music_tick():
    if music_on:
        mySong.tick()

def esperar_ms(ms):
    # Espera sense tallar la música
    t0 = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), t0) < ms:
        music_tick()
        time.sleep_ms(40)

# Configuració dels Leds 1:
pin_leds1 = Pin(11, Pin.OUT)
tira1 = neopixel.NeoPixel(pin_leds1, 10)

# Configuració dels Leds 2:
pin_leds2 = Pin(12, Pin.OUT)
tira2 = neopixel.NeoPixel(pin_leds2, 10)

for i in range(10):
    tira1[i] = (0, 0, 0)
    tira2[i] = (0, 0, 0)
    
tira1.write()
tira2.write()


def apagar_leds():
    # Apaga tires
    for i in range(10):
        tira1[i] = (0, 0, 0)
        tira2[i] = (0, 0, 0)
    tira1.write()
    tira2.write()

    # Apaga aro
    for i in range(24):
        aro[i] = (0, 0, 0)
    aro.write()


def esperar_reinici():
    # 1) Primer esperem que els dos botons estiguin SOLTS
    while boto_p1.value() == 0 or boto_p2.value() == 0:
        time.sleep_ms(10)

    # 2) Ara esperem una pulsació nova
    while True:
        if llegir_boto_p1() or llegir_boto_p2():
            return
        time.sleep_ms(10)


def fi_de_partida(guanyador):
    global p1, p2
    global music_on
    music_on = False

    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr(f"P{guanyador} wins!")

    # Deixem tot apagat mentre esperem
    apagar_leds()

    lcd.move_to(0, 1)
    lcd.putstr("Press to restart")

    esperar_reinici()

    # Reinici del joc
    p1 = 0
    p2 = 0
    actualitzar_marcador_led()
    apagar_leds()

    # Torna a començar amb compte enrere
    compte_enrera()
    music_on = True



def comprovar_guanyador():
    if p1 >= 10:
        fi_de_partida(1)
        return True
    if p2 >= 10:
        fi_de_partida(2)
        return True
    return False



def actualitzar_marcador_led():
    global p1, p2
    
    if p1 < 0: p1 = 0
    if p2 < 0: p2 = 0
    if p1 > 10: p1 = 10
    if p2 > 10: p2 = 10
    
    
    for i in range(10):
        tira1[i] = (0, 0, 0)
        tira2[i] = (0, 0, 0)
    # Omplim la tira 1 segons els punts del P1 (Color Blau)
    for i in range(p1):
        if i < 10: tira1[i] = (0, 0, 255)
            
    # Omplim la tira 2 segons els punts del P2 (Color Vermell)
    for i in range(p2):
        if i < 10: tira2[i] = (255, 0, 0)
        
    tira1.write()
    tira2.write()

def joc_mates():
    global p1, p2
    # 1. Triem dos números
    n1 = random.randint(0, 10)
    n2 = random.randint(0, 10)
    
    # 2. Triem el tipus d'operació a l'atzar
    tipus = random.choice(['+', '-', '*'])
    
    # 3. Calculem el resultat correcte segons l'operació triada
    if tipus == '+':
        res_correcte = n1 + n2
    elif tipus == '-':
        # Per evitar resultats negatius, posem el gran primer
        if n1 < n2: n1, n2 = n2, n1
        res_correcte = n1 - n2
    elif tipus == '*':
        res_correcte = n1 * n2

    # 4. Mostrem l'operació a la pantalla
    operacio_text = f"{n1}{tipus}{n2}="
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr(operacio_text)
    
    lcd.move_to(0, 1)
    lcd.putstr("P1:")
    
    lcd.move_to(8, 1)
    lcd.putstr("P2:")
    
    lcd.move_to(0, 0)
    
    
# Respuesta 1:
    intent1 = ""
    intent2 = ""
    while True:
        music_tick()
        #correcte_text = random.choice([Incorrect, Neii!! ])
        tecla1 = None
        if llegir_boto_p1():
            tecla1 = "#"
        else:
            tecla1 = llegir_tecla1()
        if tecla1:
            if tecla1.isdigit():
                intent1 += tecla1
                lcd.move_to(3, 1) 
                lcd.putstr(intent1) 
            
            elif tecla1 == "#": # Botó Enter
                if intent1 == "": continue # Si no han escrit res, no fem res
                
                if int(intent1) == res_correcte:
                    lcd.clear()
                    lcd.move_to(0, 0)
                    lcd.putstr("Well done P1!")  # Aquí se suma un punto al P1 y se resta uno al P2
                    
                    for i in range(10):
                        tira1[i] = (0, 255, 0)
                        tira2[i] = (255, 0, 0)
                        
                    tira1.write()
                    tira2.write()
                    esperar_ms(2000)
                    
                    p1 += 1
                    actualitzar_marcador_led()
                    
                    if comprovar_guanyador():
                        break
                    
    
                    
                else:
                    lcd.clear()
                    lcd.move_to(0, 0)
                    lcd.putstr("P1, incorrect!")
                    
                    for i in range(10):
                        tira1[i] = (255, 0, 0)
                        tira2[i] = (0, 255, 0)
                    tira1.write()
                    tira2.write()
                    esperar_ms(2000)
            
                    p2 += 1
                    actualitzar_marcador_led()
                    if comprovar_guanyador():
                        break
                
                esperar_ms(2000)
                break 
            
            elif tecla1 == "*": # Botó per esborrar i tornar a intentar
                if len(intent1) > 0:
                    # 1. Treiem l'últim caràcter del text
                    intent1 = intent1[:-1] 
                    
                    # 2. Netejem la línia on escriu el P1 (fila 1, columnes 3 a 7)
                    lcd.move_to(3, 1)
                    lcd.putstr("    ") # Quatre espais en blanc per "esborrar" el que hi havia
                    
                    # 3. Tornem a escriure el que queda de l'intent
                    lcd.move_to(3, 1)
                    lcd.putstr(intent1)
        
                    
        # Respuesta 2:    
        tecla2 = None
        if llegir_boto_p2():
            tecla2 = "#"
        else:
            tecla2 = llegir_tecla2()
        if tecla2:
            if tecla2.isdigit():
                intent2 += tecla2
                lcd.move_to(11, 1) 
                lcd.putstr(intent2) 
            
            elif tecla2 == "#": # Botó Enter
                if intent2 == "": continue # Si no han escrit res, no fem res
                
                if int(intent2) == res_correcte:
                    lcd.clear()
                    lcd.move_to(0, 0)
                    lcd.putstr("Well done P2!")  # Aquí se suma un punto al P2 y se resta uno al P1
                    
                    for i in range(10):
                        tira1[i] = (255, 0, 0)
                        tira2[i] = (0, 255, 0)
                    tira1.write()
                    tira2.write()
                  
                    esperar_ms(2000)
                    
                    p2 += 1
                    actualitzar_marcador_led()
                    if comprovar_guanyador():
                        break
                    
                else: 
                    lcd.clear() # Restar un punto al P2 y sumar uno al P1.
                    lcd.move_to(0, 0)
                    lcd.putstr("P2, incorrect!")
                    
                    for i in range(10):
                        tira1[i] = (0, 255, 0)
                        tira2[i] = (255, 0, 0)
                        
                    tira1.write()
                    tira2.write()
                   
                    esperar_ms(2000)
                    
                    p1 += 1
                    actualitzar_marcador_led()
                    if comprovar_guanyador():
                        break
                
                esperar_ms(2000)
                break 
            
            elif tecla2 == "*": # Botó per esborrar i tornar a intentar
                if len(intent2) > 0:
                    intent2 = intent2[:-1]
                    
                    # Netejem l'espai del P2 (columna 11 en endavant)
                    lcd.move_to(11, 1)
                    lcd.putstr("    ") 
                    
                    lcd.move_to(11, 1)
                    lcd.putstr(intent2)

        music_tick()
        time.sleep_ms(1)

compte_enrera()
music_on = True


# --- BUCLE PRINCIPAL ---
while True:
    joc_mates()