Kom godt i gang
---------------

Installer AgentsPy
==================

Åben din terminal på Mac eller Ubuntu, og brug ``pip3`` til at installere AgentsPy:
::

    pip3 install agentspy

Installer AgentsPy i Mu
=======================

1. Klik på tandhjul-ikonet nederst i højre hjørne.
2. Vælg fanen *Third Party Packages*.
3. I tekstfeltet, indtast `agentspy` og klik OK.


Et simpelt projekt med AgentsPy
===============================

Vi vil nu lave en lille model med AgentsPy. Vi laver en såkaldt *predator-prey-model*, altså en model med byttedyr og rovdyr.

Start med at lave en ny python-fil, `prey.py`, og skriv følgende:
::

   from agents import *

   model = Model("Predator-prey-model", 50, 50)

   run(model)

Dette laver en model med 50x50 felter. Hvis du kører scriptet, bør du få et vindue med en sort firkant.

Vi starter med at lave en ``Prey`` klasse til vores byttedyr. Lav den på følgende måde:
::

   class Prey(Agent):
       def setup(self, model):
           pass

       def step(self, model):
           self.direction += randint(-10,10)
           self.forward()

Den skal altså ved hvert trin ("step") ændre sin retning lidt, og bevæge sig fremad.

Lav nu en ``model_setup`` funktion, der "genstarter" modellen og tilføjer 100 nye ``Prey`` agenter:
::

   def model_setup(model):
       model.reset()
       for a in range(100):
           model.add_agent(Prey())

Tilføj så en *Setup* knap til modellen, der kører ``model_setup`` funktionen:
::

   model.add_button("Setup", model_setup)

Prøv at køre scriptet nu, og se, hvad der sker. Du burde have en *Setup* knap, der laver 100 agenter, når den klikkes på.

Vi får nu agenterne til at bevæge sig. Tilføj en ``model_step`` funktion, der får byttedyrene til at køre deres egen ``step`` funktion:
::

   def model_step(model):
       for a in model.agents:
           a.step(model)

Lav nu en *Go* knap, som kan slås til og fra, og som konstant kører ``model_step`` funktionen, når den er slået til:
::

   model.add_toggle_button("Go", model_step)

Nu har vi vores grundlæggende model. Vi vil nu gøre det muligt for byttedyrene at spise græs, og formere sig, hvis de har spist nok græs.

Vi starter med at tilføje græs. Tilføj i ``model_setup``:
::

   for t in model.tiles:
        t.info["grass"] = True
        t.color = (0, 150, 0)

Dette gør sådan, at alle felter starter med at være indikeret som græs. For at de bliver opdateret med en mere "jordlignende" farve, når græsset bliver spist, tilføj følgende i ``step``:
::

   for t in model.tiles:
       if t.info["grass"]:
           t.color = (0, 150, 0)
       else:
           t.color = (80, 80, 0)
           if randint(1, 500) == 500:
               t.info["grass"] = True

Felter, der har ``info["grass"] = True`` bliver nu farvet grønne, imens dem der har ``info["grass"] = False``, bliver farvet brune. Felter, der mangler græs, har desuden hvert step en chance for, at deres græs vokser tilbage igen.

Vi gør nu sådan, at byttedyr kan spise græs, formere sig, hvis de spiser nok, og dø, hvis de ikke får nok at spise. Vi laver først funktionaliteten for at spise. Tilføj i ``Prey`` klassens  ``setup`` funktion:
::

   self.food = 0
   self.time_since_eating = 0
   self.color = (100,100,250)

Vi giver dem en blå farve, så vi kan adskille dem fra de rovdyr, vi senere tilføjer.

Tilføj derefter i ``Prey`` klassens ``step`` funktion:
::

   tile = self.current_tile()
   if tile.info["grass"]:
       self.food += 1
       self.time_since_eating = 0
       tile.info["grass"] = False
   if self.food > 10:
       new_prey = Prey()
       new_prey.x = self.x
       new_prey.y = self.y
       model.add_agent(new_prey)
       self.food = 0
   self.time_since_eating += 1
   if self.time_since_eating > 60:
       self.destroy()

Her gør byttedyret følgende:
* Hvis den står på et felt med græs, spis græsset og læg 1 til "mad-tælleren".
* Hvis den har spist nok græs, lav et nyt byttedyr og sæt "mad-tælleren" til 0.
* Hvis der er gået for lang tid siden den sidst har spist, destruerer den sig selv.

Vi vil gerne gøre det muligt at indstille undervejs i modellen, hvor meget græs, et byttedyr skal spise, før det kan formere sig, og hvor lang tid dyret skal gå uden mad, før at det dør.

I ``model_setup``, tilføj disse to linjer:
::

   model.reproduce_food_count = 10
   model.max_time_since_eating = 60

Erstat så følgende linjer i ``Prey`` klassens ``step`` funktion:
::

   if self.food > 10:
   ...
   if self.time_since_eating > 60:

med disse
::

   if self.food > model.reproduce_food_count:
   ..
   if self.time_since_eating > model.max_time_since_eating:

Tilføj så to justerbare *sliders* ved at indsætte disse to linjer kode, efter at knapperne tilføjes:
::

   model.add_slider("reproduce_food_count", 10, 1, 30)
   model.add_slider("max_time_since_eating", 60, 10, 120)

Nu er vores byttedyr færdigt.

Man kan nu, hvis man vil, tilføje *rovdyr* til simuleringen. Man kan bruge følgende klasse som udgangspunkt:
::

   class Predator(Agent):
       def setup(model):
           self.size = 15
           self.color = (150,0,0)

       def step(model):
           self.direction += randint(-10,10)
           self.forward()

Rovdyret bør have følgende funktionalitet:

* Hvis der er et byttedyr på samme felt som rovdyret, skal det spises (brug en kombination af ``Agent.current_tile()`` og ``Tile.get_agents()`` til at finde ud af, om der er et byttedyr på samme felt).
* Hvis rovdyret har spist nok byttedyr, skal det formere sig (brug samme fremgangsmåde som for byttedyret, der spiser græs).
* Hvis rovdyret ikke har spist noget i lang nok tid, skal det dø (brug også her samme fremgangsmåde som for byttedyret).
