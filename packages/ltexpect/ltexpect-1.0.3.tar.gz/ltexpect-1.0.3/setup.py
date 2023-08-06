import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="ltexpect",
    version="1.0.3",
    description="Easier Expect interface",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/laowangv5/ltexpect",
    author="Yonghang Wang",
    author_email="yhang_wang@icloud.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    packages=["ltexpect"],
    include_package_data=True,
    keywords=['ltexpect', 'liteexpect','expect', 'lexpect','ltexpect','LiteExpect','Expect'],
    install_requires=["pexpect"],
    entry_points={
        "console_scripts": [
            "ltexpect=ltexpect.__main__:main",
        ]
    },
)
