import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="yssh",
    version="1.0.0",
    description="ssh tool with expect and multithreading",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/laowangv5/yssh",
    author="Yonghang Wang",
    author_email="yhang_wang@icloud.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    packages=["yssh"],
    include_package_data=True,
    install_requires=["pexpect"],
    keywords=['ssh','yssh','myssh','pssh','sshx'],
    entry_points={
        "console_scripts": [
            "yssh=yssh.__main__:main",
        ]
    },
)
