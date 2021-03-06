Del 2: En model over smittespredning
====================================

Du har nu din model, og dine agenter - men hvordan skal du simulere
sygdommen? Du grubler meget længe, indtil at en anden kollega
fortæller dig om
`SIR-modellen <https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model>`_ [#]_ :
en matematisk model, som bruges til at modellere sygdomsspredning.

.. role:: susceptible
.. role:: infectious
.. role:: recovered

.. raw:: html

    <style>
    .susceptible { color:green; }
    .infectious { color:red; }
    .recovered { color:blue; }
    </style>

Modellen har tre kategorier, som den opdeler folk i:

 * :susceptible:`Susceptible`: Folk i denne gruppe er modtagelige, og kan blive smittet, hvis de kommer i kontakt med en, der bærer sygdommen.
 * :infectious:`Infectious`: Folk i denne gruppe er blevet syge, og kan smitte folk, der er modtagelige.
 * :recovered:`Recovered`: Folk i denne gruppe har haft sygdommen og er blevet raske og immune, og kan derfor ikke længere hverken smitte eller blive smittet.

En person kan altså kun være i én kategori ad gangen, og deres tilstand vil have mønsteret:

 :susceptible:`Susceptible` → :infectious:`Infectious` → :recovered:`Recovered`

Du tænker, at dette er lige den model, du har brug for, og går straks i gang med at kode.




Fra agent til person
--------------------

Lige nu er vores agenter "bare" agenter. Vi vil gerne gøre dem lidt
mere avancerede, sådan at de blandt andet kan selv kan holde styr på,
hvilken kategori af SIR-modellen, de er i.

Tilføj, over din ``model_setup``-funktion (men under dine imports), følgende kode::

  class Person(Agent):
      def setup(self,model):
          self.category = 0

      def step(self,model):
          self.direction += randint(-10,10)
          self.forward()

Ovenstående kode definerer en *klasse*, som har noget opførsel
beskrevet i sine egne funktioner ``Person.setup`` og ``Person.step``.

Ændr så ``model_setup``-funktionen til::

  def model_setup(model):
      model.reset()
      for person in range(100):
          model.add_agent(Person())

Nu tilføjer vi altså personer i stedet for "bare" normale agenter.

Bemærk, at indholdet i ``Person.step`` lidt ligner det, der står i
``model_step``-funktionen i forvejen. Faktisk kan vi nu også ændre i
``model_step``-funktionen, sådan at der i stedet står::

  def model_step(model):
      for person in model.agents:
          person.step(model)

Prøv nu at køre modellen igen. Hvis du har gjort det rigtigt, burde den ikke se anderledes ud end før.

Kategorier
----------
For ikke at skulle skrive navnene på kategorierne hele tiden, bruger vi i stedet tal, sådan at

============    =====
  Kategori        #
============    =====
Susceptible       0
Infectious        1
Recovered         2
============    =====

Tilføj nu en ``infect``-funktion til ``Person``, som har følgende udseende::

  def infect(self, model):
      self.color = (200, 0, 0)
      self.category = 1

Funktionen giver agenten en rød farve, og sætter den i kategori 1.

Omskriv så ``Person.setup`` til følgende::

  def setup(self,model):
      self.category = 0
      self.color = (0, 200, 0)
      if randint(1,50) == 1:
          self.infect(model)

Vi gør her sådan, at de fleste agenter starter med at være raske og
have en grøn farve, men en lille del (omkring 2%) starter med at være
syge og have en rød farve.

.. image:: ../images/epidemic/epidemic-2.2.png
   :height: 400

Smittespredning
---------------

Ideen med modellen er, at de syge agenter skal smitte de raske
agenter. Vi gør det på den måde, at en syg agent smitter alle raske
agenter, som er indenfor en bestemt afstand af den. Tilføj følgende
kode i bunden af ``Person.step``-funktionen::

  if self.category == 1:
      for agent in self.agents_nearby(12):
          if agent.category == 0:
              agent.infect(model)

Koden siger, at hvis agenten er i kategori 1 (altså syg), så smitter
den alle agenter indenfor en radius af 12 (agentens egen radius er på
4).

.. image:: ../images/epidemic/epidemic-2.3.png
   :height: 400

Immunitet
---------

Lige nu kan vores model vise 2 af de 3 kategorier, altså "susceptible"
og "infectious". Som det sidste led i modellen, skal agenter i
"infectious" kategorien flyttes til "recovered" kategorien, når der er
gået et stykke tid.

Tilføj først først denne funktion ``turn_immune`` til
``Person``::

  def turn_immune(self, model):
      self.color = (0,0,200)
      self.category = 2

Denne minder om ``Person.infect``, men i stedet for at personen
bliver rød og inficeret, bliver den blå og opnår immunitet.

Tilføj så denne linje til ``Person.infect``::

  self.infection_level = 600

Idéen med ``infection_level``-variablen er, at den langsomt tæller
ned, og, når den rammer 0, bliver den inficerede agent immun. Det gør
vi ved at tilføje disse tre linjer i bunden af ``if``-sætningen i
``Person.step``::


  self.infection_level -= 1
  if self.infection_level == 0:
      self.turn_immune(model)

``if``-sætningen burde til slut gerne se således ud::

  if self.category == 1:
      for agent in self.agents_nearby(12):
          if agent.category == 0:
              agent.infect(model)
      self.infection_level -= 1
      if self.infection_level == 0:
          self.turn_immune(model)

Når du kører programmet, burde du nu have en færdig implementation af SIR-modellen.

Grafer
------
Til slut vil vi gerne se, om vores model forløber på samme måde som
SIR-modellen. Det gør vi ved at indsætte en graf, som viser
fordelingen af agenter over tid.

Ideen med grafen kommer til at være, at vi optæller antallet af
agenter i hver kategori, og så får grafen til at vise tre linjer, som
viser antallene i hver kategori som funktion af tid.

Begynd først med at indsætte disse tre linjer i
``model_setup``-funktionen, lige efter du har kaldt
``model.reset()``::

  model.Susceptible = 0
  model.Infectious = 0
  model.Recovered = 0

Vi får agenterne selv til at tildele sig de forskellige kategorier, så vi lader alle tre starte med at være 0.

Tilføj øverst i ``Person.setup``::

  model.Susceptible += 1

Tilføj øverst i ``Person.infect``::

  model.Susceptible -= 1
  model.Infectious += 1

Tilføj øverst i ``Person.turn_immune``::

  model.Infectious -= 1
  model.Recovered += 1

Nu har vi styr på dataen til vores model. Programmet skal dog lige
vide, at det skal opdatere grafen, imens *Go*-knappen holdes
inde. Tilføj denne linje nederst i ``model_step``-funktionen::

  model.update_plots()

Det eneste, vi mangler nu, er at tilføje graferne. Indsæt disse
linjer, lige efter der hvor du tilføjer knapperne til modellen::

  epidemic_model.line_chart(["Susceptible","Infectious","Recovered"],[(0, 200, 0),(200, 0, 0),(0, 0, 200)])
  epidemic_model.bar_chart(["Susceptible", "Infectious", "Recovered"], (200, 200, 200))

Prøv at køre modellen, indtil der ikke er flere inficerede agenter tilbage, og sammenlign så den graf du får med den, der er på `Wikipedia-siden for SIR-modellen <https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model}{>`_.

.. image:: ../images/epidemic/epidemic-2.4.png
   :height: 400

Forskelle mellem SIR-modellen og den agent-baserede model
---------------------------------------------------------
Du har nu udviklet en agent-baseret model, der approksimerer SIR-modellen. Men hvad er fordelene og ulemperne egentlig ved at bruge de to forskellige modeller?

**SIR-modellen**
 * `Fordele`: Da SIR-modellen er baseret på et sæt matematiske formler, er det nemmere at beregne direkte på modellens resultater, samt at kombinere og sammenligne den med andre matematiske modeller. Derudover er modellen også konsistent: hvis man giver det samme input flere gange til den samme model, vil man altid få det samme output.
 * `Ulemper`: SIR-modellen er en meget generaliserende model, da den antager, at alle individer opfører sig ens, for eksempel ved at alle har samme infektionsrate og sygdomsforløb. Man kan approksimere forskellige opførsler ved at justere på parametrene, men det er svært at sige, hvor meget det hænger sammen med virkeligheden.

**Agent-baseret model**
 * `Fordele`: Med den agent-baserede model er det nemmere at modellere både forskellige typer adfærd og karakteristika for både personer og virus, for eksempel superspredere, virusmutationer, social afstand, og så videre. Selvom modellen aldrig kan være helt præcis, kan den stadig give god indsigt i, hvilken indflydelse disse faktorer har på epidemien, og hvordan de interagerer med hinanden.
 * `Ulemper`: Den agent-baserede model har en stor tilfældighedsfaktor i sig. Agenterne starter tilfældige steder, bevæger sig tilfældigt, og smittes tilfældigt. Derfor er det nødvendigt at køre modellen mange gange for at fastlægge endelige resultater, og selv da kan man ikke garantere det. Derudover er det også svært at kombinere den agent-baserede model med andre eksisterende matematiske modeller.

Opgave 1
--------
Tilføj en tilfældighed, så smitte ikke spredes med 100% sandsynlighed,
men fx kun 20% sandsynlighed, når to agenter mødes.

*Hint:* Brug ``randint()``-funktionen, som vi også har brugt tidligere.

Opgave 2
--------
Overvej hvordan vi kan lave en type agent “Superspreder”, der enten:

  - Bevæger sig hurtigere (flere kontakter)

  - Smitter mere end andre agenter (høj smitterate)


Samlet kode
-----------
Her er den samlede kode du gerne skulle have nu::

  from agents import Model, Agent, run
  from random import randint


  class Person(Agent):
      def setup(self, model):
          model.Susceptible += 1
          self.category = 0
          self.color = (0, 200, 0)
          if randint(1, 50) == 1:
            self.infect(model)

      def step(self, model):
          self.direction += randint(-10, 10)
          self.forward()
          if self.category == 1:
              for agent in self.agents_nearby(12):
                  if agent.category == 0:
                      agent.infect(model)
              self.infection_level -= 1
              if self.infection_level == 0:
                  self.turn_immune(model)

      def infect(self, model):
          model.Susceptible -= 1
          model.Infectious += 1
          self.color = (200, 0, 0)
          self.category = 1
          self.infection_level = 600

      def turn_immune(self, model):
          model.Infectious -= 1
          model.Recovered += 1
          self.color = (0, 0, 200)
          self.category = 2


  def model_setup(model):
      model.reset()
      model.Susceptible = 0
      model.Infectious = 0
      model.Recovered = 0
      for person in range(100):
          model.add_agent(Person())


  def model_step(model):
      for person in model.agents:
          person.step(model)
      model.update_plots()


  epidemic_model = Model("Epidemimodel", 100, 100)

  epidemic_model.add_button("Setup", model_setup)
  epidemic_model.add_button("Go", model_step, toggle=True)
  epidemic_model.line_chart(
      ["Susceptible", "Infectious", "Recovered"], [(0, 200, 0), (200, 0, 0), (0, 0, 200)]
  )
  epidemic_model.bar_chart(["Susceptible", "Infectious", "Recovered"], (200, 200, 200))

  run(epidemic_model)

