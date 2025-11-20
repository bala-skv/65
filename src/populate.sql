USE mini_world_db;

-- Inserting the only moderator for now
INSERT INTO MODERATORS (Name) VALUES 
('FLDSMDFR'); -- The machine that created the world

-- island regions (must be inserted before INTRUDERS due to FK constraint)
INSERT INTO ISLAND_REGIONS (Region_Name, Threat_To_Intruders) VALUES 
('San Franjose', 1),            -- The ruins of the city, now a LiveCorp base
('Food Animal Jungle', 5),      -- Dense jungle with Bananostriches
('Salsa River', 3),             -- Flowing river of salsa
('Breakfast Bog', 4),           -- Syrup swamps and Mosquitoasts
('Rock Candy Mountain', 8);     -- Dangerous terrain

-- inserting the intruders
INSERT INTO INTRUDERS (Name, Gender, Height, Weight, Intelligence, Time_Of_Entry, Location_Id) VALUES 
('Flint Lockwood', 'M', 183, 75, 160, '08:00:00', 2),
('Sam Sparks', 'F', 170, 60, 155, '08:00:00', 2),
('Chester V', 'M', 190, 70, 168, '07:00:00', 1), -- LiveCorp CEO, entered early
('Earl Devereaux', 'M', 188, 110, 130, '08:05:00', 2),
('Steve', 'M', 60, 10, 85, '08:00:00', 2), -- Monkey (enhanced by translator)
('Barb', 'F', 140, 60, 165, '07:00:00', 1), -- Ape with human intelligence
('Chicken Brent', 'M', 175, 90, 70, '08:10:00', 2);

INSERT INTO FOODIMALS_SPECIES (Species_Name) VALUES 
('Tacodile'),
('Cheespider'),
('Barry'), -- yes, just barry
('Pickle'),
('Hippotatomus'),
('Shrimpanzee'),
('Cantalope'),
('Watermelophant'),
('Flamango'),
('Sasquash');

-- Strawberries (3) and Pickles (4) are shown to live in groups/families
INSERT INTO POPULATORY_SPECIES (Species_Id, Spawn_Per_Birth) VALUES 
(3, 50), -- Barry multiply
(4, 10); -- Pickles have families

INSERT INTO INDIVIDUAL_FOODIMAL_CREATURES (Species_Id, Location_Id, Populatory_Species_Id) VALUES 
(1, 3, NULL), -- A Tacodile in the Salsa River
(2, 2, NULL), -- A Cheespider in the Jungle
(NULL, 2, 3), -- Barry the Strawberry
(NULL, 2, 4), -- Dill Pickle
(NULL, 2, 4), -- Pearl
(5, 3, NULL), -- Hippotatomus
(10, 2, NULL), -- Sasquash hiding in the jungle
(6, 2, NULL), -- Shrimpanzee in the Jungle
(7, 2, NULL), -- Cantalope
(8, 3, NULL), -- Watermelophant in Salsa River
(9, 4, NULL); -- Flamango in Breakfast Bog

INSERT INTO LIVECORP_COLONY (Region_Id) VALUES 
(1); -- Base established in San Franjose

INSERT INTO LIVECORP_CELLS (Colony_Id, Type) VALUES 
(1, 'RESEARCH'),       -- The Bulb
(1, 'MANUFACTURING'),  -- BS-USB factory lines
(1, 'HOUSING'),        -- Thinkronaut sleeping quarters
(1, 'RECREATION');

INSERT INTO INVENTIONS (Item_Owner, Item_Name) VALUES 
(1, 'Spray-On Shoes'),
(5, 'Monkey Thought Translator'), -- steve uses it
(1, 'Celebrationator'), 
(1, 'BS-USB'),
(3, 'LiveCorp Vest'),   -- Chester V's vest
(6, 'LiveCorp Food Bar'), -- orangutan owns this
(3, 'Hologram Emitter'); -- The way Chester travels

INSERT INTO DESCRIPTIONS (Item_Owner_Id, Item_Name, `Description`) VALUES 
(1, 'Spray-On Shoes', 'A spray that creates indestructible shoes. Permanent.'),
(1, 'BS-USB', 'A device capable of rewriting the FLDSMDFR code. Looks like a Celebrationator.'),
(5, 'Monkey Thought Translator', 'Translates monkey thoughts into human speech. Mostly "Hungry" or "Steve".'),
(6, 'LiveCorp Food Bar', 'Soy-based nutrient bar. Tastes bland but efficient.'), -- Added Description
(3, 'Hologram Emitter', 'Projects realistic holograms of Chester V to distract enemies.'); -- Added Description

