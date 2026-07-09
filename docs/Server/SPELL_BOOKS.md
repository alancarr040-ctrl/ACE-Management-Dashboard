### Spell Books and Spell probability.
First off you have to know what spells the mob casts.  LSD has a spell book, but keep in mind that it only lists Debuffs.  It does not have offensive spells.  Just do a Control+F to find the spells.  You will also need the spell ID, which is to the right of the spell name.  You can find it here: [LSD Spell Book](https://docs.google.com/spreadsheets/d/1qQBNdNneoLIv66WUMFAScfvVpJhNpbTZ9Tn526o2vKg/edit#gid=61737657)


For finding the offensive spells, currently you will have to spend time searching through pcaps to find them (hopefully soon there will be an offensive list).  Best way is to search for the creature name, and just hitting F3 through the pcap noting what spells the creature casts.  Its tedious, but the only way to find out.

Once you know the spells and spell IDs, (if you need to find the spell ID, you can find them here: [Spell IDs](https://github.com/harliq/AceWiki/blob/master/spell_IDs/spelldump.txt))

### Monster spell books - probability

Once you have all of that information, next thing is to figure out the probability of the spells.  This is pretty much a guess, although watching videos may help.  Once you have a general idea of the probability (ie. percent), here is how you write the percent.  Monster spell books have their probabilities written with a 2.0 base. To write an 8% probability, instead of writing 0.08, you would put 2.08:

```
INSERT INTO `weenie_properties_spell_book` (`object_Id`, `spell`, `probability`)
VALUES (165008,  4447,    2.08)  /* Incantation of Frost Bolt */
```

If you want to add another spell with a 4% probability, that would be 2.04:

```
INSERT INTO `weenie_properties_spell_book` (`object_Id`, `spell`, `probability`)
VALUES (165008,  4447,    2.08)  /* Incantation of Frost Bolt */
     , (165008,  2125,    2.04)  /* Incantation of Frost Arc */
```

Another important concept of monster spellbook probability tables is that each spell is rolled for individually, in the order it appears in the spellbook

Consider this probability table, for example:

```
INSERT INTO `weenie_properties_spell_book` (`object_Id`, `spell`, `probability`)
VALUES (165008,  4447,    2.50)  /* Incantation of Frost Bolt */
     , (165008,  2125,    2.50)  /* Incantation of Frost Arc */
```

This monster can cast 2 spells, each listed with a 50% probability

Each time the monster attacks, it will first try to roll for Incantation of Frost Bolt, with a 50% chance. If this succeeds, it casts Incantation of Frost Bolt. If the roll failed, it will then try another roll for Incantation of Frost Arc, with a 50% chance.

If you are thinking this monster will cast spells 100% of the time, or that the spells will both be cast with equal probability overall, then you are probably thinking of the probabilities as independent events, where actually they are dependent events. The latter spells are dependent on the rolls for the previous spells in the list not occurring.

For the above probability table, the monster actually has a 75% chance of casting a spell overall.

In terms of independent events, it has a 50% chance of casting the first spell, and a 25% chance of casting the second spell

To help with converting between independent and dependent probability tables, here is a small program:

https://pastebin.com/XTtEF9cY