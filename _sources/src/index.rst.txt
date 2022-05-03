Getting started
===============

This project demonstrates how to use UE4ML to create a reinforcement learning
environment for machine learning.

   Machine learning (ML) is the study of computer algorithms that can improve automatically through experience and by the use of data.
   It is seen as a part of artificial intelligence. Machine learning algorithms build a model based on sample data,
   known as training data, in order to make predictions or decisions without being explicitly programmed to do so.

   -- From `Wikipedia <https://en.wikipedia.org/wiki/Machine_learning>`_

We will recreate the famous |Cartpole Env|,
which is a very simple environment that is straight forward to implement and yet will enable us
to focus on how to setup a project for machine learning, then we will train a neural network to play our game.

The notions seen in this project are applicable to any games made using UnrealEngine.

This project does not aim to introduce you to UE4 nor to teach your machine learning;
some knownledge of both is expected.


Why UnrealEngine
~~~~~~~~~~~~~~~~

* UnrealEngine is essentially open-source.
  The source is proprietary and technically private but you can get access by simply creating an Epic Account.
* The licencing is perfect for academia (See Creators LICENSE)
* All UnrealEngine technologies available to develop new cutting edge environments
* Easy to port research into the real world
* Easy to develop and redistribute environments

Cartpole
~~~~~~~~

.. toctree::
   :maxdepth: 2

   install
   ue4ml
   game
   launching
   training
   packaging


References
~~~~~~~~~~

.. [#] |Cartpole Env|
.. [#] |ML|
.. [#] `UE4ML Documentation <https://docs.unrealengine.com/4.27/en-US/API/Plugins/UE4ML/>`_
.. [#] `OpenAI Gym <https://gym.openai.com/>`_
.. [#] `PyTorch Documentation <https://pytorch.org/>`_

.. |ML| replace:: `Machine Learning`_
.. _Machine Learning: https://en.wikipedia.org/wiki/Machine_learning

.. |Cartpole Env| replace:: `Cartpole Environment`_
.. _Cartpole Environment: https://gym.openai.com/envs/CartPole-v0/

