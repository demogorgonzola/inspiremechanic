# Blueprint Doc to begin Production (Pre-Production Doc)




Development Method: TDD/BDD unit-testing

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
  * Acknowledge passing in time -- Time System
  * Be visually represented -- Graphical System
  * Interaction between entities in space -- Collision System
  * Provide a system of challenge, a challenger -- AI System
  **Note**: The Entity System is crucial to this system as every system will
  serve almost every other system.




## Road Map (i.e. Production Map):

1. Pyglet and PyDbLite installed and fully functioning.
1. **Test functionality of installed Libraries**

### Phase 1, Underlying Systems
1. Develop Entity System using PyDbLite
  - i. Initialize ESDB(Entity System DB) and write base Table
  - ii. Write hook to spawn subset databases of ESDB
    * Subset DB's should just subject ID or primary_key from ESDB
  - iii. Write sanity checks for other systems to check for entity types,
  so they don't execute on missing data groups
  - iv. Write hook to spawn static databases
    * These should just be isolated databases that serves the given system
  - v. Create _seemless_ hook for searching DB
  - **Test Database**
2. Develop Input System using Pyglet
  - i. Define a list of actions available to the player
  - ii. Spawn and Implement Action-Keybind static table
  - iii. Write dummy hooks for _future_* action profiles
    * _Test_: Write temp action profiles for testing
    * Note: use input dummy profiles to test different systems
  - **Test Input on Entities**
3. Develop Time System
    - i. Just make a simple little script that reports time passed for
    others systems to use. This can also track when a system last used it
    to easily give a time-passed result.
    - ii. **Test Time**
4. Develop Graphical System using Pyglet
  - i. Spawn and Implement subset DB for graphical data
    * Use truncated format for gl_shapes and images
  - ii. _Test_: Write temp hooks for input system
  - iii. Write dummy hooks for _future_* collision system
  - Note: **Make sure graphical position reflects logical position**
  - **Test Graphical system with Entities**
5. Develop Collision System
  - Note: Keep looking for a suitable library
  - i. Spawn and Implement subset DB for position, velocity, collisions data
  - ii. Implement simple 2d grid-based lookup system to speed-up entity
  search times.
  - iii. Write simple collision profiles for handling collisions
  - Note: Make sure that when entities are deleted/created they're
  reflected in the Collision system
  - **Test Collisions on Entities**
6. Develop AI System
  - i. Write a smattering of AI profiles
  - ii. Write active loop to push AI profile through each of it's steps
  - iii. Test and tweak AI profiles, until challenging or fun ones arise
  - iv. Repeat until you find at-least 5 good AI profiles to use
  - Note: AI profiles should reflect atmosphere, just don't sacrifice
  viability of challenge or fun
  - **Test AI on Entities, try more complex multi-AI tests**
7. **Perform stress test**

### Phase 2, Overarching Systems
1. Develop Battle System
  - i. Populate the ESDB with "characters"
    * Include "alignment" for AI profile to register target
    * Include "actions" for AI profile to use. weight actions
    * Include Aux Data relevant to other overarching systems
  - ii. Plug Input System into a "character"
  - iii. **Test Battle System for "fun factor"**
2. Develop Health System
  - i. Alter "character" Table by adding Health
  - ii. Alter action profiles to either increase or decrease Health
  - iii. Create context-switch and reset when health is 0
  - iv. **Test Health System for "fun factor"**
  * **Tinker and adjust Battle System and Health System for better experience**
4. Develop Party System
  - i. Should just be a extension of the "alignment" field in "character"
  - ii. **Test Party System for "fun factor"**
  - Note: Later create actual "party" DB to add meta-data to rival party
  groups.
5. **Start play testing and start tweaking for weeks, months, however long**
  - **DURING THIS PHASE, IF THE OVERARCHING SYSTEMS ARE NOT-FUN/TRASH,
  QUICKLY THROW THEM OUT (Archive them), START OVER AND WRITE NEW PLAN**

### Phase 3, Core Concepts
* Do review over overarching systems to see if they reflect Core Concepts.
If not, either find compromise or tweak overarching systems to find the
core concepts. Overall, this shouldn't be radically different from the
goal. However, as long as a fun experience has been made, then the
core concepts can be abandoned for a later time.

### Phase 4, **JUICE**
* **_FUTURE REVISION_**
