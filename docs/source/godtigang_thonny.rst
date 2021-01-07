.. |RUN| image:: images/thonny/run.jpg
   :height: 20
   :width: 20


Kom godt i gang (Thonny)
===========================

Installation af Thonny
----------------------
Hent og installer Thonny fra: https://thonny.org/

Åbn Thonny, du burde få et vindue op der ser nogenlunde sådan her ud:

.. todo:: SCREENSHOT

Installer AgentsPy i Thonny
---------------------------

1. Vælg **Tools** -> **Manage Packages**.
2. Skriv ``agentspy`` i feltet og klik på **Search on PyPI**.
3. Klik på **AgentsPy** og derefter **Install**.

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

..
     from agents import *

     min_agent = Agent()

     def setup(model):
       model.add_agent(min_agent)

     def step(model):
       min_agent.forward()

     min_model = SimpleModel("Min første model", 60, 60, setup, step)
     run(min_model)

Når du har skrevet ovenstående, kan du prøve programmet ved at trykke
på Run |RUN|.

.. todo:: run button icon

Du burde nu se følgende vindue:

.. todo:: SCREENSHOT

Prøv at trykke på knappen "Step" for at få din agent til at tage et skridt.


Næste skridt
------------
Tillykke du er nu godt igang! Som det næste vil vi anbefale at du
følger en af vores tutorials her på siden.

Hvis du vil vide mere om selve Mu-editoren, så har holdet bag
Mu-editoren en række tutorials, der kan gøre dig fortrolig med hvordan
Mu fungere, de er på engelsk og du finder dem her:
https://codewith.mu/en/tutorials/
