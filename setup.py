"""Python setup.py for js2pysecrets package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("js2pysecrets", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="js2pysecrets",
    version=read("js2pysecrets", "VERSION"),
    description="Shamir's Secret Sharing - A port of secrets.js-grempe to Python, allowing cross-platform compatible shares between JavaScript and Python.",
    url="https://github.com/poing/JS2PySecrets/",
    project_urls={
        'Documentation': 'https://poing.github.io/JS2PySecrets',
        'Source': 'https://github.com/poing/JS2PySecrets',
        'Bug Tracker': 'https://github.com/poing/JS2PySecrets/issues/',
    },
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Brian LaVallee",
    author_email="brian.lavallee@invite-comm.jp",
	python_requires='>=3.11',
	keywords = [
		"Adi",
		"Adi Shamir",
		"how to share a secret",
		"scheme",
		"secret",
		"secrets.js",
		"secrets",
		"Shamir Secret Sharing Scheme",
		"Shamir's Secret Sharing",
		"Shamir's",
		"Shamir",
		"share",
		"shares",
		"sharing",
		"sss",
		"ssss",
	],
	classifiers = [
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
		"Intended Audience :: Information Technology",
        'Intended Audience :: Other Audience',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3.11",
		"Topic :: Security :: Cryptography",
        'Topic :: Security', 
        'Topic :: Utilities', 
        "Operating System :: OS Independent",
        "Natural Language :: English",
	],
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["js2pysecrets = js2pysecrets.__main__:main"]
    },
    extras_require={"test": read_requirements("requirements-test.txt")},
)
