

import tellurium as _te
import matplotlib.pyplot as _plt
import numpy as _np
import os as _os

def _getModelDir():
    import pathlib as _pathlib
    parent = _pathlib.Path(__file__).parent
    return os.path.joint (parent.__str__(), 'models')

def listModelNames():
    import pathlib as _pathlib
    parent = _pathlib.Path(__file__).parent
    flist = _os.listdir (_getModelDir())
    return flist

def listModel(name):
    f = open(os.path.join (_getModelDir() , "name"), "r")
        string = f.read()
    f.close()
    return string 

def runModel (name):
    path = os.path.joing (_getModelDir(), name)
    exec(open(path).read())
