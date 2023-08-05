## Modular Home Automation
## (c) Copyright Si Dunford, 2019

## Need to:
# Create folders /opt/miot and /etc/opt/miot
# Create empty /etc/opt/miot/config.ini
# copy miot.sh as "miot" into the path somewhere, or a link to it.
# chmod 775 miot file
# Download installer.ini
# Execute "miot update" 
#   Which will:
#       Download miot-core.py
#       Add [MQTT] broker=127.0.0.1, port=1883 to config.ini

# Later updates will also include a WebGUI, but for now that has not 
# been written. "miot update" will introduce those features.

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='miot',  
    version='1.0.1',
    scripts=['miot/miot'] ,
    author="Si Dunford",
    author_email="dunford.sj+miot@gmail.com",
    description="Modular Internet of Things",
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/automation-itspeedway-net/miot.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Other Audience",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces"
        ],
    install_requires=[
        'paho-mqtt',
        'configparser'
        ],
    include_package_data=True,
    python_requires='>=3.6'
)

#Development Status :: 1 - Planning
#Development Status :: 2 - Pre-Alpha
#Development Status :: 3 - Alpha
#Development Status :: 4 - Beta
#Development Status :: 5 - Production/Stable
#Development Status :: 6 - Mature
#Development Status :: 7 - Inactive  


