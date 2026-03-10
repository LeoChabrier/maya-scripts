# Maya Scripts
This repository contains python scripts for Maya & Renderman.

![RenderMan](https://img.shields.io/badge/RenderMan-23+-orange)
![Python](https://img.shields.io/badge/Python-3.7+-green)
![Maya](https://img.shields.io/badge/Maya-2018.3+-blue)

## Requirements

- **Renderman 23+**
- **Python 3.7+**
- **Maya 2018.3+**

## Features

| Feature | Module | Description |
|---------|--------|-------------|
| Light AOV Automation | `renderman/breakdown_lights_aovs` | Auto-create light passes with per-light group filtering |
| Shadow AOV Automation | `renderman/breakdown_shadows_aovs` | Auto-create shadow passes with per-light group filtering |
| AOV Import from JSON | `renderman/utils` | Load AOV configurations from JSON presets |
| Render Layer Import from JSON | `renderman/utils` | Load render layer configurations from JSON presets |
| Relative Texture Paths | `renderman/utils` | Convert texture paths to relative (`<ws>`) paths for project portability |
| Viewport Optimization | `display/utils` | Toggle bounding box display for heavy geometry |
| LOD Visibility Control | `display/utils` | Control geometry visibility in viewport vs. render |

### RenderMan

#### Light AOV Breakdown

Scans the scene for all RenderMan lights, assigns light groups based on parent hierarchy, and creates individual `rmanDisplayChannel` nodes with the appropriate LPE expressions.

```python
from renderman import breakdown_lights_aovs
breakdown_lights_aovs.main()
```

#### Shadow AOV Breakdown

Same approach as light AOVs — creates shadow passes and assigns shadow groups to lights based on parent hierarchy.

```python
from renderman import breakdown_shadows_aovs
breakdown_shadows_aovs.main()
```

#### Import AOVs / Render Layers from JSON

Load AOV or render layer presets from a JSON file via a file browser window.

```python
from renderman.utils import Utils

# Import AOVs
Utils()._generic_window("Imports AOVs from Json", callback=Utils().import_aovs_from_json)

# Import Render Layers
Utils()._generic_window("Imports RenderLayers from Json", callback=Utils().import_render_layers)
```

#### Relative Texture Paths

Converts all texture paths in the scene to relative `<ws>` paths, avoiding missing textures when moving projects.

```python
from renderman.utils import Utils
Utils().set_relative_path()
```

### Display

Viewport optimization utilities for selected geometry.

```python
from display.utils import display_as_bounding_box, display_full_geometry, unset_lod_visibility, set_lod_visibility

display_as_bounding_box()   # Show selected objects as bounding boxes
display_full_geometry()     # Restore full geometry display
unset_lod_visibility()      # Hide in viewport, still renders
set_lod_visibility()        # Visible in viewport and renders
```

## Shelf

A custom Maya shelf (`shelves/shelf_MayaScripts.mel`) is included with quick-access buttons:

| Button | Action |
|--------|--------|
| **Light** | Create light AOVs and assign light groups |
| **Shadows** | Create shadow AOVs and assign shadow groups |
| **AOVs** | Import AOV presets from JSON |
| **Layers** | Import render layer presets from JSON |

Copy the shelf file to _%USERNAME%/maya/\<your_maya_version\>/prefs/shelves_ to use it.

## Documentations
- [RenderMan](https://rmanwiki-27.pixar.com/)
- [Python](https://www.python.org/)
- [Maya](https://www.autodesk.com/fr/support/technical/article/caas/tsarticles/tsarticles/FRA/ts/lC3jaffqnWFyQoLPEPm7n.html)

## Installation

1. **Clone the repository** :
   ```bash
   git clone https://github.com/LeoChabrier/maya-scripts.git
   ```

2. **Copy to Maya Preferences** :

   Copy _scripts_ folder to _%USERNAME%/maya/\<your_maya_version\>/prefs_

   Or run the .ps1 script and give it your maya preferences path

   ```bash
   cd maya-scripts
   ./.scripts/Push-Update.ps1
   ```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
