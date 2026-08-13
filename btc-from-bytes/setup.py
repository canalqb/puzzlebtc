from setuptools import setup, find_packages

setup(
    name="btc-keygen",
    version="0.1.0",
    description="Geração de chaves e endereços Bitcoin a partir de vetores de bytes",
    author="CanalQb",
    author_email="canalqb@example.com",
    license="MIT",
    py_modules=["btc_keygen"],
    install_requires=[
        "base58",
        "bech32",
        "ecdsa",
    ],
    extras_require={
        "dev": ["pytest>=6.0", "bit>=0.13.0"],
    },
    entry_points={
        "console_scripts": [
            "btc-keygen=btc_keygen:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)