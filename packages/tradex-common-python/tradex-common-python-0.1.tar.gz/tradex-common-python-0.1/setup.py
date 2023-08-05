import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='tradex-common-python',  
    version='0.1',
    author="HiepNtt",
    author_email="tuanhiep1232@gmail.com",
    description="common for tradex project using python language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        "tradex_common_python", 
        "tradex_common_python.kafka", 
        "tradex_common_python.async_lib", 
        "tradex_common_python.models", 
        "tradex_common_python.models.tuxedo", 
        "tradex_common_python.models.tuxedo.vcsc",
        "tradex_common_python.models.tux_broadcast",
        "tradex_common_python.models.tux_broadcast.vcsc",
        "tradex_common_python.rx",
        "tradex_common_python.utils", 
        "tradex_common_python.errors",
        "tradex_common_python.test",
    ],
    install_requires=[
        'confluent-kafka',
        'simplejson',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
