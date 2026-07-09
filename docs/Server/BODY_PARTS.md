** How Body Parts Work **
### Body Parts Table
The body parts table is used by attackable creatures. It is used for determining the amount of base damage they output, and their base armor levels which determine how much damage they receive from physical attacks.

Here is an example body parts table for weenie 5890 - Hoary Mattekar
```
Body Parts        Damage Type        Base Damage        Damage Variance        Base Armor          Height

Head              Pierce                  50                  75%                  250             Medium
Torso             Bludgeon                 0                   0%                  250             Medium
FrontLeg          Pierce                  50                  50%                  250                Low
RearLeg           Pierce                  50                  50%                  250                Low
```
### Attacking

When the creature performs a melee attack, it will select a body part to attack with from the above table.

The body parts it can attack with have Base Damage above 0. For the mattekar, it can attack with: Head, FrontLeg, RearLeg

The height of the attack is determined by the 'Height' column for that body part.

### Defending

If a player performs a melee or missile attack against the mattekar, this table is also used to determine which body part the attack hits

The chance of hitting each body part is based on the height of the attack (low / medium / high), and which quadrant the player is in relation to the mattekar (left/front, right/front, left/back, right/back).

Here are the height quadrants for the above table:
```
Body Parts    HLF    MLF    LLF  |  HRF    MRF    LRF   |  HLB    MLB    LLB  |  HRB    MRB    LRB

Head          40%    10%         |  40%    10%          |                     |
Torso         60%    70%    20%  |  60%    70%    20%   |  90%    70%    30%  |  90%    70%    30%
FrontLeg                         |                      |                     |
RearLeg              20%    80%  |         20%    80%   |  10%    30%    70%  |  10%    30%    70%
```
One thing that should be noted is the numbers in all of these columns always add up to 100%

If the player performs a High attack, and is standing in the Left-Front quadrant of the mattekar, it would use the HLF column to determine the chance for which body part gets hit.

For a High-Left-Front attack, there is a 40% chance of hitting the head, and a 60% chance of hitting the torso.

Thanks to morosity for helping to decode the information in the quadrants table.

### Base Damage / Body Armor:
Note that these are the *base* values for the damage and armor, and go through further modifications throughout the rest of the physical damage system. For example, a creature's Strength will give a significant boost to the amount of damage it does.

Similarly, Body Armor gets affected by 2 more important PropertyFloats:
`PropertyFloat.ArmorModVsType`
`PropertyFloat.ResistType`, with 'Type' being the DamageType, Slash, Pierce, Bludgeon, Fire, Cold, Acid, Electric, Nether.

If a creature gets hit with a physical fire attack on a body part with Body Armor 100, `PropertyFloat.ArmorModVsFire` would be used to determine the body armor against that particular damage type.

If `ArmorModVsFire=0.8`, it would effectively be 80 armor against fire (100 * 0.8)

For physical and magic attacks, `ResistFire` would also be used in the above scenario to scale the damage.

`ResistFire=1.0` would mean no resistance to fire, whereas `ResistFire=0.2` would mean the creature is highly resistant to fire.