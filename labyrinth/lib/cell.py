# -*- coding: utf-8 -*-
""" Cell Class  for Labyrinth """
from tg import app_globals as g

class Cell(object):
	"""docstring for Cell"""
	TERRAINS = ['wall', 'path']

	def __init__(self):
		self.coordinate_x = None
		self.coordinate_y = None
		self.is_visited = False
		self.has_fog = True
		self.has_entity = False
		self.is_beginning = False
		self.is_end = False
		self.clazz = ""
		self.terrain_type = None

	def __repr__(self):
		return '<Cell: x=%s, y=%s, foggy=%s, terrain=%s>' % (self.coordinate_x, self.coordinate_y, self.has_fog, self.terrain_type)

	@classmethod
	def get_cell(cls, x, y):
		"""Search in labyrinth cell for a given cell"""
		for row in g.LABYRINTH:
			for cell in row:
				if cell.coordinate_x == x and cell.coordinate_y == y:
					return cell

	@classmethod
	def get_beggining(cls):
		for row in g.LABYRINTH:
			for cell in row:
				if cell.is_beginning:
					return cell
		return None

	def check_if_cell_is_node(self):
		
		up_cell = Cell.get_cell(self.coordinate_x, (self.coordinate_y - 1)) 

		right_cell = Cell.get_cell(self.coordinate_x + 1, self.coordinate_y)

		down_cell = Cell.get_cell(self.coordinate_x, self.coordinate_y + 1)

		left_cell = Cell.get_cell(self.coordinate_x - 1, self.coordinate_y)
			# 1																									#2
		if ((up_cell and up_cell.terrain_type == 'path' and down_cell and down_cell.terrain_type == 'path') and (not left_cell or left_cell.terrain_type == 'wall' and not right_cell or right_cell.terrain_type == 'wall')) or ((left_cell and left_cell.terrain_type == 'path' and right_cell and right_cell.terrain_type == 'path') and (not up_cell or up_cell.terrain_type == 'wall' and not down_cell or down_cell.terrain_type == 'wall')):
			return False
		return True

	def set_cell_class(self, clazz):
		self.clazz = clazz
	
	def set_nearby_cells_unfoggy(self):
		# First we seek for up cell:
		if self.coordinate_y - 1 < 0:
			up_cell = None
		else:
			
			up_cell = Cell.get_cell(self.coordinate_x, (self.coordinate_y - 1))
			

			if up_cell:
				up_cell.has_fog = False

		# second place seek for right cell 
		if self.coordinate_x + 1 > len(g.LABYRINTH):
			right_cell = None
		else:
			right_cell = Cell.get_cell(self.coordinate_x + 1, self.coordinate_y)

			if right_cell:
				right_cell.has_fog = False

		# Third place seek for down cell
		if self.coordinate_y + 1 > len(g.LABYRINTH):
			down_cell = None
		else:
			down_cell = Cell.get_cell(self.coordinate_x, self.coordinate_y + 1)
			
			if down_cell:
				down_cell.has_fog = False

		# Then, seek for left cell
		if self.coordinate_x - 1 < 0:
			left_cell = None
		else:
			left_cell = Cell.get_cell(self.coordinate_x - 1, self.coordinate_y)
			if left_cell:
				left_cell.has_fog = False
		


		