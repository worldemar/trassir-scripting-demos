import time
import random

ROTATION_SYSTEMS = {
	"SRS" : [
		[
		"0000", "0010", "0000", "0100",
		"1111", "0010", "0000", "0100",
		"0000", "0010", "1111", "0100",
		"0000", "0010", "0000", "0100"
		],
		[
		"100", "011", "000", "010",
		"111", "010", "111", "010",
		"000", "010", "001", "110"  
		],
		[
		"001", "010", "000", "110",
		"111", "010", "111", "010",
		"000", "011", "100", "010"  
		],
		[
		"11", "11", "11", "11",
		"11", "11", "11", "11",
		],
		[
		"011", "010", "000", "100",
		"110", "011", "011", "110",
		"000", "001", "110", "010"  
		],
		[
		"010", "010", "000", "010",
		"111", "011", "111", "110",
		"000", "010", "010", "010"  
		],
		[
		"110", "001", "000", "010",
		"011", "011", "110", "110",
		"000", "010", "011", "100"  
		]
	]
}

class TextScreen:
	def __init__(self, width = 80, height = 25, colors = [" ", "░", "▒", "▓", "█"], scalex = 1, scaley = 1):
		self.width = width
		self.height = height
		self.colors = colors
		self.scalex = scalex
		self.scaley = scaley
		self.clear(0)

	def blit(self):
		f = ""
		sxb = (self.scalex - 1) / 2
		sxa = self.scalex - 1 - sxb
		syb = (self.scaley- 1) / 2
		sya = self.scaley - 1 - syb
		for y in xrange(0, self.height):
			lineg = ""
			linet = ""
			for x in xrange(0, self.width):
				if self.frame[y][x] in self.colors:
					lineg += self.frame[y][x] * self.scalex
					linet += self.frame[y][x] * self.scalex
				else:
					lineg += " " * self.scalex
					linet += " " * sxb + self.frame[y][x] + " " * sxa
			lineg += "\n"
			linet += "\n"
			f += lineg * syb
			f += linet
			f += lineg * sya
		text_add("fdt6vb3G", f, 0, 0, 100, 100, self.width * self.scalex, "FFFFFF")

	def bloom(self, x1, y1, x2, y2):
		ret = False
		for y in xrange(y1, y2 + 1):
			for x in xrange(x1, x2 + 1):
				if self.frame[y][x] == self.colors[-1]:
					continue
				try:
					cc = self.colors.index(self.frame[y][x])
					self.frame[y][x] = self.colors[cc + 1]
				except:
					self.frame[y][x] = self.colors[1]
				ret = True
		return ret

	def fade(self, x1, y1, x2, y2):
		ret = False
		for y in xrange(y1, y2 + 1):
			for x in xrange(x1, x2 + 1):
				if self.frame[y][x] == self.colors[0]:
					continue
				try:
					cc = self.colors.index(self.frame[y][x])
					self.frame[y][x] = self.colors[cc - 1]
				except:
					self.frame[y][x] = self.colors[1]
				ret = True
		return ret

	def clear(self, c):
		self.frame = [[self.colors[c] for x in xrange(self.width)] for y in xrange(self.height)]

	def draw_pixel(self, x, y, c):
		if x < 0 or x >= self.width:
			return
		if y < 0 or y >= self.height:
			return
		self.frame[y][x] = self.colors[c]

	def draw_rect_fill(self, x1, y1, x2, y2, c):
		for x in xrange(x1, x2 + 1):
			for y in xrange(y1, y2 + 1):
				self.draw_pixel(x, y, c)

	def draw_rect(self, x1, y1, x2, y2, c):
		for x in xrange(x1, x2 + 1):
			for y in xrange(y1, y2 + 1, 1 if x == x1 or x == x2 else (y2-y1)):
				self.draw_pixel(x, y, c)

	def draw_text(self, x1, y1, x2, y2, t):
		tx = (x2 + x1) / 2 - len(t) / 2
		ty = (y2 + y1) / 2
		for i in xrange(len(t)):
			self.frame[ty][tx + i] = t[i]

