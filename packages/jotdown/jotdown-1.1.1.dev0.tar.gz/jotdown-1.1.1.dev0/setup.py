from pathlib import Path
from setuptools import setup
from setuptools.extension import Extension

pymodule = Extension(
    name="jotdown",
    include_dirs=["include", "moonlight/include"],
    sources=[str(src) for src in Path.cwd().glob("src/*.cpp")],
    extra_compile_args=["-O3", "-shared", "-Wall", "-std=c++2a", "-fPIC"],
)

def local_scheme(version):
    return ""

# Get the long description from the README file
with open(Path("README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="jotdown",
    description="Jotdown structrured document language, C++ to python wrapper module.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lainproliant/jotdown",
    author="Lain Musgrove (lainproliant)",
    author_email="lainproliant@gmail.com",
    license="BSD",
    use_scm_version={"local_scheme": local_scheme},
    setup_requires=["setuptools_scm"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="document structure parser query language",
    ext_modules=[pymodule],
    zip_safe=False,
    include_package_data=True,
)
