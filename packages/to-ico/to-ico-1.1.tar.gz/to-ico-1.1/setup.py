import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="to-ico",
    version="1.1",
    author="amshinski",
    author_email="amshinski@gmail.com",
    description="A small png to ico convertor script. Just type 'to-ico' in console.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amshinski/to-ico",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['ico', 'console', 'convert', 'image'],
    python_requires='>=3.6',
    install_requires=[
       "Pillow",
    ],
    scripts=['to_ico/to_ico.py'],
    entry_points={
        'console_scripts': ['to-ico=to_ico:main']
    },
)