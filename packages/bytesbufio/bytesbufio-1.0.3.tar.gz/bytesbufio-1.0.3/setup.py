import re
import subprocess

import setuptools


def get_readme(version):
    with open("readme.md", "r", encoding='utf-8') as fh:
        readme = fh.read()
        readme = re.sub(r"]\(\./", f"](https://github.com/cbuschka/python-bytesbufio/blob/v{version}/", readme)
        return readme


def get_version():
    proc = subprocess.Popen(['git', 'describe', '--exact-match', '--tags'], stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    stdout, stderr = proc.communicate()
    result = re.search('^v([^\n]+)\n$', stdout.decode("utf-8"), re.S)
    if not result:
        raise ValueError("Invalid version: '{}'.".format(result))
    return result.group(1)


version = get_version()
long_description = get_readme(version)

setuptools.setup(
    name="bytesbufio",
    version=version,
    author="Cornelius Buschka",
    author_email="cbuschka@gmail.com",
    description="io.BytesIO that preserves bytes after close",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cbuschka/python-bytesbufio",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
