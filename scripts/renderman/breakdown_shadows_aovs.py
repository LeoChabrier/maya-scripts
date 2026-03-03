"""
This script creates a new AOV for shadows in the scene and connects it to the render settings.
It also assigns shadow groups to the lights based on their parent hierarchy
and creates corresponding display channels for each shadow group.
"""
# pylint: disable=import-error, E1111, E1121, E1123, W0622, C0301

# Third-Party
from maya import cmds
from rfm2.ui import widgets
from rfm2.ui import globals

# Internal
from enumeration import LightType
class CreateShadowAovs():
    """Class to create a new AOV for shadows and connect it to the render settings."""
    def __init__(self):
        """Initialize the class."""
        self.rman_lgt = [light.value for light in LightType]
        self.pass_name = "shadow_pass"
        self.open_exr_name = "shadow_exr"
        self.rman_display_channel_ext = "_shadow"

    def update_render_settings(self):
        """Update the UI to reflect the changes made to the render settings."""
        widgets.update_page_visibility('PxrPathTracer')
        globals.update()

    def create_node(self, node_type: str, node_name: str, attrs: dict | None = None) -> str:
        """
        Create a Maya node if it does not exist and optionally set attributes.
        :param node_type: Maya node type (e.g. 'd_openexr', 'rmanDisplayChannel')
        :param node_name: Name of the node
        :param attrs: Optional dictionary of attributes to set {attr_name: value}
        :return: Node name
        """
        if not cmds.objExists(node_name):
            node = cmds.createNode(node_type, name=node_name)
            if attrs:
                for attr, value in attrs.items():
                    cmds.setAttr(f"{node}.{attr}", value)
        else:
            node = node_name

        return node

    def get_next_available_index(self,node: str, array_attr: str) -> int:
        """
        Return the next available logical index for a multi attribute.
        """
        indices = cmds.getAttr(f"{node}.{array_attr}", multiIndices=True)

        if not indices:
            return 0

        return max(indices) + 1

    def connect_aovs(self):
        """Create AOV nodes and prepare them for connection."""

        shadow_display = self.create_node(
            node_type="rmanDisplay",
            node_name=self.pass_name
        )

        shadow_open_exr = self.create_node(
            node_type="d_openexr",
            node_name=self.open_exr_name,
            attrs={"asrgba": False}
        )
        rman_globals = cmds.ls(type="rmanGlobals")

        error_messages = {
            0: "No rmanGlobals node found in the scene.",
            "multiple": "Multiple rmanGlobals nodes found in the scene.\n"
            "Please ensure there is only one."
        }

        count = len(rman_globals)

        if count == 0:
            cmds.error(error_messages[0])
        elif count > 1:
            cmds.error(error_messages["multiple"])

        next_index = self.get_next_available_index(rman_globals[0], "displays")

        cmds.connectAttr(
            f"{shadow_open_exr}.message",
            f"{shadow_display}.displayType",
        )

        cmds.connectAttr(
            f"{shadow_display}.message",
            f"{rman_globals[0]}.displays[{next_index}]",
        )

    def create_shadows_aovs(self):
        """Create AOVs for each shadow in the scene and connect them to the render settings."""
        if cmds.objExists(self.pass_name):
            cmds.delete(self.pass_name)

        # Create the AOV nodes and connect them to the render settings
        self.connect_aovs()
        lgt_list = cmds.ls(typ=self.rman_lgt)
        lgt_transform_list = cmds.listRelatives(lgt_list, parent=True)
        lgt_count = 0
        if not lgt_transform_list:
            cmds.warning("No lights found in the scene.")
            return
        for light in lgt_transform_list:
            lgt_parent_list = cmds.listRelatives(light, parent=True)
            if not lgt_parent_list:
                cmds.warning(f"No parent found for light: {light}")
                continue
            for parents in lgt_parent_list:
                lgt_count += 1
                cmds.setAttr(f"{light}.lightGroup", f"{parents}", type="string")
                name = f"{parents.lower()}{self.rman_display_channel_ext}"
                if not cmds.objExists(name):
                    shadow_display = cmds.createNode('rmanDisplayChannel', name=name)
                    cmds.setAttr(f"{shadow_display}.channelSource", "lpe:shadows;C[DS][L]", type="string")
                    cmds.connectAttr(f"{shadow_display}.message", f"{self.pass_name}.displayChannels[{lgt_count}]")
                    cmds.setAttr(f"{shadow_display}.lpeLightGroup", f"{parents}", type="string")
                    self.update_render_settings()

def main():
    """Main function to execute the script."""
    shadow_class = CreateShadowAovs()
    shadow_class.create_shadows_aovs()

if __name__ == '__main__':
    main()
