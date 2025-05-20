import cv2
import numpy as np
import pygame
import sys
import os

SCRW = 1760
SCRH = 990

# Initialize pygame
#pygame.init()
#screen = pygame.display.set_mode((SCRW, SCRH))
#pygame.display.set_caption("Sprite convertor")

'''
DEFAULT_COLORS_16BITS = [
    [8627, 10240, 15143, 65535],   # C1
    [4456, 7175, 18236, 65535],    # C2
    [9824, 19927, 38280, 65535],   # C3
    [2842, 2458, 4996, 65535]      # C4
]

    
DEFAULT_COLORS_8BITS = [
    (34, 40, 59, 255),
    (17, 28, 71, 255),
    (38, 78, 149, 255),
    (11, 10, 19, 255)
]

orangeC2 = (145, 60, 21, 255) #(18506, 11566, 2326) #, 65535)
'''

MAX16BITVAL = 65535
MAX8BITVAL = 255

def normalizeTo8bitChannels(color):
    return ([
        int((color[0]/MAX16BITVAL)*MAX8BITVAL),
        int((color[1]/MAX16BITVAL)*MAX8BITVAL),
        int((color[2]/MAX16BITVAL)*MAX8BITVAL)
        #int((color[3]/MAX16BITVAL)*MAX8BITVAL)
    ])

def RGBAtoBGRA(rgba):
    #bgr = rgb[::-1]
        
    bgra = []
    for c in range(2, -1, -1):
        bgra.append(rgba[c])
    bgra.append(rgba[3])

    return bgra

'''
DEFAULT_COLORS_CONVERTED = [
    RGBAtoBGRA(c)
    for c in DEFAULT_COLORS_8BITS
]

#print(DEFAULT_COLORS_CONVERTED)
orangeC2_converted = RGBAtoBGRA(orangeC2)
'''

def compareColors(tupleA, tupleB) -> bool:
        return ([
            tupleA[0]==tupleB[0] and
            tupleA[1]==tupleB[1] and
            tupleA[2]==tupleB[2] 
            and tupleA[3]==tupleB[3]
        ])

def calculateColorDiff(tupleA, tupleB):

    r = tupleA[0]-tupleB[0]
    g = tupleA[1]-tupleB[1]
    b = tupleA[2]-tupleB[2]
    a = 255

    return ([
        r if r>=0 else 0,
        g if g>=0 else 0,
        b if b>=0 else 0,
        255 #tupleA[3]-tupleB[3],
    ])

def calculateColorSum(tupleA, tupleB):
    r = tupleA[0]+tupleB[0]
    g = tupleA[1]+tupleB[1]
    b = tupleA[2]+tupleB[2]
    a = 255

    return ([
        r if r>=0 else 0,
        g if g>=0 else 0,
        b if b>=0 else 0,
        255 #tupleA[3]-tupleB[3],
    ])

def convertMeleeEnemyColors(filePath, defaultColors, newC2color, newFilePath):

    # Load an image
    #image = pygame.image.load('IdleRight.png') #.convert()
    image = cv2.imread(filePath, cv2.IMREAD_UNCHANGED)


    hueDiff = calculateColorDiff(defaultColors[1],defaultColors[0])
    hueDiff[3] = 255 # Force alpha
    #calculateColorDiff(orangeC2_converted, DEFAULT_COLORS_CONVERTED[1]);
    print(hueDiff)

    newC1color = calculateColorDiff(newC2color, hueDiff)
    #calculateColorDiff(DEFAULT_COLORS_CONVERTED[1],DEFAULT_COLORS_CONVERTED[0]))
    newC3color = calculateColorSum(newC2color, hueDiff)
    newC4color = calculateColorSum(newC3color, hueDiff)

    #targetColor = DEFAULT_COLORS_CONVERTED[1]
    #replaceColor = orangeC2_converted

    maskC1 = np.all(image == defaultColors[0], axis=-1)
    maskC2 = np.all(image == defaultColors[1], axis=-1)
    maskC3 = np.all(image == defaultColors[2], axis=-1)
    maskC4 = np.all(image == defaultColors[3], axis=-1)

    #print(image)

    image[maskC1] = newC1color
    image[maskC2] = newC2color
    image[maskC3] = newC3color
    image[maskC4] = newC4color

    cv2.imwrite(newFilePath, image)

#convertMeleeEnemyColors("IdleRight.png", DEFAULT_COLORS_CONVERTED, orangeC2_converted, "IdleRightModified.png")

# Quit Pygame
#pygame.quit()
#sys.exit()