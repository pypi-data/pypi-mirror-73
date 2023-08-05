import io
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, "README.rst"), "rt", encoding="utf8") as f:
    readme = f.read()

about = {}
with io.open(
    os.path.join(here, "grvlmsstripe", "__about__.py"),
    "rt",
    encoding="utf-8",
) as f:
    exec(f.read(), about)

setup(
    name="grvlms-stripe",
    version=about["__version__"],
    url="https://github.com/groovetch/grvlms-stripe",
    project_urls={
        "Code": "https://github.com/groovetch/grvlms-stripe",
        "Issue tracker": "https://github.com/groovetch/grvlms-stripe/issues",
    },
    license="AGPLv3",
    author="GrooveTechnology",
    description="Stripe plugin for Grvlms",
    long_description=readme,
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    python_requires=">=3.5",
    install_requires=["grvlms-openedx"],
    entry_points={
        "grvlms.plugin.v0": [
            "stripe = grvlmsstripe.plugin"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
