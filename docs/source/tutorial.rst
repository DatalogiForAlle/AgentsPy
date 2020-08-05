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

Setup
-----
While we add functionality to our model, we will also add a bit of UI that makes it easier to control the flow of the simulation. First, we want to make starting and restarting the model simple, so we will create a **Setup** button. Start out by creating a function, also named 


\subsection{Setup}
Vi vil gerne gøre det nemt at starte og genstarte modellen, når vi skal køre den. Derfor laver vi en \textit{setup}-knap. Lav først en funktion der hedder \texttt{setup}, der tager en model som argument, og som ser således ud:
\begin{lstlisting}
  def setup(model):
      model.reset()
\end{lstlisting}
Indtil videre skal den bare "resette"\ modellen, altså fjerne alle agenter og nulstille alle felter (selvom der ingen er af dem endnu).\\
Tilføj nu følgende linje kode mellem oprettelsen af modellen og \texttt{run}-funktionen:
\begin{lstlisting}
  miner_model.add_button("Setup", setup)
\end{lstlisting}
Modellen burde nu have en ekstra "Setup" knap (der ikke gør noget, når man klikker på den).
