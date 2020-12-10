AgentsPy: Agent-baseret simulering i Python
===========================================

AgentsPy er et bibliotek til Python, der gør det nemt at arbejde med
agent-baseret simulering i undervisning. Det gør det muligt at forstå
fænomener fra for eksempel biologi, økonomi, fysik, kemi ved at
programmere små simuleringer.

Målet med *AgentsPy* er at gøre det ligeså nemt at arbejde med
agent-baseret simulering som i NetLogo, uden at eleverne skal lære et
separat programmeringssprog. Biblioteket er stadig under udvikling på
Datalogisk Institut, Københavns Universitet.

Som eksempel er her en epidemimodel udviklet i AgentsPy. Hvis du selv
vil prøve kræfter med modellen, så se epidemi-tutorialen nedenfor.

.. image:: images/epidemic.gif

Første skridt
---------------

 ..
    * Kom godt i gang med AgentsPy og Mu-editoren (TODO)
    * Tutorial - Simpel epidemimodel
    * Tutorial - Elektroner og strøm i en ledning
    * Tutorial - Simpelt økosystem med rovdyr og byttedyr

.. toctree::
   :maxdepth: 1

   godtigang
   epidemic
   minerbots

   

Brugerguide
-----------
``AgentsPy`` er et bibliotek, der tilbyder værktøjer, som kan bruges til agent-baseret modellering. Agent-baseret modellering fungerer ved først at opbygge et miljø med agenter, der har en prædefineret opførsel, og så simulere hele systemet baseret på agenternes opførsel. Modellen kan så vise, hvordan agenterne interagerer med hinanden, og systemet som helhed. I ``AgentsPy`` kaldes en agent passende for ``Agent``, et "felt" i miljøet kaldes en ``Tile``, og miljøet som helhed kaldes en ``Model``.

For at give agenterne deres prædefinerede opførsel, skal man kode dem. Dette gøres typisk ved først at definere en klasse, som nedarver fra ``Agent``, for eksempel ``Person`` i epidemimodellen. Heri kan man så definere en ``step`` funktion, der beskriver, hvordan agenten opfører sig i et enkelt simulationstrin. Et eksempel kunne være::

  def step(model):
      self.forward()

hvilket rykker agenten et skridt fremad ved hver trin.

Man kan så lave en ``model_step`` funktion, der simulerer alle agenterne i en model::

  def model_step(model):
      for a in model.agents:
	      a.step(model)

Miljøet ændres oftest som en direkte konsekvens af agenternes opførsel. Man kan for eksempel vælge at farve de felter, en agent har besøgt, røde::

  def step(model):
      self.forward()
	  t = self.current_tile()
	  t.color (255, 0, 0)

``AgentsPy`` tilbyder også muligheden for at justere på simulationen undervejs. Man kan for eksempel bruge en knap til at starte og stoppe simulationen::

  model.add_toggle_button("Go", model_step)

De funktioner, der kan bruges til at tilføje elementer til kontrolpanelet, er:

* ``add_button``: Tilføjer en knap, der kan klikkes på gentagne gange.
* ``add_toggle_button``: Tilføjer en knap, der kan slås til og fra.
* ``add_slider``: Tilføjer en bevægelig knap, der kan bruges til at justere værdien af en numerisk variabel i modellen.
* ``add_checkbox``: Tilføjer et afkrydsningsfelt, der kan bruges til at justere værdien af en sandhedsvariabel i modellen.

Ud over funktioner til kontrolpanelet, er der også funktioner som tilføjer forskellige slags grafer til modellen, som løbende viser data, herunder:

* ``line_chart``: Tilføjer en graf med en eller flere linjer, der beskriver modellens variable over tid.
* ``bar_chart``: Tilføjer et søjlediagram, der viser værdien af modellens variable i øjeblikket.
* ``histogram``: Tilføjer et histogram, der viser, hvordan en bestemt variabel for alle agenterne fordeler sig i givne intervaller.
* ``agent_line_chart``: Tilføjer en graf med en linje for hver agent, der viser værdien af denne variabel over tid.
* ``monitor``: Tilføjer et lille felt til kontrolpanelet, der viser værdien for en enkelt variabel i modellen.

API Dokumentation
-----------------

.. toctree::
   :maxdepth: 1

   agent
   tile
   model
   simplemodel

Kan du ikke finde det du leder efter?
-------------------------------------
Prøv at slå op i registeret eller søg i dokumentationen:

* :ref:`Søg <search>` i dokumentationen

* :ref:`genindex` over alle funktioner og klasser i AgentsPy

.. * :ref:`modindex`


License
-------
AgentsPy er udgivet under GPLv3 licensen. Valget af licens stammer fra
vores brug af PyQt5, som også er udgivet under GPLv3.

.. toctree::
   :maxdepth: 1

   license
