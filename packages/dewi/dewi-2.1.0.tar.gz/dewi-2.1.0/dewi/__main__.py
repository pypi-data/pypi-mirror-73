# Copyright 2015-2020 Laszlo Attila Toth
# Distributed under the terms of the GNU Lesser General Public License v3


import sys

from dewi_core.application import Application
from dewi_core.loader.loader import PluginLoader


def main():
    loader = PluginLoader()
    app = Application(loader, 'dewi', fallback_to_plugin_name='dewi.DewiPlugin')
    app.run(sys.argv[1:])


if __name__ == '__main__':
    main()
