import os.path
import setuptools

# Get the long description from README.
with open("README.rst", "r") as fh:
    long_description = fh.read()

# Get package metadata from '__about__.py' file.
about = {}
base_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(base_dir, "src", "imaps", "__about__.py"), "r") as fh:
    exec(fh.read(), about)

setuptools.setup(
    name=about["__title__"],
    # use_scm_version=True,
    version=about["__version__"],
    description=about["__summary__"],
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author=about["__author__"],
    author_email=about["__email__"],
    url=about["__url__"],
    license=about["__license__"],
    # Exclude tests from built/installed package.
    packages=setuptools.find_packages("src", exclude=["tests", "tests.*", "*.tests", "*.tests.*"]),
    package_dir={"": "src"},
    python_requires=">=3.6, <3.8",
    install_requires=[
        "matplotlib",
        "numpy",
        "pandas==0.24.2",
        "plumbum",
        "pybedtools",
        "scipy",
        "seaborn",
        "scikit-learn==0.22.1",
        "resdk>=11.0.1",
        # XXX: Temporarily pin wrapt to 1.11.x, since astroid 2.3.3
        # has requirement wrapt==1.11.*
        "textdistance",
        "wrapt==1.11.*",
        "xlrd",
    ],
    extras_require={
        "docs": ["sphinx_rtd_theme"],
        "package": ["twine", "wheel"],
        "test": [
            "black",
            "check-manifest",
            "docutils",
            "flake8",
            "isort<5.0.0",
            "ngs-test-utils",
            "pydocstyle",
            "pytest-cov",
            "setuptools_scm",
        ],
    },
    entry_points={
        "console_scripts": [
            "check-assets = imaps.scripts.check_assets:main",
            "imaps-sites = imaps.operations.sites:Sites.cli",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="imaps CLIP iCLIP bioinformatics protein",
)
