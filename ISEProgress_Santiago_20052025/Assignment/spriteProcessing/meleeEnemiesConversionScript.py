from spriteConvertor import *

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

DEFAULT_COLORS_8BITS_RUN = [
    (25, 33, 58, 255),
    (9, 18, 71, 255),
    (31, 77, 149, 255),
    (5, 5, 11, 255)
]

DEFAULT_COLORS_CONVERTED = [
    RGBAtoBGRA(c)
    for c in DEFAULT_COLORS_8BITS
]

DEFAULT_COLORS_RUN_CONVERTED = [
    RGBAtoBGRA(c)
    for c in DEFAULT_COLORS_8BITS_RUN
]

# Tier 2 color
orangeC2 = (145, 60, 21, 255) #(18506, 11566, 2326) #, 65535)
orangeC2_BGRA = RGBAtoBGRA(orangeC2)

# Tier 3 color
redC2 = (109, 0, 0, 255)
redC2_BGRA = RGBAtoBGRA(redC2)

# Tier 4 color
purpleC2 = (91, 0, 109, 255)
purpleC2_BGRA = RGBAtoBGRA(purpleC2)

IMAGE_FORMAT = ".png"

IMAGENAMES = [
    "IdleRight", "IdleLeft",
    "WalkRight", "WalkLeft",
    "RunRight", "RunLeft",
    "BlockRight", "BlockLeft",
    "HurtRight", "HurtLeft",
    "DeadRight", "DeadLeft",
    "Attack1Right", "Attack1Left",
    "Attack2Right", "Attack2Left",
    "Attack3Right", "Attack3Left" 
]

INPUTDIRECTORY = os.path.join("Tier1", "Melee")

def generateMeleeTier2():

    outputDirectory = os.path.join("Tier2", "Melee")

    for inputImgName in IMAGENAMES:
        
        inputImageLocation = os.path.join(INPUTDIRECTORY, inputImgName+IMAGE_FORMAT)
        print("Input image location = ", inputImageLocation)

        outputImgLocation = os.path.join(outputDirectory, inputImgName+"Modified"+IMAGE_FORMAT)
        print("Output image location = ", outputImgLocation)

        if("RunLeft" == inputImgName or "RunRight" == inputImgName):
            convertMeleeEnemyColors(inputImageLocation, DEFAULT_COLORS_RUN_CONVERTED, orangeC2_BGRA, outputImgLocation)
        else:
            convertMeleeEnemyColors(inputImageLocation, DEFAULT_COLORS_CONVERTED, orangeC2_BGRA, outputImgLocation)

def generateMeleeTier3():
    outputDirectory = os.path.join("Tier3", "Melee")

    for inputImgName in IMAGENAMES:
        
        inputImageLocation = os.path.join(INPUTDIRECTORY, inputImgName+IMAGE_FORMAT)
        print("Input image location = ", inputImageLocation)

        outputImgLocation = os.path.join(outputDirectory, inputImgName+"Modified"+IMAGE_FORMAT)
        print("Output image location = ", outputImgLocation)

        if("RunLeft" == inputImgName or "RunRight" == inputImgName):
            convertMeleeEnemyColors(inputImageLocation, DEFAULT_COLORS_RUN_CONVERTED, redC2_BGRA, outputImgLocation)
        else:
            convertMeleeEnemyColors(inputImageLocation, DEFAULT_COLORS_CONVERTED, redC2_BGRA, outputImgLocation)

def generateMeleeTier4():
    outputDirectory = os.path.join("Tier4", "Melee")

    for inputImgName in IMAGENAMES:
        
        inputImageLocation = os.path.join(INPUTDIRECTORY, inputImgName+IMAGE_FORMAT)
        print("Input image location = ", inputImageLocation)

        outputImgLocation = os.path.join(outputDirectory, inputImgName+"Modified"+IMAGE_FORMAT)
        print("Output image location = ", outputImgLocation)

        if("RunLeft" == inputImgName or "RunRight" == inputImgName):
            convertMeleeEnemyColors(inputImageLocation, DEFAULT_COLORS_RUN_CONVERTED, purpleC2_BGRA, outputImgLocation)
        else:   
            convertMeleeEnemyColors(inputImageLocation, DEFAULT_COLORS_CONVERTED, purpleC2_BGRA, outputImgLocation)
    
generateMeleeTier2()
generateMeleeTier3()
generateMeleeTier4()