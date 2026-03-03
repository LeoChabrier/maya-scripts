# Maya Scripts
This repository contains python scripts for Maya & Renderman.

![RenderMan](https://img.shields.io/badge/RenderMan-23+-orange)
![Python](https://img.shields.io/badge/Python-3.7+-green)
![Maya](https://img.shields.io/badge/Maya-2018.3+-blue)

## Requirements

- **Renderman 23+**
- **Python 3.7+**
- **Maya 2018.3+**

## Documentations
- [RenderMan](https://rmanwiki-27.pixar.com/)
- [Python](https://www.python.org/)
- [Maya](https://www.autodesk.com/fr/support/technical/article/caas/tsarticles/tsarticles/FRA/ts/lC3jaffqnWFyQoLPEPm7n.html)

## Installation

1. **Clone the repository** :
   ```bash
   git clone https://github.com/LeoChabrier/deadline-renderman-denoiser.git
   ```

2. **Copy to Maya Preferences** :

   Copy scripts forlder to %USERNAME%/maya/<your_maya_version>/prefs

2. **Example In Maya script editor** :
   ```bash
   from renderman import breakdown_lights_aovs
   breakdown_lights_aovs.main()
   ```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
