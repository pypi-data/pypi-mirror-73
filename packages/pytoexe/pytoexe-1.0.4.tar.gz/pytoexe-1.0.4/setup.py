from setuptools import setup, find_packages
__project__ = "pytoexe"
__version__ = "1.0.4"
__description__ = "A Python module to convert python scripts to exe"
__packages__ = ["pytoexe"]
__requires__ = ["cx_Freeze"]
setup(
    name = __project__,
    version = __version__,
    author = "pennacap",
    maintainer = "pennacap",
    long_description = __description__,
    description = __description__,
    packages=find_packages(),
    requires = ["cx_Freeze"],
    python_requires='>=3.5.2',
)
