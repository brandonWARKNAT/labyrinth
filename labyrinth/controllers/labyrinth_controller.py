# -*- coding: utf-8 -*-
"""Cell controller"""
from tg import request, expose, redirect, flash
from labyrinth.lib.base import BaseController
from labyrinth.lib.cell import Cell
from labyrinth.lib.tree_manager import Tree
from labyrinth.lib.helpers import * 
from tg import app_globals as g

import sys

__all__ = ['LabyrinthController']

# Then i need to implement the algorithms :v
"""
    First we need to create a list that will contain queued nodes
"""

sys.setrecursionlimit(1500)


import logging
log = logging.getLogger(__name__)

LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']

class LabyrinthController(BaseController):
    """
        Controller for Labyrint and Cells creation
    """

    @expose()
    def solve_algorithm(self, *args, **kw):
        """ - Solving By Breadth First Search -
           How we will make it to look animated? Well, the only thing I have in mind is
           each time the algorithm reaches a node, redirect to /. Pasing a parameter
           indicating to continue solving by BFS, e.g. solving_by=BFS. Then in javascript
           have a function that will catch solving_by and if the parameter exist in the url
           we need to redirect to this action. Yeah, is something weird but I think it 
           will work"""


        # 
        log.debug("Keywords: %s" % kw)

        algorithm = kw.get("algorithm")

        priorities = list()

        # Convert dict values to int, and then append to list its key acording to int weight
        priorities = getPriorities(kw)

        if algorithm == "breadth-first-search":

            # Beggining has been already added as a node, and the ending.

            # Travel from nX to zY with a given priority

            # How about ordering priorities in a list and then iterate over them, in the ui each cell visited
            # will be marked with another color to show how the algorithm travelled

            # First step ordenate the priorities

            
            if not len(g.BREADTH_NODE_QUEUE):
                begin_cell = Cell.get_beggining()
                begin_cell.set_cell_class('search')

                g.BREADTH_NODE_QUEUE.append(begin_cell)

            for c_node in g.BREADTH_NODE_QUEUE[:]:

                from_x = c_node.coordinate_x
                from_y = c_node.coordinate_y

                c_node.has_entity = False

                g.BREADTH_NODE_QUEUE.remove(c_node)

                # once ordered, iterate over priorities: 
                for p in priorities:
                    new_cell = None
                    try:
                        new_cell = move(p, from_x, from_y)

                        # Checking cell has not been visited
                        new_cell.set_nearby_cells_unfoggy()
                        new_cell.set_cell_class('search')
                        
                        if not new_cell.is_visited: 
                            g.BREADTH_NODE_QUEUE.append(new_cell)
                            new_cell.is_visited = True
                            new_cell.has_entity = True

                    except Exception as e:
                        print("Error: %s", e)

            redirect('/', params={"name":"hola"})
        
        elif algorithm == "depth-first-search":
            """ A diferencia de breadth, en dept nos seguimos por un camino hasta recorrer todos su nodos
                Se me ocurre iterando por prioridades y agregando a la cola todos con un estado de abierto, 
                si se itera hacia todas las direcciones y no se encuentra nada se sube hacía el siguiente elemento de la cola

            """
            params = dict()

            aux = False

            current_cell = None
            
            begin_cell = Cell.get_beggining()
            
            if not kw.get("begin_set"):
                g.DEPTH_NODE_QUEUE.append(begin_cell)
            
            params["begin_set"] = True


            for p in priorities:
                try:
                    new_cell = None
                    
                    if current_cell == None:
                        if len(g.DEPTH_NODE_QUEUE):
                            current_cell = g.DEPTH_NODE_QUEUE[-1]
                            current_cell.set_cell_class('search')

                    new_cell = move(p, current_cell.coordinate_x, current_cell.coordinate_y)

                    if not new_cell.is_visited:
                        new_cell.is_visited = True
                        new_cell.has_entity = True
                        g.DEPTH_NODE_QUEUE.append(new_cell)
                        aux = True
                        break

    
                except Exception as e:
                    print("Error on depth: %s", e)
            
            if aux == False:
                if len(g.DEPTH_NODE_QUEUE):
                    g.DEPTH_NODE_QUEUE.remove(current_cell)
                    

            redirect('/', params=params)


            


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
            return dict(status=500, detail="No puedes iniciar en muro")
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

