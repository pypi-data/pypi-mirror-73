from distutils.core import setup
import simple_assertions

version = simple_assertions.__version__

setup(
    name="simple-assertions",
    packages=["simple_assertions"],
    version=version,
    description="Assertion library (skeleton) inspired from `assertpy`"
                " but without batteries",
    author="Ninad Mhatre",
    author_email="ninad.mhatre@gmail.com",
    url="",
    download_url="https://github.com/assertpy/assertpy/archive/{}.tar.gz".format(
        version
    ),
    keywords=[
        "test",
        "testing",
        "assert",
        "assertion",
        "simple-assertions",
        "simpleassertions",
        "nose",
        "nosetests",
        "unittest",
    ],
    license="BSD",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
