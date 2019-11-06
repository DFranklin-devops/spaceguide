# spaceguide
Assistant to help align car in the garage

## Motivation
Want to know how far in to pull to (a) leave enough space to open hatch/tail with garage door closed, and (b) leave space between front of vehicle and wheelbarrow, snowblower, recycle bin, etc 

## Version as of Nov 6 2019:
1. Blink green when vehicle is far away (further than about 6.5 feet)
2. Blink yellow when vehicle between 6.5 and 5.8 feet (approx)
3. Solid red when vehicle at 5.5 feet plus or minus a few inches (approx)
4. Flashing red when vehicle closer than 5.2 feet (approx)

## Upgrades / next steps:
- Make it standalone (no need for a full-blown Pi, able to run on batteries)
- Mountable enclosure
- Make it configurable without having to rewrite code. Perhaps a learn/set button for distance, but what about sensitivity range (e.g. the plus or minus a few inches)
- Consider dual sensor system for front and back

Credit: https://github.com/matthewf01/pi-parking-sensor
