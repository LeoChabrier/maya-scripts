"""Utils file containing basic functions for Maya-Renderman."""
# pylint: disable = import-error, redefined-builtin, protected-access, no-member, assignment-from-no-return, unexpected-keyword-arg, too-many-arguments, too-many-positional-arguments

# Built-in
from pathlib import Path
import json

# Third-party
from maya import cmds
from maya.app.renderSetup.views import renderSetupWindow
from maya.app.renderSetup.model import renderSetup
from rfm2.ui import widgets
from rfm2.ui import globals

# Internal
from .enumeration import TextureNodeType

class Utils():
    """Utils class containing functions for Renderman-Maya"""

    def __init__(self):
        self.textures_nodes_type = [texture_node.value for texture_node in TextureNodeType]

    def import_aovs_from_json(self, json_path:Path):
        """
        Import aovs in current scene from a .json preset previously exported by user
        Args:
            json_path: path to the .json file to import
        """
        renderSetupWindow._importAOVsFromPath(json_path)
        widgets.update_page_visibility('PxrPathTracer')
        globals.update()

    def import_render_layers(self, json_path:Path):
        """
        Import Render Layers in current scene from a .json preset previously exported by user
        Args:
            json_path: path to the .json file to import
        """
        with open(json_path, 'r', encoding="UTF-8") as file:
            renderSetup.instance().decode(
            {'renderSetup' : {'renderLayers' : json.load(file)}},
            renderSetup.DECODE_AND_MERGE,
            None)

    def set_relative_path(self):
        """
        Loop through Renderman textures nodes to set path relative to project.
        This avoid missing textures when moving a project from a folder to another.
        """
        absolute_path = cmds.workspace(q=True, rd=True)
        relative_characters = "<ws>"
        texture_node_list = cmds.ls(typ=self.textures_nodes_type)

        for node in texture_node_list :
            if cmds.nodeType(node) == TextureNodeType.PXR_MULTI_TEXTURE.value:
                count = 0
                while cmds.attributeQuery(f"filename{count}", node=node, exists=True):
                    param = f"{node}.filename{count}"
                    filename = cmds.getAttr(param)
                    self._check_filename(node, param, filename, absolute_path, relative_characters)
                    count += 1
            else:
                param = f"{node}.filename"
                filename = cmds.getAttr(param)
                self._check_filename(node, param, filename, absolute_path, relative_characters)

    def _check_filename(
        self, node:str,
        param:str,
        filename:str,
        absolute_path:str,
        relative_characters:str
        ):
        """
        Check filename to ensure it's a relative one or at least in correct project path.
        Args:
            node: current node
            param: the parameter name to access
            filename : the current node filename parameter to check
            aboslute_path : the absolute path to the current workspace
            relative_characters : the defined characters by Renderman to target current workspace
        """
        if not filename:
            return

        is_relative = relative_characters in filename
        is_in_project = absolute_path in filename

        if not is_relative and not is_in_project:
            cmds.error(
                f"{node} has a texture outside the project:\n{filename}\n"
                "Move it to sourceimages and try again."
            )

        elif not is_relative :
            filepath_to_replace = filename.replace(absolute_path, relative_characters + "/")
            cmds.setAttr(param, filepath_to_replace, type="string")
