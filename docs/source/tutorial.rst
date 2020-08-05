Tutorial
========

This tutorial intends to showcase some of the functionalities provided by the ``AgentsPy`` library.

We will develop a simulation consisting of miner robots on a remote planet collecting resources and avoiding hostile aliens.

Basics
------
Begin by creating a file called ``minerbots.py``. Then, in the top of the file, import the library by writing:
::

   from agents import *

Now we can create a model. Do this by writing:
::

   miner_model = Model("MinerBots",100,100)

This creates a model named ``miner_model``, and gives it a size of 100 x 100 tiles.

To run the model, simply add the line:
::

   run(miner_model)

This line should generally be the last one in your file.

Running the python file, you should see a window with a black square and the name "MinerBots".

