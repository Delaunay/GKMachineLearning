Make the cartpole game
~~~~~~~~~~~~~~~~~~~~~~

.. image:: /_static/cartpole_overview.png
   :width: 100%


You will need to specialize 3 classes in C++.

* ``ACPPlayerState`` to expose `SetScore <https://docs.unrealengine.com/4.27/en-US/API/Runtime/Engine/GameFramework/APlayerState/SetScore/>`_
  to blueprint, this will be used to create a custom reward function
* ``ACPPawn`` to make the pawn hostile to everybody,
  this makes ``AISense_Sight`` sense all the pawn that are in range
* ``ACPGameMode`` to provide a custom ``HasMatchEnded``
  that is used to reset the environment

From there everything can be done in blueprint.
You will need to create the blueprints below.

* Level: ``CartPole``
* ``GameMode_CartPole`` inherited from ``CPGameMode``
* ``Pawn_Cart`` (inherited from ``Pawn``)
* ``Pawn_Pole`` (inherited from ``CPPawn``)
* PlayerState_Cart (inherited from ``CPPlayerState``)
* PlayerController_Cart (inherited from ``PlayerController``)

.. note::

   Both ``PlayerState_Cart`` and ``PlayerController_Cart`` are left empty.
   Your input handling could be moved to ``PlayerController_Cart`` if you wanted.


GameMode_CartPole
^^^^^^^^^^^^^^^^^

.. raw:: html

   <iframe width="100%" height="350px" src="https://blueprintue.com/render/1g8l1wr9/" scrolling="no" allowfullscreen></iframe>


Pawn_Cart
^^^^^^^^^

* Add a ``FloatingPawnMovement`` component to enable the cart's movement
* The cart is composed of a single cube followed by a cylinder rotated 90 degrees i.e ``(0, -90, 0)``
* The cube is translated ``(200, 0, 0)`` so it can be seen from the default camera

.. raw:: html

   <iframe width="100%" height="350px" src="https://blueprintue.com/render/i7gdsnhm/" scrolling="no" allowfullscreen></iframe>


Pawn_Pole
^^^^^^^^^

* The pole is a single cylinder
* Enable physics on the cylinder.
* You can modify Linear Damping and Angular Damping
  properties to make the pole easier to balance.

.. raw:: html

   <iframe width="100%" height="350px" src="https://blueprintue.com/render/4qwvkpbi/" scrolling="no" allowfullscreen></iframe>


You should now be able to play the game


.. comment

   .. raw:: html

      <details>
         <summary><code>GameMode_CartPole</code> (inherited from <code>CPGameMode</code>)</summary>
         <iframe width="100%" height="350px" src="https://blueprintue.com/render/1g8l1wr9/" scrolling="no" allowfullscreen></iframe>
      </details>

   .. raw:: html

      <details>
         <summary><code>Pawn_Cart</code> (inherited from <code>Pawn</code>)</summary>
         <iframe width="100%" height="350px" src="https://blueprintue.com/render/i7gdsnhm/" scrolling="no" allowfullscreen></iframe>
      </details>

   .. raw:: html

      <details>
         <summary><code>Pawn_Pole</code> (inherited from <code>CPPawn</code>)</summary>
         <iframe width="100%" height="350px" src="https://blueprintue.com/render/4qwvkpbi/" scrolling="no" allowfullscreen></iframe>
      </details>
