Cartpole as a gym environment
=============================

`Gym <https://gym.openai.com/>`_ is a interface to create reinforcement learning environments.


Python
~~~~~~

.. note::

   Using a NVIDIA GPU (Pascal+, 10 series or newer) for this tutorial is recommended.

   As of 10/2021, the only supported consumer AMD-GPU supported are RadeonVII and Vega 64.
   RDNA1-2 are not yet supported.

   See `ROCm website <https://rocmdocs.amd.com/en/latest/>`_ for additional details.


.. warning::

   ``ue4ml`` requires ``msgpack-rpc-python`` which is badly out of date.
   The required tornado version is particularly old ``tornado >= 3,<5``
   This might break your environment. You should build a virtualenv just for UE4.

   You can use `UE4ML_Tweaks <https://github.com/EpicGames/UnrealEngine/pull/8748>`_
   to avoid ``msgpack-rpc-python``


.. warning::

   To try UE4ML on linux you will need to build UE4 from source using
   my `custom branch <https://github.com/Delaunay/UnrealEngine/tree/Enable_U4ML_Linux>`_ (& build rpclib yourself)



- Install python using `conda <https://docs.conda.io/en/latest/miniconda.html>`_
- Install `pytorch <https://pytorch.org/get-started/locally/>`_
- Install ue4ml (python)

.. code-block:: bash

   pip install -e . UnrealEngine/Engine/Plugins/AI/UE4ML/Source/python/

- Enable UE4ML (C++/UE4 plugin)


Create a new environment
~~~~~~~~~~~~~~~~~~~~~~~~

``UE4ML`` already implements the basic blocks for us.
To create a new environment we simply need to inherit from ``ue4ml.UnrealEnv``.
We need to specify with map (i.e level) to load for our training.
Additionally we will need to set our agent configuration which mainly consist of the observation and action space.

.. code-block:: python

   class CartPole(UnrealEnv):
       MAP = '/Game/CartPole/CartPole.umap'
       PROJECT_NAME = None

       def __init__(self, path, ue4params=None, **kwargs):
           CartPole.PROJECT_NAME = path

           if ue4params is not None:
               ue4params.set_default_map_name(CartPole.MAP)

           super().__init__(ue4params=ue4params, **kwargs)


Define the action space
^^^^^^^^^^^^^^^^^^^^^^^

The action space is defined by adding `U4MLActuator <https://docs.unrealengine.com/4.27/en-US/API/Plugins/UE4ML/Actuators/>`_
to the agent configuration.

* Available actuators:

   * InputKey: used the input mapping defined by the project
   * Camera: used to control the camera  (``AddPitchInput`` & ``AddYawInput``)


.. code-block:: python

   class CartPole(UnrealEnv):

       ...

       @staticmethod
       def default_agent_config():
          # Create a new agent config
          agent_config = AgentConfig()

          # Set the spawn class that is being controlled
          agent_config.avatarClassName = "Pawn_Cart_C"

          # Define the action space by adding actuators
          # In our case our entire action space is defined with InputKey
          agent_config.add_actuator("InputKey")


For our example this will result in a an action space of `Discrete(2)`
since only 1 Axis input that varies between -1 and 1.


Define the observation space
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The observation space is defined by adding `U4MLSensor <https://docs.unrealengine.com/4.27/en-US/API/Plugins/UE4ML/Sensors/>`_
to the agent configuration.

* Available sensors:

   * AIPerception: hooks itself to the AI Perception system of UE4 (Note this is a Game-AI (Behavior Trees) system not ML-AI system)

      * see `AI Perception <https://docs.unrealengine.com/4.27/en-US/InteractiveExperiences/ArtificialIntelligence/AIPerception/>`_
        which include Hearing, Sight, Team (proximity of ally), Touch. Currently only Sight is supported, it is created by the
        UE4ML system and added to the player controller.

   * Attribute: listen to attribute change if you are using
     `UAttributeSet <https://docs.unrealengine.com/4.27/en-US/API/Plugins/GameplayAbilities/UAttributeSet/>`_ for your character.
   * Camera: Make a camera capture of the scene
   * Input: Capture the inputs

   * Movement: Capture the characters movement & acceleration

      * Space: ``Box([-1. -1. -1. -1. -1. -1.], [1. 1. 1. 1. 1. 1.], (6,), float32)``
      * 3 floats for the positions and another 3 floats for the acceleration


.. code-block:: python

   class CartPole(UnrealEnv):

       ...

       @staticmethod
       def default_agent_config():
          # Create a new agent config
          agent_config = AgentConfig()

          # Set the spawn class that is being controlled
          agent_config.avatarClassName = "Cart_Pawn_C"

          # Actuators
          ...

          # Define the observation space by adding sensors

          # Add our pawn movement (i.e cart movement)
          agent_config.add_sensor(
              "Movement",
              {
                  "location": "absolute",
                  "velocity": "absolute"
              }
          )

          # Add sight so we can see the pole
          agent_config.add_sensor(
                "AIPerception",
                {
                   "count": "1",                   # Number of actors it can see
                   'sort': 'distance',             # how the actors are sorted `distance`` or `in_front`
                   'peripheral_angle': 360,        # sight cone
                   'mode': 'vector',               # vector (HeadingVector) or rotator
                                                   # max_age
                }
          )

