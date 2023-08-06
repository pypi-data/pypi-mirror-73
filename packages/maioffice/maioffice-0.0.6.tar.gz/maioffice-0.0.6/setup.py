import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="maioffice",
    version="0.0.6",
    author="maishu",
    author_email="maishucoder@gmail.com",
    description="maishu's office package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://blog.qingke.me",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'openpyxl',
        'python-docx',
    ],
    python_requires='>=3.6',
)
