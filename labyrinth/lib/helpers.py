# -*- coding: utf-8 -*-
"""Template Helpers used in labyrinth."""
import logging
import os
from markupsafe import Markup
from pkg_resources import resource_filename

from tg import app_globals as g
from datetime import datetime

from labyrinth.lib.tree_manager import Tree
from labyrinth.lib.cell import Cell

log = logging.getLogger(__name__)

resources_dirname = os.path.join(os.path.abspath(resource_filename('labyrinth', 'res')))
filename = 'labyrinth.txt'

TERRAINS = ['wall','path']
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']

def current_year():
    now = datetime.now()
    return now.strftime('%Y')

def beginning_has_been_set():
    if any(c.is_beginning for c in g.LABYRINTH):
        return True
    return False

def ending_has_been_set():
    if any(c.is_end for c in g.LABYRINTH):
        return True
    return False

def create_labyrinth():

    with open(resources_dirname + '/' + filename, 'r') as file:
        y = 0
        for line in file:
            # @line : 0,1,2,3,4
            # Incrementing row
            x = 0
            row = list()
            for c in line.split(','):
                cell = Cell()
                cell.coordinate_x = x
                cell.coordinate_y = y
                cell.terrain_type = TERRAINS[int(c)]

                row.append(cell)

                x += 1 # Incrementing column 

            y += 1
            g.LABYRINTH.append(row)

def isDirectionAInverseB(A, B):
    if (A == "up" and B == "down") or (A == "down" and B == "up"):
        return True
    elif (A == "left" and B == "right") or (A == "right" and B == "left"):
        return True
    return False

def move(direction, from_x, from_y):
    new_x = None
    new_y = None
    if direction == 'up':
        cell = Cell.get_cell(from_x, from_y - 1)
        new_x = from_x
        new_y = from_y - 1

    elif direction == 'left':
        cell = Cell.get_cell(from_x - 1, from_y)
        new_x = from_x - 1 
        new_y = from_y

    elif direction == 'right':
        cell = Cell.get_cell(from_x + 1, from_y)
        new_x = from_x + 1
        new_y = from_y

    else:
        cell = Cell.get_cell(from_x, from_y + 1)
        new_x = from_x
        new_y = from_y + 1

    if cell: 
        if cell.terrain_type == 'wall':
            raise Exception("You cant travel through wall")

    if cell.check_if_cell_is_node():
        return cell
    else: 
        # if cell is not a node: 
        move(direction, new_x, from_y)
    

def configureTreeCell(cell):
    if cell: 
        cell.is_visited = True
        cell.has_fog = False
        cell.has_entity = True

        cell.set_nearby_cells_unfoggy()
        capital = LETTERS[cell.coordinate_x]

        if cell.check_if_cell_is_node():
            label = "%s%s" % (cell.coordinate_y, capital)

            node = g.TREE_ROOT.find(label)

            log.debug("Label: %s", label)
            log.debug("Node: %s", node)

            if not node:
                node = Tree.create_node(g.CURRENT_TREE, label, {'x': capital, 'y': cell.coordinate_y})

            g.CURRENT_TREE = node



        # if g.CURRENT_DIRECTION and g.CURRENT_DIRECTION != direction:
        #     # Direction changed, compare if direction is inverse, if not, create a node
        #     if isDirectionAInverseB(g.CURRENT_DIRECTION, direction):
        #         # Check if next node in same direction is wall
        #         if cell.terrain_type == 'wall':
        #             label = "%s%s" % (current_cell.coordinate_y, capital)
        #             node = g.TREE_ROOT.find(label)
        #             if not node: 
        #                 node = Tree.create_node(g.CURRENT_TREE, label, {'x': capital, 'y': current_cell.coordinate_y})
        #                 g.CURRENT_TREE = node
        #     else: 
        #         label = "%s%s" % (current_cell.coordinate_y, capital)
        #         node = g.TREE_ROOT.find(label)
        #         if not node:
        #             node = Tree.create_node(g.CURRENT_TREE, label, {'x': capital, 'y': current_cell.coordinate_y})
        #             g.CURRENT_TREE = node


def icon(icon_name):
    return Markup('<i class="glyphicon glyphicon-%s"></i>' % icon_name)


# Import commonly used helpers from WebHelpers2 and TG
from tg.util.html import script_json_encode

try:
    from webhelpers2 import date, html, number, misc, text
except SyntaxError:
    log.error("WebHelpers2 helpers not available with this Python Version")
