from cx_Freeze import setup, Executable
class Setup():
  def __init__(self, FileName, Packages, nameOfExec, versionOfExec, descriptive):
    base = None    

    executables = [Executable(FileName, base=base)]

    packages = Packages
    options = {
        'build_exe': {    
            'packages':packages,
        },    
    }

    setup(
        name = nameOfExec,
        options = options,
        version = versionOfExec,
        description = descriptive,
        executables = executables
    )
