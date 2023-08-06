from setuptools import setup, find_packages
setup(
    name="jsonxdm",
    version="0.1",
    packages=find_packages(),
    scripts=['jsonxdm.py'],

    install_requires=['lxml'],

    author="Pim van der Eijk",
    author_email="pvde@sonnenglanz.net",
    description="Convert between JSON and XML following the XDM schema of XSLT 3.0",
    keywords="xdm, xslt, json, xml, xsd",
    url="https://bitbucket.org/ebcore/jsonxdm/",   # project home page, if any
    project_urls={
        "Documentation": "https://bitbucket.org/ebcore/jsonxdm/",
        "Source Code": "https://bitbucket.org/ebcore/jsonxdm/src/master/",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License"
    ]
)