class TetrisPiece:
	def __init__(self, data):
		self.frame = 0
		self.frames = [[] for f in xrange(4)]
		for s in xrange(len(data[0])):
			for f in xrange(4):
				self.frames[f].append(data[s * 4 + f])

	def rotate_left(self):
		self.frame -= 1
		if self.frame < 0:
			self.frame = len(self.frames) - 1

	def rotate_right(self):
		self.frame += 1
		if self.frame > len(self.frames) - 1:
			self.frame = 0 

	def draw(self, x1, y1):
		for x in xrange(len(self.frames[self.frame][0])):
			for y in xrange(len(self.frames[self.frame][0])):
				if self.frames[self.frame][y][x] == "1":
					screen.draw_pixel(x1 + x, y1 + y, 4)

	def get(self):
		return self.frames[self.frame]

class TetrisWell:
	def __init__(self):
		self.width = well_width
		self.height = well_height
		self.clear()

	def clear(self):
		self.well = [["0" for x in xrange(self.width)] for y in xrange(self.height)]

	def piece_collide(self, x1, y1, piece):
		data = piece.get()
		for x in xrange(0, len(data[0])):
			for y in xrange(0, len(data[0])):
				if data[y][x] == "1":
					if (y1 + y) < 0 or (y1 + y) >= self.height:
						return True
					if (x1 + x) < 0 or (x1 + x) >= self.width:
						return True
					if self.well[y1 + y][x1 + x] == "1":
						return True

	def piece_place(self, x1, y1, piece):
		data = piece.get()
		for x in xrange(0, len(data[0])):
			for y in xrange(0, len(data[0])):
				if data[y][x] == "1":
					self.well[y1 + y][x1 + x] = "1"

	def count_full_lines(self):
		ret = 0
		for y in xrange(self.height):
			if self.well[y] == ["1"] * self.width:
				ret += 1
		return ret

	def draw(self):
		screen.draw_rect_fill(well_x, well_y, well_x + self.width + 1, well_y + self.height + 1, 3)
		screen.draw_rect_fill(well_x + 1, well_y, well_x + self.width, well_y + self.height, 0)
		for x in xrange(self.width):
			for y in xrange(self.height):
				#screen.draw_pixel(x1 + 1 + y % 10, y1 + 1 + y, 4)
				if self.well[y][x] != "0":
					screen.draw_pixel(well_x + 1 + x, well_y + 1 + y, 4)

	def drown(self):
		for y in xrange(self.height, -1, -1):
			if screen.bloom(well_x + 1, well_y + y, well_x + self.width, well_y + y):
				return False
		return True

	def fade(self):
		if screen.fade(well_x + 1, well_y, well_x + self.width, well_y + self.height):
			return False
		return True

	def full_lines_fade(self):
		ret = True
		for y in xrange(self.height):
			if self.well[y] == ["1"] * self.width:
				if screen.fade(well_x + 1, well_y + 1 + y, well_x + self.width, well_y + 1 + y):
					ret = False
		return ret

	def drop_down(self):
		scoreadd = 0
		new_well = []
		for y in xrange(self.height):
			if self.well[y] == ["1"] * self.width:
				new_well = [["0"] * self.width] + new_well
				scoreadd += 1
			else:
				new_well.append(self.well[y])
		self.well = new_well
		return scoreadd

	def bloom(self):
		if screen.bloom(well_x + 1, well_y, well_x + self.width, well_y + self.height):
			return False
		return True

# screen

scale_x = 3
scale_y = 2
well_x = 5
well_y = 2
well_width = 10
well_height = 20
screen_width = 45
screen_height = 25
screen = TextScreen(width = screen_width, height = screen_height, scalex = scale_x, scaley = scale_y)
well = TetrisWell()

# player controls queue

buttons = []

def key_left():
	global buttons
	buttons.append("L")

def key_right():
	global buttons
	buttons.append("R")

def key_up():
	global buttons
	buttons.append("U")

def key_down():
	global buttons
	buttons.append("D")

activate_on_shortcut("F5", key_left)
activate_on_shortcut("F6", key_down)
activate_on_shortcut("F7", key_up)
activate_on_shortcut("F8", key_right)

# drawing helper functions

def draw_score():
	global screen
	global score
	global well_x
	global well_y
	screen.draw_text(well_x + 13, well_y + 4, well_x + 30, well_y + 4, "  SCORE: %08d" % score)

