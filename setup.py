from setuptools import setup, find_packages

setup(
    name="cobertura_merge",
    version="0.1.0",
    packages=find_packages(include=["cobertura_merge", "cobertura_merge.*"]),
    entry_points={"console_scripts": ["cobertura-merge=cobertura_merge:main"]},
    install_requires=["pydantic==1.8.2", "xmltodict==0.12.0"],
    license_files=("LICENSE",),
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
)
