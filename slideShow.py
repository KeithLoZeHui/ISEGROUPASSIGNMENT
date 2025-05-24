import pygame
from colorConstants import *
from decimal import *

class Slide:
    def __init__(self, image, text, fadeInTime, stallTime, fadeOutTime):
        self.image = image # Image pixals displaed above text
        self.text = text # Text displayed below the image
        self.fadeInTime = fadeInTime 
        self.stallTime = stallTime
        self.fadeOutTime = fadeOutTime

class SlideShow:

    FADE_IN = 0
    STALL = 1
    FADE_OUT = 2
    MAX_TEXT_WIDTH_FACTOR = 0.7

    DEFAULT_TYPINGSPEED = 100
    DEFAULT_FADESPEED = 4

    LOCAL_SCALEFACTOR = 0.70

    def __init__(self, slides, font, screenRef):
        self.slideState = self.FADE_IN 
        self.slides = slides

        # Scale down the images
        for i in range(0, len(self.slides)):
            nImage = self.slides[i].image
            scaledImage = pygame.transform.scale_by(nImage, self.LOCAL_SCALEFACTOR)
            self.slides[i].image = scaledImage


        self.currentSlideID = 0
        self.slidet0 = 0#pygame.time.get_ticks()
        self.slideElapsed = 0
        self.alphaModulation = Decimal(0)
        self.finishedSlideShow = False
        self.font = font
        self.screenRef = screenRef

        self.currentTextWidth = 0
        self.typingSpeed = self.DEFAULT_TYPINGSPEED
        self.typingt0 = 0#pygame.time.get_ticks()
        self.typingElapsed = 0
        self.textRenderWidth = screenRef.get_width()*self.MAX_TEXT_WIDTH_FACTOR
        self.textYoffset = 0
        self.alreadyRenderedTextLines = []
        self.currentRenderTextLine = ""

        self.lineCharLength = int(self.textRenderWidth/font.size('X')[0])
        #print("N chars per line = ", self.lineCharLength)

        self.subTextInitialChar = 0
        self.currentSubTextChar = 0
        self.subTextLastChar = self.lineCharLength

    def advanceSlide(self):
        self.slideElapsed = 0
        self.slideState += 1 
        if(self.currentSlideID < len(self.slides)-1):
            self.currentSlideID += 1
        else:
            self.finishedSlideShow = True

    def update(self):
        if(self.slidet0!=0):
            self.slideElapsed = pygame.time.get_ticks() - self.slidet0
        else:
            self.slidet0 = pygame.time.get_ticks()
        #print(self.slideElapsed)
        currentSlide = self.slides[self.currentSlideID]
        if(self.slideState == self.FADE_IN):
            if(self.slideElapsed >= currentSlide.fadeInTime):
                self.slideElapsed=0
                self.slidet0 = pygame.time.get_ticks()
                self.slideState = self.STALL
            else:
                self.alphaModulation += self.DEFAULT_FADESPEED                
        elif(self.slideState == self.STALL):
            if(self.slideElapsed >= currentSlide.stallTime):
                self.slideElapsed=0
                self.slidet0 = pygame.time.get_ticks()
                self.slideState = self.FADE_OUT
            else:
                self.alphaModulation=Decimal(255)
                
                #print("len1",(self.currentSubTextChar-self.subTextInitialChar))
                #print("len2",len(currentSlide.text[self.textYoffset]))

                # Update text line Y 
                if(
                    # Render width exceeded:
                    (self.currentTextWidth <= self.textRenderWidth)    
                    # Line finished rendering:
                    and ((self.currentSubTextChar-self.subTextInitialChar)
                    < len(currentSlide.text[self.textYoffset]))
                ):
                    self.currentSubTextChar += 1
                else:
                    #print(self.textYoffset)
                    self.subTextInitialChar = 0 #+= self.lineCharLength 
                    self.subTextLastChar = 0#+= self.lineCharLength
                    if(len(currentSlide.text)-1 > self.textYoffset):
                        self.textYoffset+=1
                        self.alreadyRenderedTextLines.append(self.currentRenderTextLine)
                        self.currentTextWidth=0
                        self.currentSubTextChar = 0
                        self.currentRenderTextLine = ""

                # Update typing of each line
                if((self.currentSubTextChar-self.subTextInitialChar) < len(currentSlide.text)):    
                    self.typingElapsed = pygame.time.get_ticks() - self.typingt0 
                    if(self.typingElapsed >= self.typingSpeed):
                        self.typingElapsed=0
                        self.typingt0 = pygame.time.get_ticks()
        
        elif(self.slideState == self.FADE_OUT):
            if(self.slideElapsed >= currentSlide.fadeOutTime): 
                self.advanceSlide()
                self.slideElapsed=0
                self.alphaModulation = Decimal(0) # Reset alpha modulation
                self.slidet0 = pygame.time.get_ticks()
                self.typingElapsed
                self.subTextInitialChar = 0
                self.currentSubTextChar = 0
                self.subTextLastChar = self.lineCharLength
                self.slideState = self.FADE_IN
                self.alreadyRenderedTextLines = []
                self.textYoffset = 0
            else:
                self.alphaModulation -= self.DEFAULT_FADESPEED
    def renderImage(self, screen):
        #self.slides[self.currentSlideID].image.set_alpha(Decimal(self.alphaModulation))
        slideImg = self.slides[self.currentSlideID].image
        slideImg.set_alpha(Decimal(self.alphaModulation))
        scaledSlideImg = pygame.transform.scale_by(slideImg, self.LOCAL_SCALEFACTOR);
        
        screen.blit(
            #self.slides[self.currentSlideID].image, 
            #scaledSlideImg,
            slideImg,
            (
                (screen.get_width()/2)
                - (slideImg.get_width()/2)#(scaledSlideImg.get_width()/2)
                #- (self.slides[self.currentSlideID].image.get_width()/2)
                , 
                20
            )
        )

    def renderText(self, screen):

        #textRenderWidth = screen.get_width()*self.MAX_TEXT_WIDTH_FACTOR
        currentSlide = self.slides[self.currentSlideID] 

        textSubset = ""
        fullText = currentSlide.text[self.textYoffset]

        #c = 0
        #while c < self.currentTextLength:
        for i in range(self.subTextInitialChar, self.currentSubTextChar):
            if(i<= len(fullText)-1): #and i<= self.subTextLastChar):#len(fullText)-1):
                textSubset += fullText[i]
            #print(fullText[i])
        self.currentRenderTextLine = textSubset

        currentTextRendered = self.font.render(self.currentRenderTextLine, False, WHITE)
        currentTextRendered.set_alpha(Decimal(self.alphaModulation))
        self.currentTextWidth = currentTextRendered.get_width() 

        # If all the lines were rendered, do not keep rendering the last line
        #if(self.textYoffset < len(self.slides[self.currentSlideID].text)):    
        screen.blit(
            currentTextRendered, 
            (
                (screen.get_width()/2) 
                - (currentTextRendered.get_width()/2)#(self.textRenderWidth/2)
                , 
                20 +
                (currentSlide.image.get_height())
                + 30
                + (self.textYoffset*currentTextRendered.get_height())
            )
        )
        
        for i in range(0, len(self.alreadyRenderedTextLines)):
            previousTextRendered = self.font.render(self.alreadyRenderedTextLines[i], False, WHITE) 
            previousTextRendered.set_alpha(Decimal(self.alphaModulation))

            screen.blit(
                previousTextRendered, 
                (
                    (screen.get_width()/2) 
                    - (previousTextRendered.get_width()/2)#(self.textRenderWidth/2)
                    , 
                    20 +
                    (currentSlide.image.get_height())
                    + 30
                    + (i*currentTextRendered.get_height())
                )
            )

        '''
        # DEBUG
        pygame.draw.rect(screen, YELLOW, pygame.rect.Rect(
                (screen.get_width()/2) 
                - (self.textRenderWidth/2),
                20 + (currentSlide.image.get_height())
                + 30
                + (self.textYoffset*currentTextRendered.get_height()),
                self.currentTextWidth,
                currentTextRendered.get_height(),
        ), 2)
        '''

    def render(self, screen, font):
        screen.fill(BLACK)
        
        if(self.slideState == self.FADE_IN):
            self.renderImage(screen)
        elif(self.slideState == self.STALL):
            self.renderImage(screen)
            self.renderText(screen)
        elif(self.slideState == self.FADE_OUT):
            self.renderImage(screen)
            self.renderText(screen)
        pygame.display.flip()


