# Blueprint Doc to begin Production (Pre-Production Doc)




Development Method: BDD unit-testing

Language(s) Used: Python

Libraries Used:
  * [Pyglet](https://pyglet.readthedocs.io/en/pyglet-1.2-maintenance/index.html)
    * Supports Graphical System
    * Supports Input System
  * [PyDbLite](https://pydblite.readthedocs.io/en/latest/index.html)
    * Supports Entity System




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
  * A way of punching kids (Battle System)
  * Emotional State (Health System)
  * Character Alignment (Party System)

Underlying Systems (Systems that support Overarching systems):
  * Keep track of entities and query certain characteristic -- Entity System
  * Involve player input -- Input System
  * Be visually represented -- Graphical System
  * Interaction between entities in space -- Collision System
  * Provide a system of challenge, a challenger -- AI System
  **Note**: The Entity System is crucial to this system as every system will
  serve almost every other system.




## Road Map (i.e. Production Phase Map):

    1. Pyglet and PyDbLite installed and fully functioning.
    1. **Test functionality of installed Libraries**

### Phase 1, Underlying Systems
    1. Develop Entity System using PyDbLite
      1. Initialize DB and write base Tables
      1. Create hooks for other systems to construct specialized tables
      1. Create sanity check method for existence of certain Tables, so
      some systems require certain "Entity's" to execute
      1. Create **seemless** hook for searching DB
      1. Do final testing
    1. **Test Database**
    1. Develop Input System using Pyglet
      1. Define a list of actions available to the player (Singleton Entry)
      1. Create Action-Keybind Table in Entity System
      1. Create dummy hooks for _future_* action system
          Note: use input dummy hooks to test different systems
    1. **Test Input on Entities**
    1. Develop Graphic System using Pyglet
      **_<REVISIT AFTER PYGLET GRAPHICAL MOCKUP>_**
    1. **Test Graphical system with Entities**
    1. Develop Collision System
        Note: Keep looking for a suitable library
      1. Implement Table for position and velocity for Entity System
      1. Implement Table for collision shape for Entity System
      1. Create simple 2d grid-based lookup system to speed-up entity
      search times.
      1. Implement Table for collisions that have occurred
      1. Create hooks for Collision Handlers to resolve collisions
      Note: Make sure that when entities are deleted/created they're
      reflected in the Collision system
    1. **Test Collisions on Entities**
    1. Develop AI System
      1. Implement a smattering of AI profiles
      1. Test and tweak AI profiles, until challenging or fun ones arise
      1. Repeat until you find at-least 5 good AI profiles to use
      1. Implement AI profile Table to Entity System
      Note: AI profiles should reflect atmosphere, just don't sacrifice
      viability of challenge
    1. **Test AI on Entities, try more complex multi-AI tests**
    1. **Perform stress test**

### Phase 2, Overarching Systems
    1. Develop Battle System
      1. Create template "character" Table to populate
        1. Include "alignment" for AI profile to register target
        1. Include "actions" for AI profile to use, weight actions
      1. Populate Entity System with "characters"
        1. Make sure to include AI Profile (Player Profile if player)
        1. Include Aux Data relevant to other overarching systems
    1. **Test Battle System for "fun factor"**
    1. Develop Health System
      1. Alter "character" Table by adding Health
      1. Alter confirmed-action to either increase or decrease Health
      1. Create context-switch and reset when health is 0
    1. **Test Health System for "fun factor"**
    1. **Tinker and adjust Battle System and Health System for better experience**
    1. Develop Party System
      1. Should just be a extension of the "alignment" field in the "character"
      Table
      Note: Later create actual "party" Table to add meta-data to rival party
      groups.
    1. **Test Party System for "fun factor"**
    1. **Start play testing and start tweaking for weeks, months, however long**

    **DURING THIS PHASE, IF THE OVERARCHING SYSTEMS ARE NOT-FUN/TRASH,
    QUICKLY THROW THEM OUT (Archive them), START OVER AND WRITE NEW PLAN**

###Phase 3, Core Concepts
    Do review over overarching systems to see if they reflect Core Concepts.
    If not, either find compromise or tweak overarching systems to find the
    core concepts. Overall, this shouldn't be radically different from the
    goal. However, as long as a fun experience has been made, then the
    core concepts can be abandoned for a later time.

###Phase 4, **JUICE**
    **_<FUTURE REVISION>_**
