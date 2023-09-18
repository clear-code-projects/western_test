import pygame
from pygame.math import Vector2 as vector
from os import walk
from math import sin
from support import import_sub_folders

class Entity(pygame.sprite.Sprite):
	def __init__(self, pos, groups, path, collision_sprites):
		super().__init__(groups)

		self.frames = import_sub_folders(*path)
		self.frame_index = 0
		self.status = 'down'

		self.frames = import_sub_folders(*path)
		self.image = self.frames[self.status][self.frame_index]
		self.rect = self.image.get_frect(center = pos)

		# float based movement
		self.pos = vector(self.rect.center)
		self.direction = vector()
		self.speed = 180

		# collisions
		self.hitbox = self.rect.inflate(-self.rect.width / 2,-self.rect.height / 2)
		self.collision_sprites = collision_sprites
		self.mask = pygame.mask.from_surface(self.image)

		# attack 
		self.attacking = False

		# health
		self.health = 3
		self.is_vulnerable = True
		self.hit_time = None

		# sound 
		# self.hit_sound = pygame.mixer.Sound('../sound/hit.mp3')
		# self.hit_sound.set_volume(0.1)
		# self.shoot_sound = pygame.mixer.Sound('../sound/bullet.wav')
		# self.shoot_sound.set_volume(0.2)

	def blink(self):
		if not self.is_vulnerable:
			if self.wave_value():
				mask = pygame.mask.from_surface(self.image)
				white_surf = mask.to_surface()
				white_surf.set_colorkey((0,0,0))
				self.image = white_surf

	def wave_value(self):
		value = sin(pygame.time.get_ticks())
		if value >= 0:
			return True
		else:
			return False

	def damage(self):
		if self.is_vulnerable:
			self.health -= 1
			self.is_vulnerable = False
			self.hit_time = pygame.time.get_ticks()
			self.hit_sound.play()

	def vulnerability_timer(self):
		if not self.is_vulnerable:
			current_time = pygame.time.get_ticks()
			if current_time - self.hit_time > 400:
				self.is_vulnerable = True	

	def move(self,dt):

		# horizontal
		self.rect.centerx += self.direction.x * self.speed * dt
		self.hitbox.centerx = self.rect.centerx
		self.collision('horizontal')

		# vertical movement
		self.rect.centery += self.direction.y * self.speed * dt
		self.hitbox.centery = self.rect.centery
		self.collision('vertical')

	def collision(self,direction):
		for sprite in self.collision_sprites.sprites():
			if sprite.hitbox.colliderect(self.hitbox):
				if direction == 'horizontal':
					if self.direction.x > 0: # moving right 
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0: # moving left
						self.hitbox.left = sprite.hitbox.right
					self.rect.centerx = self.hitbox.centerx

				else: # vertical
					if self.direction.y > 0: # moving down
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom
					self.rect.centery = self.hitbox.centery