Known Issues
============

Cartpole Bugs
~~~~~~~~~~~~~

* Pole Initial push is ineffective after a few level restarts, might be related to the PlayerController issue (fixed on MLAdapter_Tweaks)


MLAdapter Bugs
~~~~~~~~~~

* PlayerController is not set upon level reset.
  The training script is sending actions but UE4ML agent does nothing
  because his PlayerController reference is null. (mitigated on UE4ML_Tweaks)

* U4ML does not launch on standalone builds (fixed on MLAdapter_Tweaks)

* Standalone game crash after python connection

UE4 Linux Bugs
~~~~~~~~~~~~~~

.. code-block::

   Assertion failure at SDL_DestroyWindow_REAL (/SDL-gui-backend/src/video/SDL_video.c:2840), triggered 1 time:
    'window && window->magic == &_this->window_magic'


UE5 Linux Bugs
~~~~~~~~~~~~~~


