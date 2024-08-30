import pygame

class Button:
    def __init__(self, x, y, width, height, id, text="", action=None):
        self.id = id
        self.rect = pygame.Rect(x, y, width, height)
        self.colour = (120, 120, 120)
        self.hoverColour = (20, 20, 20)
        self.clickColour = (200, 120, 120)
        self.currentColour = self.colour
        self.text = text
        self.textColour = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 30)
        self.clicked = False
        self.action = action
    
    def draw(self, screen):
        # Draw the button with the current color
        pygame.draw.rect(screen, self.currentColour, self.rect)
        
        # Draw the text
        if self.text:
            text = self.font.render(self.text, True, self.textColour)
            textRect = text.get_rect(center=self.rect.center)
            screen.blit(text, textRect)
    
    def update(self, mouseClick, currentButton):
        mousePos = pygame.mouse.get_pos()
        # Check if the mouse is over the button
        if self.rect.collidepoint(mousePos):
            self.currentColour = self.hoverColour
            if mouseClick:
                self.currentColour = self.clickColour
                self.clicked = True
            else:
                self.clicked = False
        elif currentButton == self.id:
            self.currentColour = self.clickColour
        else:
            self.currentColour = self.colour
            self.clicked = False

    def is_clicked(self):
        return self.clicked
    
    def get_action(self):
        return self.action
