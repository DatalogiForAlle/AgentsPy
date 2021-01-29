.. |SETTINGS| image:: images/godtigang/mu_settings_icon.png
   :height: 20
   :width: 20

.. |PYTHON| image:: images/godtigang/python_mode.png
   :height: 20
   :width: 20

.. |RUN| image:: images/godtigang/mu_run.png
   :height: 20
   :width: 20



Kom godt i gang (Mu-editor)
===========================

Installation af Mu-editoren
---------------------------
Hent og installér denne alpha-udgave af Mu-editoren:

- `Hent Mu-editor til Windows (64 bit) <https://github.com/mu-editor/mu/suites/1782896084/artifacts/34089824>`_
- `Hent Mu-editor til Mac OS X <https://github.com/mu-editor/mu/suites/1782896084/artifacts/34089823>`_
- `Hent Mu-editor til Linux <https://github.com/mu-editor/mu/archive/1.1.0-alpha.2.tar.gz>`_


.. warning:: Nyeste udgave af Mu fra deres hjemmeside er 1,5 år gammel
             og understøtter ikke nyeste udgaver af Mac OS X og heller
             ikke installation af eksterne biblioteker, såsom AgentsPy.

Start Mu
--------
Åbn Mu-editoren. Første gang Mu åbner bliver du bedt om at vælge en
*mode* i dialogen **Select Mode**. Her skal du vælge |PYTHON| **Python
3** og trykke "OK":

.. figure:: images/godtigang/mu_choose_mode.png
    :alt: Mode choice dialog - Python 3
    :width: 400px


Installer AgentsPy
------------------
1. Klik på |SETTINGS|-ikonet nederst i højre hjørne.
2. Vælg fanen *Third Party Packages*.
3. I tekstfeltet, indtast `agentspy` og klik "OK".

.. figure:: images/godtigang/mu_install_agentspy.png
    :alt: Third Party Package installation dialog
    :width: 400px

   
Dit første program med AgentsPy
-------------------------------

Du er nu klar til at skrive dit første lille agent-baserede
program. Du placerer cursoren på linjen efter den hvor der
står ``# Write your code here :-)``,og skriver følgende::

  # Importer biblioteket `agents`
  from agents import *

  # Opret en model og en agent
  min_model = Model("Min første model", 50, 50)
  min_agent = Agent()

  # Tilføj agenten til modellen
  min_model.add_agent(min_agent)

  # Tilføj en `step`-funktion, og en knap der aktiverer den
  def step(model):
    min_agent.forward(10)

  min_model.add_button("Step", step)

  # Kør modellen
  run(min_model)

Når du har skrevet ovenstående, kan du prøve programmet ved at trykke
på Run |RUN|.

Du burde nu se følgende vindue:

.. figure:: images/godtigang/first_model.png
    :alt: Første model
    :width: 400px

Prøv at trykke på knappen "Step" et par gange, for at få din agent til
at tage et skridt.

Linjerne der starter med ``#`` i programmet, bliver forstået som en
kommentar til koden, og får ikke betydning for dit program.



Næste skridt
------------
Tillykke du er nu godt igang! Som det næste vil vi anbefale at du
følger en af vores tutorials her på siden.

Hvis du vil vide mere om selve Mu-editoren, så har holdet bag
Mu-editoren en række tutorials, der kan gøre dig fortrolig med hvordan
Mu fungere, de er på engelsk og du finder dem her:
https://codewith.mu/en/tutorials/
