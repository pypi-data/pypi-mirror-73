from distutils.version import LooseVersion

__version__ = '0.3.3'
__version_info__ = tuple(LooseVersion(__version__).version)

__all__ = [
    'parsers',
    'readers',
    'sniffers',
]
