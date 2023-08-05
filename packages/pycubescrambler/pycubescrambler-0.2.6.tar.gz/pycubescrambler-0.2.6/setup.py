import setuptools

setuptools.setup(
    name="pycubescrambler",
    version="0.2.6",
    author="midnightcuberx",
    author_email="midnightcuberx@gmail.com",
    url="https://github.com/midnightcuberx/pycubescrambler",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'appdirs',
        'packaging',
        'PyExecJS',
        'pyparsing',
        'six',
    ],
)
