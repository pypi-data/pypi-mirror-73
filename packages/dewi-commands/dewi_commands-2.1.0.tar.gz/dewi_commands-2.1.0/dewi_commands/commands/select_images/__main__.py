# Copyright 2020 Laszlo Attila Toth
# Distributed under the terms of the GNU Lesser General Public License v3

import sys

from dewi_commands.commands.select_images import ImageSelectorCommand
from dewi_core.application import SingleCommandApplication


def main():
    app = SingleCommandApplication('dewi-select-images', ImageSelectorCommand)
    app.run(sys.argv[1:])


if __name__ == '__main__':
    main()
