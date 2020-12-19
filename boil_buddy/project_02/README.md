--------------------------------------------------------------------------
Boil Buddy: Text message alerts for a boiling pot of water
--------------------------------------------------------------------------
Copywright 2020 Nicolas Escobar
nick[dot]bob[dot]escobar[at]gmail[dot]com

This is the Boil Buddy PCB Design! Boil Buddy uses a piezoelectric disc to sense vibrations in the pot as water boils and sends a text alert.
This PCB was adapted from a PocketBeagle project and thus makes use of many chips found on that board, including the Octavo Systems OSD353558 Microprocessor.
In converting to the PCB design, my goal was to eliminate extraneous components from the PocketBeagle to cut down on costs and size. However, I learned that
the PocketBeagle doesn't really have much that I don't need built into it (unless I swap the CPU) and that it would be *much* more cost-efficient to make a shield
for the existing board.

The 'boil_buddy' folder on GitHub should contain software used to run the Boil Buddy, at least for the prototyped version. I'm unsure on how to adapt it to a
standalone device, though I figure that I'd be using much of the same Debian backbone because I've kept most of the same hardware. 