from setuptools import find_packages, setup

with open('README.md') as f:
    README = f.read()

setup(
    name="gitlab_superb_helper",
    version="1.0.0",
    url="",
    author="Renan Ben Moshe",
    author_email="renan.moshe@gmail.com",
    license="",
    description="Projeto para ser utilizado como Helper para o GitLab",
    long_description=README,
    python_requires=">=3.5",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    include_package_data=True,
    packages=find_packages(),
)