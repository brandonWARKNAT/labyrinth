# -*- coding: utf-8 -*-
""" Tree Manager Library for Labyrinth """

import os

import tg
from tg import url
from tg import app_globals as g

import logging
log = logging.getLogger(__name__)

class Tree(object):
    """@Class creates a tree"""
    def __init__(self):
        self.parent = None # If None wee asume node is Root, because no orphan nodes allowed
        self.label = None # Node label, unique
        self.children = [] # Node array, containing node subnodes. It can be calculated? 
        self.coordinates = {} # e.g. {'x': 'A', 'y': 0}

    def __repr__(self):
        return '<TreeNode: %s>' % (self.label)

    @classmethod
    def create_node(cls, parent, label, coordinates):
        new_node = Tree()
        new_node.parent = parent
        new_node.label = label
        new_node.coordinates = coordinates
        parent.children.append(new_node)
        
        return new_node

    def delete_node(coordinate_x, coordinate_y): # @x = 'A', @y = 0
        """If a tree node is deleted, we should delete all orphan nodes"""
        pass

    def edit_node():
        # Method not defined
        pass

    def find(self, label):
        if self.label == label: 
            return self
        for node in self.children:
            n = node.find(label)
            if n: return n
        return None

    def __str__(self, level=0):
        ret = "\t" * level + repr(self)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    @classmethod
    def init_tree(cls, label, coordinates):
        
        tree = Tree()
        tree.label = label
        tree.coordinates = coordinates
        
        g.TREE_ROOT = tree
        g.CURRENT_TREE = tree


  # def edit_node(label=None, node=None, coordinates, children):
  #   pass

  # def delete_node():
  #   # Take into account that if you delete a parent node, all children will die
  #   pass