def draw_statistics():
	global screen
	global statistics
	global well_x
	global well_y
	for i in statistics.keys():
		screen.draw_text(well_x + 13, well_y + 4 + i, well_x + 25, well_y + 4 + i, "%d-LINES: %03d" % (i, statistics[i]))


# transitions and animations

transitions = []

def transition_next():
	global transitions
	global buttons
	if len(transitions) > 0:
		nextfunc = transitions[0]
		transitions = transitions[1:]
		if transitions == []:
			buttons = []
		timeout(1, nextfunc)

def transition_welldrown():
	if not well.drown():
		screen.blit()
		timeout(1, transition_welldrown)
		return
	transition_next()

def transition_wellfade():
	if not well.fade():
		screen.blit()
		timeout(1, transition_wellfade)
		return
	transition_next()

def transition_wellfadelines():
	global statistics
	global score
	if not well.full_lines_fade():
		screen.blit()
		timeout(1, transition_wellfadelines)
		return
	scr = well.drop_down()
	if scr in statistics.keys():
		statistics[scr] += 1
	score += scr * scr
	transition_next()

def transition_wellbloom():
	if not well.bloom():
		screen.blit()
		timeout(1, transition_wellbloom)
		return
	transition_next()

# play screen

piece_next = None
piece = None
piece_last_gravity = 0
piece_x = 0
piece_y = 0
statistics = {1: 0, 2: 0, 3: 0, 4: 0}
score = 0

def play():
	global screen
	global well
	global buttons
	global piece
	global piece_next
	global piece_x
	global piece_y
	global piece_last_gravity

	now = time.time()

	if piece_next is None:
		piece_next = TetrisPiece(random.choice(ROTATION_SYSTEMS["SRS"]))
		timeout(0, play)
		return

	if piece is None:
		piece = piece_next
		piece_next = None
		piece_x = 3
		piece_y = -1
		piece_last_gravity = now
		timeout(0, play)
		return

	for b in buttons:
		if b == "L":
			if not well.piece_collide(piece_x - 1, piece_y, piece):
				piece_x -= 1
		elif b == "R":
			if not well.piece_collide(piece_x + 1, piece_y, piece):
				piece_x += 1
		elif b == "U":
			piece.rotate_right()
			if well.piece_collide(piece_x, piece_y, piece):
				piece.rotate_left()
		elif b == "D":
			if not well.piece_collide(piece_x, piece_y + 1, piece):
				piece_y += 1
	buttons = []

	if piece_last_gravity + 0.5 < now:
		if well.piece_collide(piece_x, piece_y + 1, piece):
			if piece_y == -1:
				well = TetrisWell()
				piece = None
				transitions.append(transition_welldrown)
				transitions.append(transition_wellfade)
				transitions.append(gameover)
				transition_next()
				return
			well.piece_place(piece_x, piece_y, piece)
			piece = None
			lines = well.count_full_lines()
			if lines > 0:
				transitions.append(transition_wellfadelines)
				transitions.append(play)
				transition_next()
				return
			timeout(0, play)
			return
		else:
			piece_y += 1
			piece_last_gravity = now
			timeout(0, play)
			return

	screen.clear(0)
	well.draw()
	piece.draw(well_x + piece_x + 1, well_y + piece_y + 1)
	screen.draw_text(well_x + 13, well_y, well_x + 20, well_y, "NEXT")
	piece_next.draw(well_x + 13, well_y + 1)
	draw_score()
	draw_statistics()
	screen.blit()
	timeout(0, play)

# game over

def gameover():
	global screen
	global well
	global buttons
	global score
	global statistics

	now = time.time()

	for b in buttons:
		if b in "LRUD":
			transitions.append(transition_wellfade)
			transitions.append(menu)
			transition_next()
			return

	buttons = []

	screen.clear(0)
	well.draw()

	go_y = well_y + (well_height - 1) / 2
	screen.draw_text(well_x, go_y + 0, well_x + well_width + 2, go_y + 0, "GAME")
	screen.draw_text(well_x, go_y + 1, well_x + well_width + 2, go_y + 1, "OVER")

	screen.draw_text(well_x, go_y + 3, well_x + well_width + 2, go_y + 3, "SCORE:")
	screen.draw_text(well_x, go_y + 4, well_x + well_width + 2, go_y + 4, "%08d" % score)

	if int(now) % 2 == 1:
		screen.draw_text(well_x, well_y + well_height - 4, well_x + well_width + 2, well_y + well_height - 4, "ANY BUTTON")
		screen.draw_text(well_x, well_y + well_height - 3, well_x + well_width + 2, well_y + well_height - 3, "TO")
		screen.draw_text(well_x, well_y + well_height - 2, well_x + well_width + 2, well_y + well_height - 2, "CONTINUE")

	draw_score()
	draw_statistics()

	screen.blit()
	timeout(0, gameover)

