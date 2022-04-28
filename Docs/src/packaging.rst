Packaging
=========

Once your RL environment is done you will want to package it
for other people to use.

1. `Cook the game <https://docs.unrealengine.com/4.27/en-US/SharingAndReleasing/Deployment/Cooking/>`_
   this will generate a compact version of the environment that can easily be redistributed.

.. code-block:: python

   UE4Editor.exe <GameName or uproject> -run=cook -targetplatform=<Plat1>+<Plat2> [-cookonthefly] [-iterate] [-map=<Map1>+<Map2>]


2. Package the cooked game with your python code by adding
   all the files in the `package_data` section of setuptools


.. code-block:: python

   setup(
       name="cartpole",
       package_data={"cartpole": [
           "UE cooked files",
                ...
       ]},
   )


3. To access the packaged data inside a python module you can use `pkg_resources`


.. code-block:: python

   import pkg_resources

   cartpole_linux = pkg_resources.resource_filename(
       __name__, "Cooked/LinuxNoEditor/Cartpole/Binaries/Linux/Cartpole"
   )

References
----------

.. [#] `Cooking <https://docs.unrealengine.com/4.27/en-US/SharingAndReleasing/Deployment/Cooking/>`_
