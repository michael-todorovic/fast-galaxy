from setuptools import setup, find_packages

setup(
    name="fast-galaxy",
    version="0.1.2",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fast-galaxy=fast_galaxy.__main__:main',
        ],
    },
    install_requires=[
        'PyYAML',
    ],
    author="Michael Todorovic",
    author_email="michael.todorovic@outlook.com",
    description="A package to split and install Ansible Galaxy requirements in parallel.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/michael-todorovic/fast-galaxy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
