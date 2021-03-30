from pathlib import Path
from sys import argv

from ncd.ncd import bz2, ncd

if __name__ == "__main__":
    if len(argv) == 2:
        print(f'Size of bz2 {argv[1]}:',
              bz2(Path(argv[1])))
    elif len(argv) == 3:
        print(f'NCD of {argv[1]}, {argv[2]} using bz2:',
              ncd(Path(argv[1]),
                  Path(argv[2]),
                  bz2),
              )
