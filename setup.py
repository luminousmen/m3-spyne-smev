import os
from distutils.core import setup


def read_file(name):
    with open(os.path.join(os.path.dirname(__file__), name)) as fd:
        return fd.read()

setup(
    name="spyne-smev",
    packages=[
        "spyne_smev", "spyne_smev.smev256", "spyne_smev.smev255",
        "spyne_smev.server", "spyne_smev.wsse"],
    package_dir={"": "src"},
    package_data={"": ["xsd/*"]},
    url="http://bitbucket.org/timic/spyne-smev",
    license=read_file("LICENSE"),
    description=read_file("DESCRIPTION"),
    author="Timur Salyakhutdinov",
    author_email="t.salyakhutdinov@gmail.com",
    requires=["lxml", "cryptography==0.4.1"],
    dependency_links=[
        "https://github.com/timic/cryptography/archive/0.4.1.zip"
        "#egg=cryptography-0.4.1"
    ]
)
