from setuptools import setup, find_packages
# 
with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name="nanocamera",
	version="0.1.5",
	author="Ayo Ayibiowu",
	author_email="charlesayibiowu@hotmail.com",
	description="A Python camera interface for the Jetson Nano",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/thehapyone/NanoCamera",
	project_urls={
        "Examples": "https://github.com/thehapyone/NanoCamera/tree/master/examples",
        "Documentation": "https://github.com/thehapyone/NanoCamera/blob/master/README.md",
        "Source Code": "https://github.com/thehapyone/NanoCamera",
    },
	packages=find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: POSIX :: Linux",
	],
	python_requires='>=3',
)
