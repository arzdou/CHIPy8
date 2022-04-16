import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CHIPy8",
    version="0.1.0",
    author="Jaime Travesedo",
    author_email="jaimetravesedo125@gmail.com",
    description="CHIP8 interpreter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jtl125/CHIPy8",
    project_urls={
        "Bug Tracker": "https://github.com/jtl125/CHIPy8/issues",
    },
    scripts=["bin/chipy8"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pygame',
    ],
    packages=['chipy8'],
    package_data = {
        'chipy8': ['beep.mp3', 'icon.png', 'font.ch8'],
    },
    python_requires='>=3.8',
)