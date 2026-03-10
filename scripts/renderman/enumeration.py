"""Enumeration module for Renderman scripts."""

# Third-Party
from enum import Enum

class LightType(Enum):
    """Enumeration for Renderman light types."""
    RECT_LIGHT = "PxrRectLight"
    DOME_LIGHT = "PxrDomeLight"
    PORTAL_LIGHT = "PxrPortalLight"
    DISK_LIGHT = "PxrDiskLight"
    DISTANT_LIGHT = "PxrDistantLight"
    SPHERE_LIGHT = "PxrSphereLight"
    CYLINDER_LIGHT = "PxrCylinderLight"

class TextureNodeType(Enum):
    """Enumeration for Renderman texture nodes types."""
    PXR_TEXTURE = "PxrTexture"
    PXR_P_TEXTURE =  "PxrPtexture"
    PXR_MULTI_TEXTURE = "PxrMultiTexture"
    PXR_BUMP = "PxrBump"
    PXR_NORMAL_MAP = "PxrNormalMap"
