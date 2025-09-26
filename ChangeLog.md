All noteable changes to this project will be documented in this file



## Unreleased
- Features dealing with saving preset weapons or enemies for quickloading their stats (This will take a while becasue it has to deal with incoperation into my larger project)

## [1.0.0] 9/12/25


## [1.1.0] 9/14/25
### Additions
- Toughness to reduce final damage
- Agility Debuff Immunity charges to stop the dodge / parry debuff from applying


### Changes
- Agility decreases with each dodge / parry attempt
- optimized some code


## [1.2.0] 9/15/25
### Additions
- Protection against incorect input types
- Says the location and sublocation each successful shot

### Changes
- Optimized some more code


## [1.2.5] 9/19/25
### Additions
- Total damage tracker that goes down with a successful dodge / parry
- Screen resize capability (only for the main page)

### Changes
- More code Optimizations


## [1.3.0] 9/22/25
### Additions
- Debuffs from hitting a sublocation
- Dark Mode
- Instruction Page
- Halo Font to titles and subtitles
- Fire modes for Ranged and Melee
- Ammo Tracker
- Zeros now disappear when you click on an entry and will re-appear if you leave the entry with nothing in it

### Changes
- Sublocation and Debuffs only apply on a crit
- Added resize functionality to the calculation and instruction pages
- Code optimization and improved formatting
- Moved the executable file to the top level of the project

### Fixes
- Vehicle damage not calculating


## [2.0.0] (technicaly 1.0.0) 9/24/25
Version number note: Since the previous 1.x version were not public I see them as 0.x so the new 2.x is more like 1.x and I will use that convention in the future
### Additions
- Change Log file
- README file
- License file
- Imported everything to GitHub
- Imported everything to itch.io
- More optimzations, mainly behind the scenes files logic

### Changes
- Now only shoots the lowest value between the expected shots and rounds left in the weapon
- Changed project name from 'Halo Combat Program' to 'Halo: Combat Resolved'
- Rebuilt the .exe with current changes

### Fixes


## [1.0.1] 9/26/25
### Additions
- Added some code that pulls the foucs when a button or screen is cliked to fix "None" soemtimes being inputted into the calcukation due to a entry that previously had a zeor in it still being focused on

### Changes
- Made some design changes to make the layout of pages look better

### Fixes
- Halo font now works when opening the project through the .exe file
- Fixed spelling mistakes in various parts of the project