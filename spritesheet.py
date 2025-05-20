import pygame

# Loads a set of sprites/frames from an image
def getSpritesheetAsSpriteArr(
    file, sprWidth, sprHeight, 
    sheetWidth, sheetHeight):
    
    sprtRectX=0
    sprtRectY=0 

    # Number of sprites in horizontal axis (X)
    nHorSprites = sheetWidth/sprWidth
    # Number of sprite in vertical axis (Y)
    nVerSprites = sheetHeight/sprHeight

    # First load the image data
    sheet = pygame.image.load(file).convert_alpha()

    sprites = []
    for i in range(0, int(nVerSprites)):
        for j in range(0, int(nHorSprites)):
            # Set the sprite clip rectangle
            sheet.set_clip(
                pygame.Rect(sprtRectX, sprtRectY, 
                float(sprWidth), float(sprHeight)))
            # Extract the subsurface using the clip
            # and add it to the frame array
            sprites.append(sheet.subsurface(sheet.get_clip()))

            sprtRectX+=sprWidth
        sprtRectX=0
        sprtRectY+=sprHeight
    return sprites

# Extract a stripe of frames horizontally from a sprite/frame array
def extractAnimationFromSpriteArr(spriteArr, nCols, row, x1, x2):
    extractedFrames = []
    for i in range(x1,x2+1):
        extractedFrames.append(spriteArr[i+(row*nCols)])
    return extractedFrames



    