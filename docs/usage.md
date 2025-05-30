### 3. `setup.py`
```python
from setuptools import setup, find_packages

setup(
    name="treeviz",
    version="0.1.0",
    description="Terminal-based file tree visualizer with TUI and export formats.",
    author="Your Name",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'treeviz=treeviz.cli:main',
        ],
    },
    install_requires=[
        'urwid>=2.1.2',
        'PyYAML>=6.0'
    ],
)
