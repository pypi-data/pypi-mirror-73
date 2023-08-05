
import setuptools
import os
import re

with open("README.md", "r") as fh:
    long_description = fh.read()

def find_version(fnam,version="VERSION"):
    with open(fnam) as f:
        cont = f.read()
    regex = f"{version}\s*=\s*[\"]([^\"]+)[\"]"
    match = re.search(regex,cont)
    if match is None:
        raise Exception( f"version with spec={version} not found, use double quotes for version string")
    return match.group(1)
   
def find_projectname():
    cwd = os.getcwd()
    name = os.path.basename(cwd)
    return name  

projectname = find_projectname()
file = os.path.join( "modapp", "watering", "__init__.py" )
version = find_version(file)

setuptools.setup(
    
    name=projectname, 
    version=version,
    author="k.r. goger",
    author_email = f"k.r.goger+{projectname}@gmail.com",
    license= f"https://github.com/kr-g/{projectname}/blob/master/LICENSE",
    description="mpymodcore",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = f"https://github.com/kr-g/{projectname}",
    packages=setuptools.find_packages( ),
    include_package_data=True,
    keywords = 'mpy-modcore micropython framework micro-framework esp32 esp8266',
    install_requires=[],#['mpymodcore'],
    # https://pypi.org/classifiers/
    classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'Topic :: Software Development :: Embedded Systems',
            'Topic :: Utilities',
            'Topic :: Home Automation',
            'Topic :: Software Development :: Libraries :: Application Frameworks',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Programming Language :: Python :: Implementation :: MicroPython',
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    ],
    
)

