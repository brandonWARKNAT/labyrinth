# -*- coding: utf-8 -*-

"""The application's Globals object"""

__all__ = ['Globals']


class Globals(object):
    """Container for objects available throughout the life of the application.

    One instance of Globals is created during application initialization and
    is available during requests via the 'app_globals' variable.

    """
    LABYRINTH = list()

    TREE_ROOT = None

    CURRENT_TREE = None

    BREADTH_NODE_QUEUE = list()

    DEPTH_NODE_QUEUE = list()

    def __init__(self):
        """Do nothing, by default."""
        pass
