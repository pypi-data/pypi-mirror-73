import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stackoverflow_java_queries",
    version="0.1.1",
    author="Ariel",
    author_email="arielblobstein@gmail.com",
    description="Stack Overflow java queries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArielBlG/stackoverflow_java_queries",
    packages=setuptools.find_packages(),
    install_requires=['pandas','javalang','google-cloud-bigquery',],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)