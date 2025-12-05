from setuptools import setup, find_packages

setup(
    name="stellarforge",
    version="0.1.0",
    description="Cosmic Simulation Application with PyQt6 and VisPy",
    author="StellarForge Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "PyQt6>=6.6.0",
        "vispy>=0.14.0",
        "numpy>=1.24.0",
        "scipy>=1.11.0",
        "astropy>=5.3.0",
        "noise>=1.2.2",
        "mesa>=2.1.0",
        "h5py>=3.10.0",
        "pyopengl>=3.1.6",
        "pillow>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "stellarforge=main:main",
        ],
    },
)
