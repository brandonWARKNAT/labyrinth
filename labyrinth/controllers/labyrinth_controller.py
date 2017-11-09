# -*- coding: utf-8 -*-
"""Cell controller"""
from tg import request, expose, redirect
from labyrinth.lib.base import BaseController
from labyrinth.lib.cell import Cell
from labyrinth.lib.tree_manager import Tree
from labyrinth.lib.helpers import * 
from tg import app_globals as g

__all__ = ['LabyrinthController']

# Then i need to implement the algorithms :v
"""
    First we need to create a list that will contain queued nodes
"""

import logging
log = logging.getLogger(__name__)

LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']

class LabyrinthController(BaseController):
    """
        Controller for Labyrint and Cells creation
    """

    @expose('json')
    def breadth_first_search(self, **kw):
        """ - Solving By Breadth First Search -
           How we will make it to look animated? Well, the only thing I have in mind is
           each time the algorithm reaches a node, redirect to /. Pasing a parameter
           indicating to continue solving by BFS, e.g. solving_by=BFS. Then in javascript
           have a function that will catch solving_by and if the parameter exist in the url
           we need to redirect to this action. Yeah, is something weird but I think it 
           will work"""

        # 
        log.debug("Keywords: ", kw)

        # Beggining has been already added as a node, and the ending.

        # Travel from nX to zY with a given priority

        # How about ordering priorities in a list and then iterate over them, in the ui each cell visited
        # will be marked with another color to show how the algorithm travelled

        # First step ordenate the priorities

        priorities = list()
        
        if not len(g.BREADTH_NODE_QUEUE):
            print("It is suposed I've entered Here :D");
            begin_cell = Cell.get_beggining()
            begin_cell.set_cell_class('search')

            g.BREADTH_NODE_QUEUE.append(begin_cell)

        # Convert dict values to int, and then append to list its key acording to int weight
        
        if int(kw.get('up_priority')) == 1:
            priorities.append('up')
        elif int(kw.get('down_priority')) == 1:
            priorities.append('down')
        elif int(kw.get('left_priority')) == 1: 
            priorities.append('left' )
        elif int(kw.get('right_priority')) == 1: 
            priorities.append('right')

        if int(kw.get('up_priority')) == 2:
            priorities.append('up')
        elif int(kw.get('down_priority')) == 2:
            priorities.append('down')
        elif int(kw.get('left_priority')) == 2: 
            priorities.append('left' )
        elif int(kw.get('right_priority')) == 2: 
            priorities.append('right')

        if int(kw.get('up_priority')) == 3:
            priorities.append( 'up')
        elif int(kw.get('down_priority')) == 3:
            priorities.append( 'down')
        elif int(kw.get('left_priority')) == 3: 
            priorities.append( 'left' )
        elif int(kw.get('right_priority')) == 3: 
            priorities.append( 'right')

        if int(kw.get('up_priority')) == 4:
            priorities.append('up')
        elif int(kw.get('down_priority')) == 4:
            priorities.append('down')
        elif int(kw.get('left_priority')) == 4: 
            priorities.append('left' )
        elif int(kw.get('right_priority')) == 4: 
            priorities.append('right')
        
        for c_node in g.BREADTH_NODE_QUEUE: 
            from_x = c_node.coordinate_x
            from_y = c_node.coordinate_y
            g.BREADTH_NODE_QUEUE.remove(c_node)

            # once ordered, iterate over priorities: 
            for p in priorities:
                try:
                    new_cell = move(p, from_x, from_y)
                    new_cell.set_nearby_cells_unfoggy()
                    new_cell.set_cell_class('search')
                    g.BREADTH_NODE_QUEUE.append(new_cell)
                except Exception as e:
                    pass
    

        redirect('/')


    @expose('json')
    def create_beginning(self, **kw):
        """
            Este método crea el nodo raíz para el árbol de decisión. 
            También convierte una celula en la celula inicial. 
        """
        response = dict()

        log.debug("These are the keywords: %s", kw)
        
        begin_cell = Cell.get_cell(int(kw.get('x-coordinate')), int(kw.get('y-coordinate')))


        if begin_cell.terrain_type == 'wall':
            return dict(status=500, detail="No puedes inciar en muro")
        else:
            begin_cell.is_visited = True
            begin_cell.is_beginning = True
            begin_cell.has_fog = False
            begin_cell.has_entity = True

            # Locate Cell at # and set nearby cells not foggy
            begin_cell.set_nearby_cells_unfoggy()


            X_letter = LETTERS[begin_cell.coordinate_x]
            
            Tree.init_tree("%s%s" % (begin_cell.coordinate_y, X_letter), {'x': X_letter, 'y': begin_cell.coordinate_y})

        return dict(status=200, detail="Se ha creado el nodo satisfactoriamente")


    @expose('json')
    def create_ending(self, **kw):
        """
            Este método crea el nodo raíz para el árbol de decisión. 
            También convierte una celula en la celula inicial. 
        """
        response = dict()

        log.debug("These are the keywords: %s", kw)
        
        end_cell = Cell.get_cell(int(kw.get('x-coordinate')), int(kw.get('y-coordinate')))


        if end_cell.terrain_type == 'wall':
            return dict(status=500, detail="El fin no puede ser un muro")
        else:
            end_cell.is_end = True

            X_letter = LETTERS[end_cell.coordinate_x]
            
            # Tree.init_tree("%s%s" % (end_cell.coordinate_y, X_letter), {'x': X_letter, 'y': end_cell.coordinate_y})

        return dict(status=200, detail="Se ha ajustado el fin")
        
    @expose('json')
    def move(self, **kw):
        """
            Este método mueve al usuario hacía una posición. Si es una celula de desición, 
            creara un nuevo nodo en el árbol.
        """
        # First check where to move
        response = dict()
        
        direction = kw.get('move')
        from_x = int(kw.get('from_x'))
        from_y = int(kw.get('from_y'))
        cell = None

        """ We should check if cell is end of path, this means,
            he cannot move to the same direction he is going without hitting 
            a wall or having to take a desicion
        """
        
        if direction == 'up':
            cell = Cell.get_cell(from_x, from_y - 1)

        elif direction == 'left':
            cell = Cell.get_cell(from_x - 1, from_y)

        elif direction == 'right':
            cell = Cell.get_cell(from_x + 1, from_y)

        else:
            cell = Cell.get_cell(from_x, from_y + 1)
            
        if cell:
            if cell.terrain_type == 'wall':
                return dict(status=500, detail="No puedes moverte a muro")
            
            
            configureTreeCell(cell)
        
        current_cell = Cell.get_cell(from_x, from_y)
        current_cell.has_entity = False
        # Remove entity from cell only if movement was done

        print(g.TREE_ROOT)

        return dict(status=200, detail="Movimiento realizado correctamente")
