import pygame

class Animation:
    def __init__(self, milisPerFrame, nFrames):
        #self.sprites=sprites
        self.milisPerFrames = milisPerFrame
        self.nFrames=nFrames
        self.currentFrame = 0
        self.t0=pygame.time.get_ticks()
        self.t1=pygame.time.get_ticks()
        
        # Start delay allows to skip the update for
        # the first frame, in order to avoid 
        # premature skipping of it
        self.startDelay = True

    def reset(self):
        self.currentFrame=0
        self.startDelay=True

    #def initializeTimer(self):
    #    self.t0 = pygame.time.Clock().get_time() 
    #    self.t1 = pygame.time.Clock().get_time()

    def update(self):
        self.t1 = pygame.time.get_ticks()
        elapsed = self.t1-self.t0

        if(elapsed>=self.milisPerFrames):
            self.t0=pygame.time.get_ticks() # reset timer
            if(self.currentFrame==(self.nFrames-1)):
                self.currentFrame = 0
                self.startDelay = True
            else:
                if(not self.startDelay):
                    self.currentFrame+=1
                else:
                    self.startDelay = False

    def getCurrentFrame(self):
        return self.currentFrame
