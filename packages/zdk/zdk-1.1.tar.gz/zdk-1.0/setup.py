import setuptools

setuptools.setup(
    name='zdk',
    version='1.0',
    author="Deisy Muñoz",
    author_email="deisy.dymo@gmail.com",
    description="SDK for Zinobe Tech API's",
    long_description="This SKD for Zinobe Tech allows to consume any API in a disengaged way. ",
    long_description_content_type="text/markdown",
    url="https://https://gitlab.sg-zinobe.com/pythagoras/zdk/-/tree/develop",
    download_url="https://gitlab.sg-zinobe.com/pythagoras/zdk.git",
    packages=['zdk', 'zdk.core', 'zdk.zinobe.zevents'],
    keywords=['sdk', 'api', "zinobe"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)