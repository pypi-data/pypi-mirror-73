# --------------------------------------------------------------------
# bake.py
#
# Author: Lain Musgrove (lain.proliant@gmail.com)
# Date: Saturday February 22, 2020
#
# Distributed under terms of the MIT license.
# --------------------------------------------------------------------
import shlex
import subprocess
from pathlib import Path

from panifex import build, default, provide, seq, sh, target, noclean

# -------------------------------------------------------------------
PYPI_USERNAME = "lainproliant"
PYPI_KEY_NAME = "pypi"

# -------------------------------------------------------------------
INCLUDE_DIRS = [
    "./include",
    "./python/include",
    "./moonlight/include",
    "./pybind11/include",
]

# -------------------------------------------------------------------
INCLUDES = ["-I" + inc for inc in INCLUDE_DIRS]

sh.env(
    CC="clang++",
    CFLAGS=(
        "-g",
        *INCLUDES,
        "--std=c++2a",
        "-DMOONLIGHT_DEBUG",
        "-DMOONLIGHT_ENABLE_STACKTRACE",
        "-DMOONLIGHT_STACKTRACE_IN_DESCRIPTION",
    ),
    LDFLAGS=("-rdynamic", "-g", "-ldl"),
)


# --------------------------------------------------------------------
def check(cmd):
    return subprocess.check_output(shlex.split(cmd)).decode("utf-8").strip()


# -------------------------------------------------------------------
def compile_app(src, headers):
    return sh(
        "{CC} {CFLAGS} {input} {LDFLAGS} -o {output}",
        input=src,
        output=Path(src).with_suffix(""),
        includes=headers,
    )


# -------------------------------------------------------------------
def link_pybind11_module(pybind11_module_objects):
    return sh(
        "{CC} -O3 -shared -Wall -std=c++2a -fPIC {input} -o {output}",
        input=pybind11_module_objects,
        output="jotdown%s" % check("python3-config --extension-suffix"),
    )


# -------------------------------------------------------------------
def compile_pybind11_module_object(src, headers):
    return sh(
        "{CC} -O3 -shared -Wall -std=c++2a -fPIC {flags} {input} -o {output}",
        input=src,
        output=Path(src).with_suffix(".o"),
        flags=INCLUDES + shlex.split(check("python-config --includes")),
        includes=headers,
    )


# -------------------------------------------------------------------
@provide
def submodules():
    return sh("git submodule update --init --recursive")


# -------------------------------------------------------------------
@provide
def headers():
    return Path.cwd().glob("include/jotdown/*.h")


# -------------------------------------------------------------------
@provide
def demo_sources(submodules):
    return Path.cwd().glob("demo/*.cpp")


# -------------------------------------------------------------------
@provide
def test_sources(submodules):
    return Path.cwd().glob("test/*.cpp")


# -------------------------------------------------------------------
@target
def demos(demo_sources, headers):
    return [compile_app(src, headers) for src in demo_sources]


# -------------------------------------------------------------------
@target
def tests(test_sources, headers):
    return [compile_app(src, headers) for src in test_sources]


# -------------------------------------------------------------------
@provide
def version():
    return check("git describe --tags --abbrev=0")


# -------------------------------------------------------------------
@target
def run_tests(tests):
    return (sh("{input}", input=test, cwd="test").interactive() for test in tests)


# -------------------------------------------------------------------
@target
def pybind11_tests(submodules):
    return seq(
        sh("mkdir -p {output}", output="pybind11-test-build"),
        sh("cmake ../pybind11", cwd="pybind11-test-build"),
        sh("make check -j 4", cwd="pybind11-test-build").interactive(),
    )


# -------------------------------------------------------------------
@provide
def pymodule_sources(submodules):
    return Path.cwd().glob("python/src/*.cpp")


# -------------------------------------------------------------------
@target
def pymodule_objects(pymodule_sources, headers, run_tests):
    return [compile_pybind11_module_object(src, headers) for src in pymodule_sources]


# -------------------------------------------------------------------
@target
def pymodule_dev(pymodule_objects):
    return link_pybind11_module(pymodule_objects)


# -------------------------------------------------------------------
@target
def pymodule_sdist(submodules, version):
    return sh("python3 setup.py sdist", output="dist")


# -------------------------------------------------------------------
@target
@noclean
def pypi_upload(pymodule_sdist):
    tarballs = [*Path('dist').glob('*.tar.gz')]
    latest_tarball = max(tarballs, key=lambda x: x.stat().st_mtime)

    pypi_password = check(f"pass {PYPI_KEY_NAME}")
    return sh(
        "twine upload -u {PYPI_USERNAME} -p {pypi_password} {pymodule_sdist}",
        PYPI_USERNAME=PYPI_USERNAME,
        pypi_password=pypi_password,
        pymodule_sdist=latest_tarball,
    )


# -------------------------------------------------------------------
@default
def all(demos, pymodule_dev):
    pass


# -------------------------------------------------------------------
build()
