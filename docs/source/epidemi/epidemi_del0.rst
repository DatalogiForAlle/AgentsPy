Del 0: Programmering i Python
=============================

*Hvis du ikke endnu har installeret en editor, så brug en af følgende guides:*

.. toctree::
   :maxdepth: 1

   ../godtigang_mu
   ../godtigang_thonny


Turtle-biblioteket
------------------
Som indledning til at bruge det agent-baserede bibliotek ``AgentsPy`` vil vi bruge et andet bibliotek, kaldet ``turtle``. Et bibliotek er en samling af eksterne funktioner, som man kan vælge bruge i sit eget program.

Start med at åbne din editors *REPL*:

 * I Mu-editoren skal du klikke på knappen i den øverste bjælke, hvor der står **REPL**.
 * I Thonny burde vinduet allerede være åbent nederst med titlen **Shell**, ellers kan du åbne det ved at klikke på **View** og derefter **Shell**.

Der er som udgangspunkt to måder at køre Python-kode på. Den første er at indtaste koden i en fil, og så køre hele filen (som man gør i "Kom godt i gang"-guiden). Den anden måde er at bruge en *REPL*, hvor man kan indtaste og køre enkelte linjer kode ad gangen.

Prøv som eksempel i din *REPL* at indtaste::

  >   x = 2
  >   x + x

Du burde gerne få resultatet 4.

Lad os nu prøve at bruge ``turtle`` biblioteket. For at bruge et bibliotek, skal man først *importere* det. Gør det ved i dit *REPL* at skrive::

  >   from turtle import *

Stjernen ``*`` indikerer, at vi gerne vil importere alle funktioner fra biblioteket.
Efter importeringen kan du nu fremover i din REPL (indtil at du genstarter din editor) bruge funktioner fra ``turtle`` biblioteket.

Lad os nu lave en "turtle". En turtle er en lille agent (markeret med en pil), som kan flyttes rundt på en skærm ved at kalde nogle bestemte funktioner. Lav først en turtle i dit *REPL* ved at skrive::

  >   t = Turtle()

Når du har skrevet dette, burde der komme et vindue frem med en hvid baggrund og en sort pil i midten. Den sorte pil er dit "turtle-objekt", som kan refereres med variablen ``t``. Prøv derfor nu at skrive::

  >   t.forward(100)

Du burde gerne se din turtle rykke sig lidt fremad. Giv den lidt flere instrukser:
::

  >   t.left(90)
  >   t.color("red")
  >   t.forward(200)

Det her er bare nogle af de funktioner, man kan bruge på sin "turtle". Agenterne fra ``AgentsPy`` har nogle lignende funktioner.
