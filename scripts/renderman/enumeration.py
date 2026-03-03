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
