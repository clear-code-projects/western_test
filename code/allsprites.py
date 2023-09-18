from settings import *

class AllSprites(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.offset = vector()
		self.display_surface = pygame.display.get_surface()
		self.bg = pygame.image.load(join('..', 'graphics', 'other','bg.png' )).convert()

	def custom_draw(self, target_pos):

		# change the offset vector
		self.offset.x = -int(target_pos[0] - WINDOW_WIDTH / 2)
		self.offset.y = -int(target_pos[1] - WINDOW_HEIGHT / 2)
	
		# floor 
		self.display_surface.blit(self.bg, self.offset)

		# sprites
		for sprite in sorted(self, key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft + self.offset
			self.display_surface.blit(sprite.image,offset_pos)