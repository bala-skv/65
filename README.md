# Cloudy With a Chance of Meatballs Database CLI

## **Video Link:** https://drive.google.com/file/d/1WKVxFjf6I7ei_Hda66xTHsM7vdqtPGEd/view?usp=sharing

A command-line interface application for managing a the Cloudy with a Chance of Meatballs database with intruders, foodimals, regions, and inventions.

- **Team Number:** 65
- **Team Members:**
    - Kaushik Yadala [2024101123]
    - Mukund Hebbar [2024101037]
    - Balasubramanian K [2025121002]

## Features and Commands

### Main Menu Commands

1. **Insert data** - Allows you to insert new records into any database table. Prompts for table selection and then guides you through entering values for each column, showing reference data for foreign keys.

2. **Update data** - Updates existing records in a selected table. Displays current table data, prompts for WHERE conditions to identify records, and then allows you to specify which columns to update with new values.

3. **Delete data** - Deletes records from a selected table. Shows current table data, prompts for WHERE conditions to identify records to delete, and requires confirmation before executing the deletion.

4. **View tables** - Displays all data from a selected table in a formatted view with column headers, showing NULL values where applicable, and includes a row count.

5. **Retrieval Operations** - Opens a submenu with specialized query operations (see Retrieval Operations below).

6. **Analysis Reports** - Opens a submenu with comprehensive analytical reports (see Analysis Reports below).

7. **Exit** - Closes the database connection and exits the application gracefully.

### Retrieval Operations Submenu

1. **Find Species by Food Item** - Searches for Foodimal species by food item keyword. Prompts for a keyword (e.g., 'taco', 'pizza') and displays all species that contain that food item along with species IDs and food item names.

2. **Search Invention Descriptions** - Searches for inventions by description keyword. Prompts for a keyword and performs a case-insensitive search through invention descriptions, displaying matching inventions with their owners and full descriptions.

3. **Count Foodimals of a Specific Species** - Counts the total number of individual foodimal creatures of a specific species. Prompts for species name and displays the count of living instances.

4. **Calculate Average Intruder Intelligence** - Calculates the average intelligence of intruders associated with a specific LiveCorp colony. Shows available colonies, prompts for colony ID, and displays the average intelligence and total intruder count.

5. **Find the Most Dangerous Region** - Identifies and displays the island region(s) with the highest threat level to intruders, showing region ID, name, and threat value.

6. **Display Intruder Threat Profiles** - Lists all intruders with their names, intelligence levels, and calculated threat status. Threat status is calculated using the formula: Intelligence² + Height - Weight/Height, sorted from highest to lowest threat.

7. **List Foodimal Species and Recipes** - Displays all Foodimal species along with their "recipes" showing the animal and food item components that make up each species, with both summary and detailed breakdown views.

8. **Identify High-Threat Intruders** - Finds intruders whose threat status exceeds a user-specified threshold. Prompts for a critical threshold value and displays detailed information about all intruders above that threat level.

9. **Find Foodimals in a Specific Region** - Locates all individual foodimal creatures in a specified region. Shows available regions, prompts for region name, and displays all foodimals with species information and distribution statistics.

10. **List Inventions Effective Against a Species** - Shows all inventions that are effective against a specific foodimal species. Displays available species, prompts for species name, and lists all inventions with their owners that can be used against that species.

11. **Back to Main Menu** - Returns to the main menu.

### Analysis Reports Submenu

1. **Intruder Threat Assessment by Region** - Generates a comprehensive report of all intruders with their physical stats, intelligence, location, and calculated threat levels. Includes both summary table and detailed breakdown with threat level calculation formula.

2. **Foodimal Defensive Readiness Report** - Analyzes foodimal species distribution across all regions, showing the number of different species and total units in each region. Provides summary statistics and detailed breakdown by region.

3. **Combat Effectiveness Analysis** - Analyzes combat events to show which intruders use which inventions and how frequently. Displays summary tables, detailed breakdowns by intruder, and identifies the top 5 most used inventions across all combat events.

4. **Back to Main Menu** - Returns to the main menu.
