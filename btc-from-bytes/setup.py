from setuptools import setup, find_packages

setup(
    name="byte2btc",
    version="0.1.0",
    description="Geração de chaves e endereços Bitcoin a partir de vetores de bytes.",
    author="Rodrigo Carlos Moraes",
    author_email="qrodrigob@gmail.com",
    packages=find_packages(),
    install_requires=[
        "base58",
        "bech32",
        "ecdsa"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.7',
)
