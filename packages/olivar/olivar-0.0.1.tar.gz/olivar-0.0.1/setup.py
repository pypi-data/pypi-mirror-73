import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="olivar", # Replace with your own username
    version="0.0.1",
    author="Treangen Lab",
    author_email="acd7+olivar@rice.edu",
    description="Olivar pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/treangen.lab/olivar",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'pip',
        'pipdeptree',
        'pandas',
        'certifi',
        'chardet',
        'docopt',
        'idna',
        'pipreqs',
        'requests',
        'urllib3',
        'yarg',
        'biopython',
        'jinja2',
        'pysam',
        'pyvcf',
        'tqdm',
      ],
    
    scripts=['bin/olivar'],

)