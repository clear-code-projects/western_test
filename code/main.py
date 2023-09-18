from settings import  *
from pytmx.util_pygame import load_pygame
from allsprites import AllSprites

from player import Player
from sprite import Sprite, Bullet
# from monster import Coffin, Cactus

class Game:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.clock = pygame.time.Clock()
		self.bullet_surf = pygame.image.load(join('..', 'graphics', 'other', 'particle.png')).convert_alpha()

		self.all_sprites = AllSprites()
		self.obstacles = pygame.sprite.Group()
		self.bullets = pygame.sprite.Group()
		self.monsters = pygame.sprite.Group()

		self.setup()

	def setup(self):
		tmx_map = load_pygame(join('..', 'data', 'map.tmx'))
		
		# tiles
		for x, y, surf in tmx_map.get_layer_by_name('Fence').tiles():
			Sprite((x * 64, y * 64),surf,[self.all_sprites, self.obstacles])

		# # objects
		for obj in tmx_map.get_layer_by_name('Objects'):
			Sprite((obj.x, obj.y),obj.image,[self.all_sprites, self.obstacles])

		for obj in tmx_map.get_layer_by_name('Entities'):
			if obj.name == 'Player':
				self.player = Player(
					pos = (obj.x, obj.y), 
					groups = self.all_sprites, 
					path = ('..','graphics', 'player'), 
					collision_sprites = self.obstacles,
					create_bullet = self.create_bullet
					)

			# if obj.name == 'Coffin':
			# 	Coffin((obj.x,obj.y), [self.all_sprites, self.monsters], 'coffin', self.obstacles, self.player)

			# if obj.name == 'Cactus':
			# 	Cactus((obj.x, obj.y), [self.all_sprites, self.monsters], 'cactus', self.obstacles, self.player,self.create_bullet)

	def create_bullet(self, pos, direction):
		Bullet(pos, direction, self.bullet_surf, [self.all_sprites,self.bullets])

	def run(self):
		while True:
			dt = self.clock.tick() / 1000
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()

			# update
			self.display_surface.fill('black')
			self.all_sprites.update(dt)
			# self.bullet_collision()

			# draw
			self.all_sprites.custom_draw(self.player.rect.center)

			pygame.display.update()


if __name__ == '__main__':
	game = Game()
	game.run()