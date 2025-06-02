from setuptools import setup, find_packages

setup(
    name="treeviz",
    version="0.1",
    description="Directory‐tree visualization",
    author="Your Name",
    author_email="you@example.com",
    packages=find_packages(),      # ← this finds the “treeviz/” folder automatically
    install_requires=[
        # e.g. "networkx>=2.0", etc., if you have runtime deps.
    ],
    entry_points={
        "console_scripts": [
            "treeviz = treeviz.cli:main",  # if you want a `treeviz` CLI
        ],
    },
)

