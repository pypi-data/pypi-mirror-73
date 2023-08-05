from distutils.core import setup

setup(
        name='pilton',
        version='1.0.5',
        py_modules= ['pilton','bcolors'],
        package_data     = {
            "": [
                "*.txt",
                "*.md",
                "*.rst",
                "*.py"
                ]
            },
        license='Creative Commons Attribution-Noncommercial-Share Alike license',
        long_description="Python interface for Parameter Interface Library (PIL)",
        )
