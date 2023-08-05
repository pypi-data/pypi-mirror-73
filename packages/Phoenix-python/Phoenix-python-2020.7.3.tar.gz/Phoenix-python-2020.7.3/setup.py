from setuptools import setup
from setuptools import find_packages

with open("README.md") as f:
    LONG_DESCRIPTION = f.read()
    f.close()

MAJOR_VERSION = "2020"
MINOR_VERSION = "7"
MICRO_VERSION = "3"
VERSION = "{}.{}.{}".format(MAJOR_VERSION, MINOR_VERSION, MICRO_VERSION)

setup(
    name='Phoenix-python',
    version="v"+VERSION,
    description='This is a pip-installable package for executing java and python programs together.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    author='Sam Arora',
    author_email='phoenix.language.official@gmail.com',
    keywords=['Phoenix','Java','Python','Java-Python Integration','phoenix','java','python','java-python integration'],
    url='https://github.com/Sam-Arora',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Win32 (MS Windows)",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    requires_python=">=3.4.0",
)
