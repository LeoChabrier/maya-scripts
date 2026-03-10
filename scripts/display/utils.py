"""Utils file containing basic functions for Maya viewport."""
# pylint:disable = E1111, E0401

# Third-party
from maya import cmds

def display_as_bounding_box():
    """
    To optimize loading time when opening scene,
    it's a good idea to display heavy models as bounding box
    """
    sel = cmds.ls(sl=True)
    for obj in sel:
        cmds.setAttr(obj + ".overrideLevelOfDetail", 1)
        cmds.setAttr(obj + ".overrideEnabled", 1)
        cmds.select(d=True)

def display_full_geometry():
    """Switch from bouding box to full geometry display"""
    sel = cmds.ls(sl=True)
    for obj in sel:
        cmds.setAttr(obj + ".overrideLevelOfDetail", 0)
        cmds.setAttr(obj + ".overrideEnabled", 0)
        cmds.select(d=True)

def unset_lod_visiblity():
    """Level Of Detail visiblity set on 0 will display object in render only"""
    sel = cmds.ls(sl=True)
    for obj in sel:
        cmds.setAttr(f'{obj}.lodVisibility', 0)

def set_lod_visiblity():
    """Level Of Detail visiblity set on 1 will display object in viewport"""
    sel = cmds.ls(sl=True)
    for obj in sel:
        cmds.setAttr(f'{obj}.lodVisibility', 1)