INSERT INTO INVENTOR (Name, Item_Owner_Id, Item_Name) VALUES 
('Flint Lockwood', 1, 'Spray-On Shoes'),
('Steve', 5, 'Monkey Thought Translator'),
('Flint Lockwood', 1, 'Celebrationator'),
('Flint Lockwood', 1, 'BS-USB'),
('Chester V', 3, 'LiveCorp Vest'),
('Chester V', 6, 'LiveCorp Food Bar'),
('Chester V', 3, 'Hologram Emitter');

-- 1. CREATION OF SPECIES CONCEPTS (Creature_Id is NULL)
INSERT INTO CREATES (Moderator_Id, Species_Id, Creature_Id) VALUES 
(1, 1, NULL), (1, 2, NULL), (1, 3, NULL), (1, 4, NULL), (1, 5, NULL),
(1, 6, NULL), (1, 7, NULL), (1, 8, NULL), (1, 9, NULL), (1, 10, NULL);

-- 2. CREATION OF INDIVIDUAL CREATURES
INSERT INTO CREATES (Moderator_Id, Species_Id, Creature_Id) VALUES 
(1, 1, 1),  -- Tacodile
(1, 2, 2),  -- Cheespider
(1, 3, 3),  -- Barry (Strawberry)
(1, 4, 4),  -- Dill (Pickle)
(1, 4, 5),  -- Pearl (Pickle)
(1, 5, 6),  -- Hippotatomus
(1, 10, 7), -- Sasquash
(1, 6, 8),  -- Shrimpanzee
(1, 7, 9),  -- Cantalope
(1, 8, 10), -- Watermelophant
(1, 9, 11); -- Flamango

-- Cheespiders are weak to the BS-USB (it shuts them down)
INSERT INTO WEAKNESS (Species_Id, Item_Inventor_Id, Item_Name) VALUES 
(2, 1, 'BS-USB');

INSERT INTO ANIMAL (Species_Id, Name) VALUES 
(1, 'Crocodile'),       -- Tacodile
(2, 'Spider'),          -- Cheespider
(5, 'Hippopotamus'),    -- Hippotatomus
(6, 'Chimpanzee'),      -- Shrimpanzee
(7, 'Antelope'),        -- Cantalope
(8, 'Elephant'),        -- Watermelophant
(9, 'Flamingo'),        -- Flamango
(10, 'Sasquatch');      -- Sasquash

INSERT INTO FOOD_ITEM (Species_Id, Name) VALUES 
(1, 'Taco'),            -- Tacodile
(2, 'Cheeseburger'),    -- Cheespider
(3, 'Strawberry'),      -- Barry
(4, 'Pickle'),          -- Pickle
(5, 'Potato'),          -- Hippotatomus
(6, 'Shrimp'),          -- Shrimpanzee
(7, 'Cantaloupe'),      -- Cantalope
(8, 'Watermelon'),      -- Watermelophant
(9, 'Mango'),           -- Flamango
(10, 'Squash');         -- Sasquash

-- Chester V (3) watching a captured Pickle (4) in the Research Cell (1)
-- Barb (6) observing Barry (3) in Research (1)
-- Chester V (3) studying a Tacodile (1) in Manufacturing (2)
INSERT INTO SUSPIOUS_ACTIVITIES (Intruder_Id, Creature_Id, Colony_Id, Cell_Id) VALUES 
(3, 4, 1, 1),
(6, 3, 1, 1),
(3, 1, 1, 2);

-- Flint (1) fights Cheespider (2) using BS-USB in the Jungle (2)
-- Chester V (3) fights Tacodile (1) using LiveCorp Vest (3) in San Franjose (1)
-- Flint (1) fights Tacodile (1) using BS-USB (1) in Salsa River (3)
INSERT INTO COMBAT_EVENT (Intruder_Id, Creature_Id, Item_Owner_Id, Region_Id, Item_Name) VALUES 
(1, 2, 1, 2, 'BS-USB'),
(3, 1, 3, 1, 'LiveCorp Vest'),
(1, 1, 1, 3, 'BS-USB');
