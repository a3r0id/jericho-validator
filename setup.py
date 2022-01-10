# Installs the module

import setuptools

description = "Validate arbitrary base64-encoded image uploads as incoming data urls while preserving image integrity but removing EXIF and unwanted artifacts and mitigating RCE-exploit potential."

required = ["Pillow==9.0.0"]

setuptools.setup(name='jericho_validator',
    version='1.0',
    description=description,
    author='github.com/hostinfodev',
    author_email='aero@recon.us.com',
    url='https://github.com/hostinfodev/jericho-validator',
    project_urls={
        "Example Usage": "https://github.com/hostinfodev/jericho-validator/tree/main/example",
    },
    packages=setuptools.find_packages(where="src"),
    install_requires=required,
    package_dir={"": "src"},
    python_requires=">=3.6",
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"
    ],)