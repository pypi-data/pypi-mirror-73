import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="faros",
    version="0.1.0",
    author="Faros",
    author_email="contact@faros.ai",
    description="Faros API SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/faros-ai/faros-python-client",
    keywords=["faros", "api", "graphql", "sdk"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    install_requires=[
        "graphqlclient>=0.2.4",
        "attrs==19.3.0"
    ],
    python_requires='>=3.6'
)
