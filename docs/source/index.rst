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
   

Brugerguide
-----------
TODO: Brugerguide rundt om de forskellige ting man kan. Måske inspireret af
NetLogo tutorial om predator-prey

 * Hvad er en agent-baseret model?
 * Hvordan beskrives en agents opførsel?
 * Hvordan beskrives miljøet agenterne bevæger sig i?
 * Hvordan tilføjes sliders og ekstra knapper?
 * Hvordan tilføjes forskellige typer af grafer og histogrammer?

   
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
