# Blueprint Doc to begin Production (Pre-Production Doc)

#####

Language(s) Used: Python

Libraries Used:
  * [Pyglet](https://pyglet.readthedocs.io/en/pyglet-1.2-maintenance/index.html)
  * [PyDbLite](https://pydblite.readthedocs.io/en/latest/index.html)

#####

Kind of Game:
  2d-top-down arena-styled party-based battler. That sounds like shitty
  buzz-words. The player fights with a team of chosen party members to
  try and beat another team by way of using team-tactics with autonomous
  party members via a Suggestion and Cooperation Mechanic.

Core Concepts of Game:
  * Friends (Party Members) are autonomous
  * Beating up other kids and getting beaten is good
  * Emotional state of yourself and others need care

Overarching Systems (Systems that support the Concepts):
  * Character Alignment (Party System)
  * Emotional State (Health System)
  * A way of punching kids (Battle System)

Underlying Systems (Systems that support Overarching systems):
  * Move and be represented in space -- Spatial System
  * Be visually represented -- Graphical System
  * Involve player input -- Input System
  * Provide a system of challenge, a challenger -- AI System
  * Include moving dynamic entities -- NPC System
  * Keep track of entities and query certain characteristic -- Entity System
  **Note**: The Entity System is crucial to this system as every system will
  serve almost every other system.
