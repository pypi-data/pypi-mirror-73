import os

if 'YBC_ENV' in os.environ:
    from qbc_box.ide_box import buttonbox
    from qbc_box.ide_box import choicebox
    from qbc_box.ide_box import codebox
    from qbc_box.ide_box import enterbox
    from qbc_box.ide_box import fileopenbox
    from qbc_box.ide_box import indexbox
    from qbc_box.ide_box import intbox
    from qbc_box.ide_box import integerbox
    from qbc_box.ide_box import msgbox
    from qbc_box.ide_box import multchoicebox
    from qbc_box.ide_box import multenterbox
    from qbc_box.ide_box import multpasswordbox
    from qbc_box.ide_box import passwordbox
    from qbc_box.ide_box import tablebox
    from qbc_box.ide_box import textbox
    from qbc_box.ide_box import ynbox
else:
    from qbc_box.native_box import buttonbox
    from qbc_box.native_box import choicebox
    from qbc_box.native_box import codebox
    from qbc_box.native_box import enterbox
    from qbc_box.native_box import fileopenbox
    from qbc_box.native_box import indexbox
    from qbc_box.native_box import intbox
    from qbc_box.native_box import integerbox
    from qbc_box.native_box import msgbox
    from qbc_box.native_box import multchoicebox
    from qbc_box.native_box import multenterbox
    from qbc_box.native_box import multpasswordbox
    from qbc_box.native_box import passwordbox
    from qbc_box.native_box import tablebox
    from qbc_box.native_box import textbox
    from qbc_box.native_box import ynbox

__all__ = [
    'buttonbox',
    'choicebox',
    'codebox',
    'enterbox',
    'fileopenbox',
    'indexbox',
    'intbox',
    'integerbox',
    'msgbox',
    'multchoicebox',
    'multenterbox',
    'multpasswordbox',
    'passwordbox',
    'tablebox',
    'textbox',
    'ynbox',
]

__version__ = '1.1.0'
