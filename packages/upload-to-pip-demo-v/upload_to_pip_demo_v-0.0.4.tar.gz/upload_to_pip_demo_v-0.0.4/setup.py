import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="upload_to_pip_demo_v", # Replace with your own username
    version="0.0.4",
    author="Gegham Vardanyan",
    author_email="vardanyan.gegham95@gmail.com",
    description="demo package to test uploading to PyPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/geghamcode/upload_to_pip_demo.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "hub-login = mock_library.click_cmd:hello",
        ],
    },
)