======
TIAMAT
======

Intro
=====

Tiamat is the single binary builder for Python projects.

Getting Started
===============

The main idea behind Tiamat is to make building python projects as a single
frozen binary easy. Therefore using tiamat just takes a few steps.

So we can start with an existing python application, this quickstart will assume
that your python project has a standard `setup.py` and `requirements.txt`.

The only other thing that most projects will need is a `run.py`.

The run.py
----------

Since Tiamat creates a single binary, it needs a single entry point. This entry
point is defined in the file `run.py`. This is just a simple python script that is
used to start your application. The contents of the `run.py` is typically the same
code that is used in your setuptools entry point, or the startup script used in
distutils. There is nothing special about the run.py, `tiamat` just needs an
entry point that is clean python.

.. note::

    Setuptools creates a startup script that dynamically discovers part of how
    the application starts up. This makes sense when the application is started
    in an environment with many python libs and apps. But tiamat creates an
    isolated python environment which does not satisfy the needs of setuptools.

A typical `run.py` will look like this:

.. code-block:: python

    import myapp

    def main():
        myapp.start()

    main()

Just some good old python! If you are building a pop project then `pop-seed` will
create the run.py for you.

Run Tiamat
----------

Thats right! All you need outside of a `run.py` your python project likely already has!
Tiamat uses the setup.py and requirements.txt files to build the environment used.

So assuming you have a standard python project defined, all you need to do is cd to that
directory and run `tiamat build`, in this example we will assume the application is called
foo:

.. code-block:: bash

    tiamat build -n foo

This will kick off the process and the resulting binary will be placed in `dist/foo`

Now that the binary is available it can be directly called.

What Happened?
--------------

Tiamat starts with the version of python that you exceuted `tiamat` with. This python
is the python that will be embeded in your binary. Next it creates a venv for your application.
With the venv in hand, Tiamat populates it. The venv is populated with all of the deps that
are defined as requrements for the main application, including the application itself.

Now that the venv has been set up, we tell PyInstaller to create a binary from the `run.py`.
But PyInstaller is all about building a binary from all of the imports that come from
the run.py. This is done to build a small binary and include only the most required code.
But this is not the case for many applications, it is typical that things are late imported
and the application assumes that a larger python environment is available. It is also typical
that extra files are needed by the application and are typically added via the setup.py.

Instead of following the imports, Tiamat bundles the venv into the binary created by
PyInstaller. This means that you have a strong assurance that the full, needed environment is
available. This does make a larger binary, but it allows for a much easier and reliable build.
Also, the binary is typically not much bigger.

Using the Build Addon
=====================

Many python projects require C libraries. How is it then, that
the dynamic libs can be added to the final binary? Tiamat has an answer to this.

When running `tiamat` we can use a configuration file. This file allows for any option
that would be passed on the cli to be defined, but also to define the routines for
external builds.

A Tiamat config, that as an example, adds the library libsodium looks like this:

.. code-block:: yaml

    tiamat:
      build:
        libsodium:
          sources:
              - https://download.libsodium.org/libsodium/releases/LATEST.tar.gz
          make:
              - tar xvf LATEST.tar.gz
              - cd libsodium-stable && ./configure && make
          src: libsodium-stable/src/libsodium/.libs/libsodium.so
          dest: lib/

This example shows how we can define a library to download and build, then the `src`
which is relative to the root of the build and the `dest` which is relative to the root
of the venv.

The src can be a directory or a list of files, the dest is just a single directory to store
the files.
