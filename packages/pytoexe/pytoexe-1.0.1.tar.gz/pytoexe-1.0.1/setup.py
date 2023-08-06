from setuptools import setup
__project__ = "pytoexe"
__version__ = "1.0.1"
__description__ = "A Python module to convert python scripts to exe"
__packages__ = ["pytoexe"]
__requires__ = ["cx_Freeze"]
setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    requires = __requires__
)