.. code-block:: python

   # Observation space
   Tuple(
      # AIPerception
      Box([-1. -1. -1. -1. -1.], [1. 1. 1. 1. 1.], (5,), float32),

      # Movement
      Box([-1. -1. -1. -1. -1. -1.], [1. 1. 1. 1. 1. 1.], (6,), float32)
   )

   # Observation
   (
      array([ 9.8459434e-41,  3.9260104e+02,  9.6790361e-01, -2.3592940e-01, -8.6601958e-02], dtype=float32),
      array([    240.      ,      90.84363 ,      242.00069 ,      0.      ,    -77.921715,     0.      ], dtype=float32)
   )

.. warning::

   The sight sensor has an affiliation property that can filter out between friendlies/hostiles and neutrals.
   If the ``AIPerception`` observation is not set that would be the main reason why.

   The affiliation is set using ``ETeamAttitude`` from the ``FGenericTeamId``
   The team id is returned using ``FGenericTeamId FGenericTeamId::GetTeamIdentifier(const AActor* TeamMember)``
   The ``AActor`` must implement the ``IGenericTeamAgentInterface`` interface (if not ``FGenericTeamId::NoTeam`` is used).

   The ``ACPActor`` we defined earlier using C++ is handling this and you should not have any issue if you used it for your pole.


Run the environment
~~~~~~~~~~~~~~~~~~~

To test our environment we can write a simple script that will
launch the environment an execute some random actions.

.. code-block:: python

   from cartpole.env import Cartpole
   from ue4ml.utils import random_action, ArgumentParser
   from ue4ml.runner import UE4Params

   parser = ArgumentParser()
   parser.add_argument("--project", type=str, default=project, help="Path to the uproject")
   parser.add_argument("--iter", type=int, default=3, help="number of games to play")
   args = parser.parse_args()

   # python will launch the game
   # if false it will attach to the game that is currently running
   launch = True

   env = Cartpole(
       args.project,
       UE4Params() if not launch else None,
       server_port=15151,
   )

   print('Starting Environment')

   for i in range(args.iter):
       obs = env.reset()

       reward = 0
       done = False
       print('Environment initialized')

       while not env.game_over:
           a = random_action(env)
           # print(obs, a, reward, done)
           print(reward)
           obs, reward, done, _ = env.step(a)

       print("{}: Score: {}".format(i, reward))

   env.close()

You can now run the environment from python.
You need to specify where the UnrealEngine editor is located and the path
to your cartpole uproject.

.. code-block:: bash

   # Add UE-DevBinaries=E:/Engine/Binaries/Win64 to the path
   python Source/python/cartpole/run.py --project E:/cartpole/Cartpole.uproject

   # if UE-DevBinaries is not in the path you can set it manually like bellow
   python Source/python/cartpole/run.py --project E:/cartpole/Cartpole.uproject --exec E:/UnrealEngine/Engine/Binaries/Win64/UE4Editor.exe


.. raw:: html

   <iframe width="100%" height="315" src="https://www.youtube-nocookie.com/embed/dV_mkHu1wQ4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


.. note::

   To test the code above simply install cartpole python environment using ``pip install -e .``
   at the root of the cartpole repository.


.. note::

   When running a python script from the commandline do not forget to use the annaconda
   commandline shortcut that was added when you installed annaconda.


.. note::

   If the python script launch the game but actions are not executed, try executing the environment
   from the editor first.
   UE4ML has a known issue where it can fail to connect to the RPC server when launching UE4.


.. note::

   Only Windows was tested


References
~~~~~~~~~~

.. [#] `Gym <https://gym.openai.com/>`_
.. [#] `ROCm website <https://rocmdocs.amd.com/en/latest/>`_
.. [#] `Enable_U4ML_Linux branch <https://github.com/Delaunay/UnrealEngine/tree/Enable_U4ML_Linux>`_
.. [#] `conda <https://docs.conda.io/en/latest/miniconda.html>`_
.. [#] `pytorch <https://pytorch.org/get-started/locally/>`_
.. [#] `AI Perception <https://docs.unrealengine.com/4.27/en-US/InteractiveExperiences/ArtificialIntelligence/AIPerception/>`_
.. [#] `U4MLSensor <https://docs.unrealengine.com/4.27/en-US/API/Plugins/UE4ML/Sensors/>`_
.. [#] `UAttributeSet <https://docs.unrealengine.com/4.27/en-US/API/Plugins/GameplayAbilities/UAttributeSet/>`_

