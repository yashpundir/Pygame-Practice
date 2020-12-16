import pygame
pygame.init()

#set window
win = pygame.display.set_mode((852,480))
pygame.display.set_caption('Valorant')

#load all images
walkright = [pygame.image.load(f'hero images/R{x}.png') for x in range(1,10)]
walkleft = [pygame.image.load(f'hero images/L{x}.png') for x in range(1,10)]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('hero images/standing.png')

#load music & sound effects
bullet_sound = pygame.mixer.Sound('badass music/bullet.mp3')
hit_sound = pygame.mixer.Sound('badass music/hit.mp3')
bgmusic = pygame.mixer.music.load('badass music/Batman.mp3')
pygame.mixer.music.play(fade_ms=6000)  								#play the bgmusic

# clock
clock = pygame.time.Clock()

class Player():
	def __init__(self,x,y):
		self.x, self.y = x, y
		self.speed = 6
		self.is_jump , self.jump_count = False, 10
		self.left, self.right, self.walk_count = True, False, 0
		self.standing = True
		self.width = self.height = 64
		self.hitbox = (self.x + 10, self.y + 7, 40, 60)

	def draw(self,win):
		if self.walk_count+1 >= 27:
			self.walk_count = 0

		if not self.standing:
			if self.left:
				win.blit(walkleft[self.walk_count//3], (self.x,self.y))
				self.walk_count += 1
			elif yash.right:
				win.blit(walkright[self.walk_count//3], (self.x,self.y))
				self.walk_count += 1
		else:                                            # standing or jumping
			if self.right:
				win.blit(walkright[0], (self.x,self.y))
			else:
				win.blit(walkleft[0], (self.x,self.y))
		self.hitbox = (self.x + 10, self.y + 7, 40, 60)
		# pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

	def hit(self):
		self.x, self.y = 700, 405
		self.walk_count = 0
		hit_font = pygame.font.SysFont('comicsans',100)
		hit_text = hit_font.render('YOU GOT HIT!', 1, (255,0,0))
		win.blit(hit_text, (426-(hit_text.get_width()//2), 200))
		pygame.display.update()
		pygame.time.delay(1000)


class Enemy():
	walkLeft = [pygame.image.load(f"enemy images/L{x}E.png") for x in range(1,12)]
	walkRight = [pygame.image.load(f"enemy images/R{x}E.png") for x in range(1,12)]

	def __init__(self,x,y,dir=1):
		self.x, self.y = x, y
		self.width = self.height = 64
		# self.end = end
		self.walk_count = 0
		self.path = [0, 790]
		self.speed = dir*5
		self.hitbox = (self.x + 10, self.y, 50, 60)
		self.visible = True
		self.health = 10

	def draw(self,win):
		if self.visible:
			if self.walk_count + 1 >= 33:
				self.walk_count = 0

			if self.speed > 0:
				win.blit(self.walkRight[self.walk_count//3], (self.x, self.y))
				self.walk_count += 1
			else:
				win.blit(self.walkLeft[self.walk_count//3], (self.x, self.y))
				self.walk_count += 1
			
			pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.y - 10, 50, 8))
			pygame.draw.rect(win, (0,255,0), (self.hitbox[0], self.y - 10, 5*self.health, 8))
			self.hitbox = (self.x + 10, self.y, 50, 60)
			
		

	def move(self):
		if self.speed > 0:
			if self.x + self.speed < self.path[1]:
				self.x += self.speed
			else:
				self.speed *= -1
				self.walk_count = 0
		else:
			if self.x + self.speed > self.path[0]:
				self.x += self.speed
			else:
				self.speed *= -1
				self.walk_count = 0



class projectile():
	
	def __init__(self, hero):
		self.x, self.y = hero.x + hero.width//2, hero.y + hero.height//2
		self.color = 0,0,0
		self.radius = 5
		if hero.left:
			self.facing = -1
		else:
			self.facing = 1
		self.vel = 10 * self.facing 

	def draw(self,win):
		pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

	def hit(self):
		if joy.health > 1:
			joy.health -= 1
		else:
			joy.visible = False
		hit_sound.play()
		# print("BAMM NIGGA!!" )



def redrawwin(hero,enemiess):
	win.blit(bg,(0,0))
	text = font.render(f"SCORE : {score}", 1, (0,0,0))
	win.blit(text, (700,20))	
	hero.draw(win)
	for Enemy in enemiess:
		Enemy.move()
		Enemy.draw(win)
	for bullet in bullets:
		bullet.draw(win)
	pygame.display.update()


# Players initiated
yash = Player(700,405)
joy1 = Enemy(0,410,1)
joy2 = Enemy(400,410,1)
joy3 = Enemy(600,410,-1)
enemies = [joy1, joy2, joy3]

#Necessary variables
run=True
font = pygame.font.SysFont('comicsans', 30, True)
bullets = []
shoot_loop = 0
score = 0

#mainloop
while run:
	clock.tick(35)

	#if player is hit
	for joy in enemies:
		if joy.visible:                          # if enemy is alive, only then check for collisions	
			if (joy.hitbox[0] + joy.hitbox[2]) >= yash.hitbox[0] >= joy.hitbox[0]: 
				if (joy.hitbox[1] + joy.hitbox[3]) > yash.hitbox[1] >= joy.hitbox[1]:
					yash.hit()
					score -= 5
			


	# SHOOT COOLDOWN
	if shoot_loop > 0:
		shoot_loop+=1
	if shoot_loop > 4:
		shoot_loop = 0


	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			run = False

	# BULLET MOVEMENTS
	for joy in enemies:
		if joy.visible:
			for bullet in bullets:           #if bullet hits enemy
				if (joy.hitbox[0] + joy.hitbox[2]) > bullet.x > joy.hitbox[0]: 
					if (joy.hitbox[1] + joy.hitbox[3]) > bullet.y > joy.hitbox[1]:
						bullet.hit()
						score += 1
						bullets.remove(bullet)

	for bullet in bullets:
		if bullet.x > 0 and bullet.x < 850:
			bullet.x += bullet.vel
		else:
			bullets.remove(bullet)		


	# PLAYER MOVEMENTS/ACTIONS
	keys = pygame.key.get_pressed()
	
	if keys[pygame.K_SPACE] and shoot_loop==0:
		if len(bullets) < 3:
			bullets.append(projectile(yash))
			bullet_sound.play()
			shoot_loop = 1


	if keys[pygame.K_LEFT] and yash.x>=0:
		yash.x -= yash.speed
		yash.left, yash.right, yash.standing = True, False, False
	elif keys[pygame.K_RIGHT] and yash.x<=782:
		yash.x += yash.speed		
		yash.left, yash.right, yash.standing = False,True, False
	else:
		yash.standing = True
		walk_count = 0


	if not yash.is_jump:
		if keys[pygame.K_UP]:
			yash.is_jump = True

	else:
		if yash.jump_count >= -10:
			yash.y -= (yash.jump_count * abs(yash.jump_count)) * 0.5
			yash.jump_count -= 1
		else:
			yash.is_jump = False
			yash.jump_count = 10


	redrawwin(yash,enemies)

pygame.quit()