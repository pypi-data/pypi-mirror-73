import os
import setuptools

root = os.path.abspath(os.path.dirname(__file__))

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

about = {}
with open(os.path.join(root, 'kleentimer', '__about__.py'), 'r', encoding='utf-8') as file:
    exec(file.read(), about)

packages = [
    'kleentimer'
]

setuptools.setup(
    name=about['_title'],
    version=about['_version'],
    description=about['_description'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=about['_author'],
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'kleentimer': 'kleentimer'},
    license=about['_license'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
