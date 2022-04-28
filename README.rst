Cartpole
========

.. image:: https://readthedocs.org/projects/cartpole/badge/?version=latest
   :target: https://cartpole.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

Reimplementation of the cartpole environment in UE4 as a demo of the MLAdapter plugin

.. image:: /_static/Cartpole_big.png


Requirements
~~~~~~~~~~~~

* UE4 - 4.27/master/5.1


.. note::

   For linux you will need to compile `Enable_U4ML_Linux branch <https://github.com/EpicGames/UnrealEngine/pull/8745>`_ from source.

.. note::

   For a more reliable experience you can use `UE4ML_Tweaks branch <https://github.com/Delaunay/UnrealEngine/tree/UE4ML_Tweaks>`_

.. note::

   For UE5 on linux you will need to disable 2 plugins (XGEController and FastBuildController as of Jan 2022)


Packaged Install
~~~~~~~~~~~~~~~~

Unfortunately U4ML python package is not open source and you will need to
create an Epic account to install it on your machine.
Once it is install you can run any packaged environment without installing or compiling UnrealEngine.

.. code-block:: bash

   # Install MLAdapter python package
   python -e UnrealEngine/Engine/Plugins/AI/MLAdapter/Source/python

   # Download the cartpole environment
   wget https://github.com/Delaunay/cartpole/releases/download/0.0.0-package-test/cartpole-0.0.0-py3-none-any.whl
   pip install cartpole-0.0.0-py3-none-any.whl

   # run the packaged environment for training
   cartpole-train --launch


Development Install
~~~~~~~~~~~~~~~~~~~

.. note::

   This repo started using UE5 after commit ``332ae357235995d1184effdb060``


Install the python package to run this example as a gym environment

.. code-block:: bash

   git clone https://github.com/Delaunay/cartpole
   cd cartpole
   pip install -e .

   # Install MLAdapter python package
   python -e UnrealEngine/Engine/Plugins/AI/MLAdapter/Source/python

   # this will compile the project
   UE4Editor Cartpole.uproject

   # Click play in the editor to start the game

   # this will connect to the game running inside the editor
   cartpole-train --no-launch


To run the example just launch the appropriate script

.. code-block:: bash

   python Source/python/cartpole/run.py --project E:/cartpole/Cartpole.uproject --exec E:/UnrealEngine/Engine/Binaries/Win64/UE4Editor.exe
