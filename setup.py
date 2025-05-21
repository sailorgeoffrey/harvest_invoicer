try:
    from setuptools import setup, find_packages
except ImportError:
    from pip._internal.commands.install import InstallCommand
    install_cmd = InstallCommand()
    install_cmd.main(['setuptools'])
    from setuptools import setup, find_packages

setup(
    name="invoicer",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "setuptools",
        "jinja2",
        "requests",
        "markdown-it-py",
        "markdown_pdf",
        "MarkupSafe",
        "keyring"
    ],
    entry_points={
        'console_scripts': [
            'invoicer=invoicer.invoicer:main',
        ],
    },
    package_data={
        'invoicer': ['template.md'],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to generate invoices from Harvest time tracking data",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/invoicer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