# main menu

def game_start():
	global score
	global statistics
	score = 0
	statistics = {1: 0, 2: 0, 3: 0, 4: 0}
	screen.clear(0)
	well.draw()
	screen.blit()
	transitions.append(transition_wellbloom)
	transitions.append(transition_wellfade)
	transitions.append(play)
	transition_next()

def menu_item_wellx():
	global well_x
	return "X:  %02d" % well_x

def menu_item_wellx_more():
	global well_x
	well_x += 1
	if well_x > 15:
		well_x = 15
	timeout(0, menu)

def menu_item_wellx_less():
	global well_x
	well_x -= 1
	if well_x < 0:
		well_x = 0
	timeout(0, menu)

def menu_item_welly():
	global well_y
	return "Y:  %02d" % well_y

def menu_item_welly_more():
	global well_y
	well_y += 1
	if well_y > 10:
		well_y = 10
	timeout(0, menu)

def menu_item_welly_less():
	global well_y
	well_y -= 1
	if well_y < 1:
		well_y = 1
	timeout(0, menu)

def menu_item_sh():
	global screen_height
	return "H:  %02d" % screen_height

def menu_item_sh_more():
	global screen_height
	screen_height += 1
	if screen_height > 40:
		screen_height = 40
	timeout(0, menu)

def menu_item_sh_less():
	global screen_height
	screen_height -= 1
	if screen_height < 20:
		screen_height = 20
	timeout(0, menu)

def menu_item_sw():
	global screen_width
	return "W: %03d" % screen_width

def menu_item_sw_more():
	global screen_width
	screen_width += 1
	if screen_width > 999:
		screen_width = 999
	timeout(0, menu)

def menu_item_sw_less():
	global screen_width
	screen_width -= 1
	if screen_width < 15:
		screen_width = 15
	timeout(0, menu)

menu_current_item = 0

menu_items = [
{"name": lambda: "START ", "L": None,                 "R": game_start },
{"name": menu_item_wellx,  "L": menu_item_wellx_less, "R": menu_item_wellx_more },
{"name": menu_item_welly,  "L": menu_item_welly_less, "R": menu_item_welly_more },
{"name": menu_item_sw,     "L": menu_item_sw_less,    "R": menu_item_sw_more },
{"name": menu_item_sh,     "L": menu_item_sh_less,    "R": menu_item_sh_more },
]

def menu():
	global screen
	global well
	global buttons
	global menu_current_item

	screen = TextScreen(width = screen_width, height = screen_height, scalex = scale_x, scaley = scale_y)

	for b in buttons:
		if b == "U":
			if menu_current_item - 1 >= 0:
				menu_current_item -= 1
		elif b == "D":
			if menu_current_item + 1 < len(menu_items):
				menu_current_item += 1
		elif b == "L":
			if menu_items[menu_current_item]["L"] is not None:
				timeout(0, menu_items[menu_current_item]["L"])
				buttons = []
				return
		elif b == "R":
			if menu_items[menu_current_item]["R"] is not None:
				timeout(0, menu_items[menu_current_item]["R"])
				buttons = []
				return
	buttons = []

	screen.clear(0)
	well.draw()

	go_y = well_y + (well_height - 1) / 2 - 2
	for m in xrange(len(menu_items)):
		name = menu_items[m]["name"]()
		if menu_current_item == m:
			name = ">" + name + "<"
		screen.draw_text(well_x, go_y + m, well_x + well_width + 2, go_y + m, name)

	draw_score()
	draw_statistics()

	screen.blit()
	timeout(0, menu)

well.draw()
transitions.append(transition_wellbloom)
transitions.append(transition_wellfade)
transitions.append(menu)
transition_next()
