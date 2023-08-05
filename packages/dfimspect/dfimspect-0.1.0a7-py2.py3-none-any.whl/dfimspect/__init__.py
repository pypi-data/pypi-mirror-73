from ._version import version_info, __version__

from .example import *
from .widget import *

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'df-imspect-widget',
        'require': 'df-imspect-widget/extension'
    }]
