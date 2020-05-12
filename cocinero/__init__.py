import os
import sys
import os

from cocinero.cli import cli

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


__version__ = '0.1.0'

os.environ['COCINERO_VERSION'] = __version__

__main__ = cli()
