# -*- coding: utf-8 -*-


"""
Generate colours!
=================

"""    

import brewer2mpl

def prettyColours():
    set2 = brewer2mpl.get_map('Set2', 'qualitative', 8).mpl_colors  
    return set2
    