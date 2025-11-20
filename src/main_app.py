#!/usr/bin/env python3

import mysql.connector
from mysql.connector import Error
import sys
from typing import Optional, Dict, List, Any
import re

class DatabaseCLI:
    def __init__(self):
        self.connection: Optional[mysql.connector.MySQLConnection] = None
        self.cursor = None
        
        self.tables = [
            'INTRUDERS', 'MODERATORS', 'FOODIMALS_SPECIES', 'INDIVIDUAL_FOODIMAL_CREATURES',
            'ISLAND_REGIONS', 'LIVECORP_COLONY', 'POPULATORY_SPECIES', 'INVENTIONS',
            'LIVECORP_CELLS', 'WEAKNESS', 'SUSPIOUS_ACTIVITIES', 'COMBAT_EVENT',
            'CREATES', 'DESCRIPTIONS', 'INVENTOR', 'ANIMAL', 'FOOD_ITEM'
        ]
        
        self.table_columns = {
            'INTRUDERS': ['User_Id', 'Name', 'Gender', 'Height', 'Weight', 'Intelligence', 'Time_Of_Entry', 'Location_Id'],
            'MODERATORS': ['Moderator_Id', 'Name'],
            'FOODIMALS_SPECIES': ['Species_Id', 'Species_Name'],
            'INDIVIDUAL_FOODIMAL_CREATURES': ['Creature_Id', 'Species_Id', 'Location_Id', 'Populatory_Species_Id'],
            'ISLAND_REGIONS': ['Region_Id', 'Region_Name', 'Threat_To_Intruders'],
            'LIVECORP_COLONY': ['Colony_Id', 'Region_Id'],
            'POPULATORY_SPECIES': ['Species_Id', 'Spawn_Per_Birth'],
            'INVENTIONS': ['Item_Owner', 'Item_Name'],
            'LIVECORP_CELLS': ['Cell_Id', 'Colony_Id', 'Type'],
            'WEAKNESS': ['Species_Id', 'Item_Inventor_Id', 'Item_Name'],
            'SUSPIOUS_ACTIVITIES': ['Intruder_Id', 'Creature_Id', 'Colony_Id', 'Cell_Id'],
            'COMBAT_EVENT': ['Intruder_Id', 'Creature_Id', 'Item_Owner_Id', 'Region_Id', 'Item_Name'],
            'CREATES': ['Moderator_Id', 'Species_Id', 'Creature_Id'],
            'DESCRIPTIONS': ['Description', 'Item_Owner_Id', 'Item_Name'],
            'INVENTOR': ['Name', 'Item_Owner_Id', 'Item_Name'],
            'ANIMAL': ['Name', 'Species_Id'],
            'FOOD_ITEM': ['Name', 'Species_Id']
        }
        
        self.auto_increment_columns = {
            'INTRUDERS': ['User_Id'],
            'MODERATORS': ['Moderator_Id'],
            'FOODIMALS_SPECIES': ['Species_Id'],
            'INDIVIDUAL_FOODIMAL_CREATURES': ['Creature_Id'],
            'ISLAND_REGIONS': ['Region_Id'],
            'LIVECORP_COLONY': ['Colony_Id'],
            'LIVECORP_CELLS': ['Cell_Id']
        }
        
        # Foreign key relationships: column_name -> (referenced_table, id_column, display_column)
        self.foreign_keys = {
            'Location_Id': ('ISLAND_REGIONS', 'Region_Id', 'Region_Name'),
            'Region_Id': ('ISLAND_REGIONS', 'Region_Id', 'Region_Name'),
            'Species_Id': ('FOODIMALS_SPECIES', 'Species_Id', 'Species_Name'),
            'Populatory_Species_Id': ('POPULATORY_SPECIES', 'Species_Id', 'Spawn_Per_Birth'),
            'Colony_Id': ('LIVECORP_COLONY', 'Colony_Id', 'Region_Id'),
            'Cell_Id': ('LIVECORP_CELLS', 'Cell_Id', 'Type'),
            'Creature_Id': ('INDIVIDUAL_FOODIMAL_CREATURES', 'Creature_Id', 'Species_Id'),
            'Intruder_Id': ('INTRUDERS', 'User_Id', 'Name'),
            'Moderator_Id': ('MODERATORS', 'Moderator_Id', 'Name'),
            'Item_Owner_Id': ('INVENTIONS', 'Item_Owner', 'Item_Name'),
            'Item_Inventor_Id': ('INVENTIONS', 'Item_Owner', 'Item_Name'),
            'Item_Owner': ('INVENTIONS', 'Item_Owner', 'Item_Name')
        }

    def connect_to_database(self):
        """Prompt user for database connection details and establish connection"""
        print("\n" + "="*60)
        print("DATABASE CONNECTION")
        print("="*60)
        
        try:
            host = input("Enter host (default: localhost): ").strip() or "localhost"
            user = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            database = input("Enter database name (default: mini_world_db): ").strip() or "mini_world_db"
            
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            
            self.cursor = self.connection.cursor(dictionary=True)
            print("\n✓ Successfully connected to the database!")
            return True
            
        except Error as e:
            print(f"\n✗ Error connecting to database: {e}")
            return False

    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print("MINI WORLD DATABASE CLI")
        print("="*60)
        print("1. Insert data")
        print("2. Update data")
        print("3. Delete data")
        print("4. View tables")
        print("5. Retrieval Operations")
        print("6. Analysis Reports")
        print("7. Exit")
        print("="*60)

    def display_analysis_reports_menu(self):
        """Display analysis reports submenu"""
        print("\n" + "="*60)
        print("ANALYSIS REPORTS")
        print("="*60)
        print("1. Intruder Threat Assessment by Region")
        print("2. Foodimal Defensive Readiness Report")
        print("3. Combat Effectiveness Analysis")
        print("4. Back to Main Menu")
        print("="*60)

    def display_retrieval_operations_menu(self):
        """Display retrieval operations submenu"""
        print("\n" + "="*60)
        print("RETRIEVAL OPERATIONS")
        print("="*60)
        print("1. Find Species by Food Item")
        print("2. Search Invention Descriptions")
        print("3. Count Foodimals of a Specific Species")
        print("4. Calculate Average Intruder Intelligence")
        print("5. Find the Most Dangerous Region")
        print("6. Display Intruder Threat Profiles")
        print("7. List Foodimal Species and Recipes")
        print("8. Identify High-Threat Intruders")
        print("9. Find Foodimals in a Specific Region")
        print("10. List Inventions Effective Against a Species")
        print("11. Back to Main Menu")
        print("="*60)

    def display_tables(self):
        """Display available tables"""
        print("\n" + "="*60)
        print("AVAILABLE TABLES")
        print("="*60)
        for idx, table in enumerate(self.tables, 1):
            print(f"{idx}. {table}")
        print("="*60)

    def select_table(self) -> Optional[str]:
        """Let user select a table"""
        self.display_tables()
        try:
            choice = int(input("\nEnter table number: "))
            if 1 <= choice <= len(self.tables):
                return self.tables[choice - 1]
            else:
                print("✗ Invalid table number!")
                return None
        except ValueError:
            print("✗ Please enter a valid number!")
            return None

    def get_table_data(self, table: str) -> List[Dict]:
        """Fetch all data from a table"""
        try:
            self.cursor.execute(f"SELECT * FROM {table}")
            return self.cursor.fetchall()
        except Error as e:
            print(f"✗ Error fetching data: {e}")
            return []
    
    def show_reference_data(self, column_name: str):
        """Display reference data for foreign key columns"""
        if column_name not in self.foreign_keys:
            return
        
        ref_table, id_col, display_col = self.foreign_keys[column_name]
        
        try:
            self.cursor.execute(f"SELECT {id_col}, {display_col} FROM {ref_table}")
            ref_data = self.cursor.fetchall()
            
            if ref_data:
                print(f"\n  Available {column_name} values from {ref_table}:")
                print(f"  {'-' * 50}")
                for row in ref_data:
                    print(f"  {id_col}: {row[id_col]} -> {display_col}: {row[display_col]}")
                print(f"  {'-' * 50}")
        except Error as e:
            print(f"  (Could not fetch reference data: {e})")

    def display_table_data(self, table: str):
        """Display table data in a formatted manner"""
        data = self.get_table_data(table)
        
        if not data:
            print(f"\n✗ No data found in {table}")
            return
        
        print(f"\n{'='*60}")
        print(f"DATA IN {table}")
        print("="*60)
        
        # Get column names
        columns = list(data[0].keys())
        
        # Calculate column widths
        col_widths = {}
        for col in columns:
            max_width = len(str(col))
            for row in data:
                max_width = max(max_width, len(str(row[col])) if row[col] is not None else 4)
            col_widths[col] = min(max_width + 2, 30)  # Cap at 30 characters
        
        # Print header
        header = '|'.join([str(col).center(col_widths[col]) for col in columns])
        separator = '+'.join(['-' * col_widths[col] for col in columns])
        
        print(f"\n{separator}")
        print(header)
        print(separator)
        
        # Print rows
        for row in data:
            row_str = '|'.join([str(row[col] if row[col] is not None else 'NULL').ljust(col_widths[col]) for col in columns])
            print(row_str)
        
        print(separator)
        print(f"\nTotal rows: {len(data)}")
        print("="*60)

    def insert_data(self):
        """Insert data into a table"""
        table = self.select_table()
        if not table:
            return
        
        print(f"\n{'='*60}")
        print(f"INSERT DATA INTO {table}")
        print("="*60)
        
        columns = self.table_columns[table]
        auto_cols = self.auto_increment_columns.get(table, [])
        
        values = []
        insert_columns = []
        
        for col in columns:
            if col in auto_cols:
                response = input(f"{col} (AUTO_INCREMENT - press Enter to skip): ").strip()
                if response:
                    insert_columns.append(col)
                    values.append(response if response.lower() != 'null' else None)
            else:
                # Show reference data for foreign keys
                self.show_reference_data(col)
                
                while True:
                    value = input(f"Enter {col}: ").strip()
                    if value.lower() == 'null':
                        values.append(None)
                        insert_columns.append(col)
                        break
                    elif value:
                        values.append(value)
                        insert_columns.append(col)
                        break
                    else:
                        print("✗ Value cannot be empty (use 'null' for NULL values)")
        
        try:
            placeholders = ', '.join(['%s'] * len(values))
            column_names = ', '.join(insert_columns)
            query = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"
            
            self.cursor.execute(query, values)
            self.connection.commit()
            print(f"\n✓ Data inserted successfully into {table}!")
            
        except Error as e:
            self.connection.rollback()
            print(f"\n✗ Error inserting data: {e}")

    def update_data(self):
        """Update data in a table"""
        table = self.select_table()
        if not table:
            return
        
        self.display_table_data(table)
        
        print(f"\n{'='*60}")
        print(f"UPDATE DATA IN {table}")
        print("="*60)
        
        columns = self.table_columns[table]
        
        print("\nSpecify WHERE condition:")
        where_conditions = []
        where_values = []
        
        while True:
            print("\nAvailable columns:")
            for idx, col in enumerate(columns, 1):
                print(f"{idx}. {col}")
            
            try:
                col_choice = int(input("\nSelect column for WHERE condition (0 to finish): "))
                if col_choice == 0:
                    break
                if 1 <= col_choice <= len(columns):
                    col_name = columns[col_choice - 1]
                    # Show reference data for foreign keys (WHERE condition)
                    self.show_reference_data(col_name)
                    col_value = input(f"Enter value for {col_name}: ").strip()
                    where_conditions.append(f"{col_name} = %s")
                    where_values.append(col_value if col_value.lower() != 'null' else None)
                else:
                    print("✗ Invalid column number!")
            except ValueError:
                print("✗ Please enter a valid number!")
        
        if not where_conditions:
            print("✗ At least one WHERE condition is required!")
            return
        
        print("\nSpecify columns to UPDATE:")
        update_columns = []
        update_values = []
        
        while True:
            print("\nAvailable columns:")
            for idx, col in enumerate(columns, 1):
                print(f"{idx}. {col}")
            
            try:
                col_choice = int(input("\nSelect column to update (0 to finish): "))
                if col_choice == 0:
                    break
                if 1 <= col_choice <= len(columns):
                    col_name = columns[col_choice - 1]
                    # Show reference data for foreign keys (UPDATE)
                    self.show_reference_data(col_name)
                    new_value = input(f"Enter new value for {col_name}: ").strip()
                    update_columns.append(f"{col_name} = %s")
                    update_values.append(new_value if new_value.lower() != 'null' else None)
                else:
                    print("✗ Invalid column number!")
            except ValueError:
                print("✗ Please enter a valid number!")
        
        if not update_columns:
            print("✗ At least one column to update is required!")
            return
        
        try:
            set_clause = ', '.join(update_columns)
            where_clause = ' AND '.join(where_conditions)
            query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
            
            all_values = update_values + where_values
            self.cursor.execute(query, all_values)
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                print(f"\n✓ {self.cursor.rowcount} row(s) updated successfully in {table}!")
            else:
                print(f"\n✗ No rows matched the WHERE condition.")
                
        except Error as e:
            self.connection.rollback()
            print(f"\n✗ Error updating data: {e}")

    def delete_data(self):
        """Delete data from a table"""
        table = self.select_table()
        if not table:
            return
        
        self.display_table_data(table)
        
        print(f"\n{'='*60}")
        print(f"DELETE DATA FROM {table}")
        print("="*60)
        
        columns = self.table_columns[table]
        
        print("\nSpecify WHERE condition:")
        where_conditions = []
        where_values = []
        
        while True:
            print("\nAvailable columns:")
            for idx, col in enumerate(columns, 1):
                print(f"{idx}. {col}")
            
            try:
                col_choice = int(input("\nSelect column for WHERE condition (0 to finish): "))
                if col_choice == 0:
                    break
                if 1 <= col_choice <= len(columns):
                    col_name = columns[col_choice - 1]
                    # Show reference data for foreign keys (DELETE WHERE)
                    self.show_reference_data(col_name)
                    col_value = input(f"Enter value for {col_name}: ").strip()
                    where_conditions.append(f"{col_name} = %s")
                    where_values.append(col_value if col_value.lower() != 'null' else None)
                else:
                    print("✗ Invalid column number!")
            except ValueError:
                print("✗ Please enter a valid number!")
        
        if not where_conditions:
            print("✗ At least one WHERE condition is required for DELETE!")
            return
        
        where_clause = ' AND '.join(where_conditions)
        confirm = input(f"\n⚠ Are you sure you want to delete from {table} WHERE {where_clause}? (yes/no): ").strip().lower()
        
        if confirm != 'yes':
            print("✗ Delete operation cancelled.")
            return
        
        try:
            query = f"DELETE FROM {table} WHERE {where_clause}"
            self.cursor.execute(query, where_values)
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                print(f"\n✓ {self.cursor.rowcount} row(s) deleted successfully from {table}!")
            else:
                print(f"\n✗ No rows matched the WHERE condition.")
                
        except Error as e:
            self.connection.rollback()
            print(f"\n✗ Error deleting data: {e}")

    def intruder_threat_assessment(self):
        """Display Intruder Threat Assessment by Region Report"""
        print("\n" + "="*80)
        print("INTRUDER THREAT ASSESSMENT BY REGION")
        print("="*80)
        
        try:
            # Query to get intruders with their region information
            query = "SELECT i.User_Id, i.Name, i.Gender, i.Height, i.Weight, i.Intelligence, i.Time_Of_Entry, r.Region_Name, r.Region_Id, (i.Intelligence * i.Intelligence + i.Height - i.Weight / i.Height) AS Threat_Level FROM INTRUDERS i JOIN ISLAND_REGIONS r ON i.Location_Id = r.Region_Id ORDER BY Threat_Level DESC"
            
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            if not results:
                print("\n✗ No intruder data found.")
                print("="*80)
                return
            
            # Display results in formatted table
            print("\n" + "-"*80)
            print(f"{'User ID':<10}{'Name':<20}{'Region':<20}{'Threat Level':<15}")
            print("-"*80)
            
            for row in results:
                user_id = row['User_Id']
                name = row['Name'][:19]  # Truncate if too long
                region = row['Region_Name'][:19]
                threat_level = row['Threat_Level']
                
                print(f"{user_id:<10}{name:<20}{region:<20}{threat_level:<15.2f}")
            
            print("-"*80)
            print(f"\nTotal Intruders: {len(results)}")
            
            # Display detailed breakdown
            print("\n" + "="*80)
            print("DETAILED BREAKDOWN")
            print("="*80)
            
            for row in results:
                print(f"\nIntruder ID: {row['User_Id']} | Name: {row['Name']}")
                print(f"  Region: {row['Region_Name']} (ID: {row['Region_Id']})")
                print(f"  Physical Stats: Height={row['Height']}cm, Weight={row['Weight']}kg")
                print(f"  Intelligence: {row['Intelligence']}")
                print(f"  Time of Entry: {row['Time_Of_Entry']}")
                print(f"  THREAT LEVEL: {row['Threat_Level']:.2f}")
                print(f"    Formula: ({row['Intelligence']}^2) + {row['Height']} - ({row['Weight']}/{row['Height']})")
                print("  " + "-"*76)
            
            print("\n" + "="*80)
            
        except Error as e:
            print(f"\n✗ Error generating report: {e}")
            print("="*80)

    def foodimal_defensive_readiness(self):
        """Display Foodimal Defensive Readiness Report by Region"""
        print("\n" + "="*80)
        print("FOODIMAL DEFENSIVE READINESS REPORT")
        print("="*80)
        
        try:
            # Query to get foodimal species distribution across regions
            query = "SELECT r.Region_Name, r.Region_Id, fs.Species_Name, fs.Species_Id, COUNT(ifc.Creature_Id) AS Number_of_Units FROM INDIVIDUAL_FOODIMAL_CREATURES ifc JOIN FOODIMALS_SPECIES fs ON ifc.Species_Id = fs.Species_Id JOIN ISLAND_REGIONS r ON ifc.Location_Id = r.Region_Id GROUP BY r.Region_Name, r.Region_Id, fs.Species_Name, fs.Species_Id ORDER BY r.Region_Name, Number_of_Units DESC"
            
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            if not results:
                print("\n✗ No foodimal creature data found.")
                print("="*80)
                return
            
            # Group results by region for better display
            regions_data = {}
            for row in results:
                region_name = row['Region_Name']
                if region_name not in regions_data:
                    regions_data[region_name] = {
                        'region_id': row['Region_Id'],
                        'species': [],
                        'total_units': 0
                    }
                regions_data[region_name]['species'].append({
                    'species_name': row['Species_Name'],
                    'species_id': row['Species_Id'],
                    'count': row['Number_of_Units']
                })
                regions_data[region_name]['total_units'] += row['Number_of_Units']
            
            # Display summary table
            print("\n" + "-"*80)
            print(f"{'Region':<25}{'Species Count':<20}{'Total Units':<15}")
            print("-"*80)
            
            for region_name in sorted(regions_data.keys()):
                region_info = regions_data[region_name]
                species_count = len(region_info['species'])
                total_units = region_info['total_units']
                print(f"{region_name:<25}{species_count:<20}{total_units:<15}")
            
            print("-"*80)
            print(f"\nTotal Regions: {len(regions_data)}")
            print(f"Total Foodimal Units: {sum(r['total_units'] for r in regions_data.values())}")
            
            # Display detailed breakdown by region
            print("\n" + "="*80)
            print("DETAILED BREAKDOWN BY REGION")
            print("="*80)
            
            for region_name in sorted(regions_data.keys()):
                region_info = regions_data[region_name]
                print(f"\n{'='*80}")
                print(f"REGION: {region_name} (ID: {region_info['region_id']})")
                print(f"{'='*80}")
                print(f"{'Species Name':<30}{'Species ID':<15}{'Unit Count':<15}")
                print("-"*80)
                
                for species in region_info['species']:
                    print(f"{species['species_name']:<30}{species['species_id']:<15}{species['count']:<15}")
                
                print("-"*80)
                print(f"Region Total: {region_info['total_units']} units across {len(region_info['species'])} species")
            
            print("\n" + "="*80)
            
        except Error as e:
            print(f"\n✗ Error generating report: {e}")
            print("="*80)

    def combat_effectiveness_analysis(self):
        """Display Combat Effectiveness Analysis Report"""
        print("\n" + "="*80)
        print("COMBAT EFFECTIVENESS ANALYSIS")
        print("="*80)
        
        try:
            # Query to analyze combat events and invention usage
            query = "SELECT i.Name AS Intruder_Name, i.User_Id, inv.Item_Name AS Invention_Used, inv.Item_Owner, COUNT(*) AS Frequency_of_Use FROM COMBAT_EVENT ce JOIN INTRUDERS i ON ce.Intruder_Id = i.User_Id JOIN INVENTIONS inv ON ce.Item_Owner_Id = inv.Item_Owner AND ce.Item_Name = inv.Item_Name GROUP BY i.Name, i.User_Id, inv.Item_Name, inv.Item_Owner ORDER BY Frequency_of_Use DESC"
            
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            if not results:
                print("\n✗ No combat event data found.")
                print("="*80)
                return
            
            # Display summary table
            print("\n" + "-"*80)
            print(f"{'Intruder Name':<25}{'Invention Used':<30}{'Frequency':<15}")
            print("-"*80)
            
            for row in results:
                intruder_name = row['Intruder_Name'][:24]
                invention = row['Invention_Used'][:29]
                frequency = row['Frequency_of_Use']
                print(f"{intruder_name:<25}{invention:<30}{frequency:<15}")
            
            print("-"*80)
            print(f"\nTotal Combat Events Analyzed: {sum(r['Frequency_of_Use'] for r in results)}")
            print(f"Unique Intruder-Invention Combinations: {len(results)}")
            
            # Group by intruder for detailed analysis
            intruders_data = {}
            for row in results:
                intruder_name = row['Intruder_Name']
                if intruder_name not in intruders_data:
                    intruders_data[intruder_name] = {
                        'user_id': row['User_Id'],
                        'inventions': [],
                        'total_events': 0
                    }
                intruders_data[intruder_name]['inventions'].append({
                    'item_name': row['Invention_Used'],
                    'item_owner': row['Item_Owner'],
                    'frequency': row['Frequency_of_Use']
                })
                intruders_data[intruder_name]['total_events'] += row['Frequency_of_Use']
            
            # Display detailed breakdown by intruder
            print("\n" + "="*80)
            print("DETAILED BREAKDOWN BY INTRUDER")
            print("="*80)
            
            for intruder_name in sorted(intruders_data.keys(), key=lambda x: intruders_data[x]['total_events'], reverse=True):
                intruder_info = intruders_data[intruder_name]
                print(f"\n{'='*80}")
                print(f"INTRUDER: {intruder_name} (ID: {intruder_info['user_id']})")
                print(f"{'='*80}")
                print(f"{'Invention Name':<35}{'Owner ID':<15}{'Usage Count':<15}{'% of Total':<15}")
                print("-"*80)
                
                for inv in intruder_info['inventions']:
                    percentage = (inv['frequency'] / intruder_info['total_events']) * 100
                    print(f"{inv['item_name']:<35}{inv['item_owner']:<15}{inv['frequency']:<15}{percentage:.1f}%")
                
                print("-"*80)
                print(f"Total Combat Events: {intruder_info['total_events']}")
                print(f"Unique Inventions Used: {len(intruder_info['inventions'])}")
                
                # Find most used invention for this intruder
                most_used = max(intruder_info['inventions'], key=lambda x: x['frequency'])
                print(f"Most Frequently Used: {most_used['item_name']} ({most_used['frequency']} times)")
            
            # Display top 5 most used inventions overall
            print("\n" + "="*80)
            print("TOP 5 MOST USED INVENTIONS (ACROSS ALL INTRUDERS)")
            print("="*80)
            
            invention_totals = {}
            for row in results:
                inv_key = (row['Invention_Used'], row['Item_Owner'])
                if inv_key not in invention_totals:
                    invention_totals[inv_key] = 0
                invention_totals[inv_key] += row['Frequency_of_Use']
            
            top_inventions = sorted(invention_totals.items(), key=lambda x: x[1], reverse=True)[:5]
            
            print(f"\n{'Rank':<8}{'Invention Name':<35}{'Owner ID':<15}{'Total Uses':<15}")
            print("-"*80)
            for idx, ((inv_name, owner_id), total) in enumerate(top_inventions, 1):
                print(f"{idx:<8}{inv_name:<35}{owner_id:<15}{total:<15}")
            
            print("\n" + "="*80)
            
        except Error as e:
            print(f"\n✗ Error generating report: {e}")
            print("="*80)

    def find_species_by_food_item(self):
        """Search for Foodimal Species by Food Item name"""
        print("\n" + "="*80)
        print("FIND SPECIES BY FOOD ITEM")
        print("="*80)
        
        food_item_keyword = input("\nEnter food item keyword to search (e.g., 'taco', 'pizza'): ").strip()
        
        if not food_item_keyword:
            print("✗ Search keyword cannot be empty.")
            return
        
        try:
            # Query to find species that have food items containing the keyword
            query = "SELECT DISTINCT fs.Species_Id, fs.Species_Name, fi.Name AS Food_Item_Name FROM FOODIMALS_SPECIES fs JOIN FOOD_ITEM fi ON fs.Species_Id = fi.Species_Id WHERE fi.Name LIKE %s ORDER BY fs.Species_Name"
            search_pattern = f"%{food_item_keyword}%"
            
            self.cursor.execute(query, (search_pattern,))
            results = self.cursor.fetchall()
            
            if not results:
                print(f"\n✗ No species found with food item containing '{food_item_keyword}'.")
                print("="*80)
                return
            
            # Display results
            print(f"\nSearch Results for '{food_item_keyword}':")
            print("-"*80)
            print(f"{'Species ID':<15}{'Species Name':<30}{'Food Item Name':<30}")
            print("-"*80)
            
            for row in results:
                species_id = row['Species_Id']
                species_name = row['Species_Name'][:29]
                food_item_name = row['Food_Item_Name'][:29]
                print(f"{species_id:<15}{species_name:<30}{food_item_name:<30}")
            
            print("-"*80)
            print(f"\nTotal species found: {len(results)}")
            print("="*80)
            
        except Error as e:
            print(f"\n✗ Error searching for species: {e}")
            print("="*80)

    def search_invention_descriptions(self):
        """Search for Inventions by description keyword"""
        print("\n" + "="*80)
        print("SEARCH INVENTION DESCRIPTIONS")
        print("="*80)
        
        description_keyword = input("\nEnter description keyword to search (e.g., 'party', 'celebration'): ").strip()
        
        if not description_keyword:
            print("✗ Search keyword cannot be empty.")
            return
        
        try:
            # Query to find inventions with descriptions containing the keyword (case-insensitive)
            query = "SELECT inv.Item_Owner, inv.Item_Name, d.Description, i.Name AS Owner_Name FROM INVENTIONS inv JOIN DESCRIPTIONS d ON inv.Item_Owner = d.Item_Owner_Id AND inv.Item_Name = d.Item_Name JOIN INTRUDERS i ON inv.Item_Owner = i.User_Id WHERE LOWER(d.Description) LIKE LOWER(%s) ORDER BY inv.Item_Name"
            search_pattern = f"%{description_keyword}%"
            
            self.cursor.execute(query, (search_pattern,))
            results = self.cursor.fetchall()
            
            if not results:
                print(f"\n✗ No inventions found with description containing '{description_keyword}'.")
                print("="*80)
                return
            
            # Display results
            print(f"\nSearch Results for '{description_keyword}':")
            print("-"*80)
            print(f"{'Item Name':<30}{'Owner':<20}{'Owner ID':<12}")
            print("-"*80)
            
            displayed_items = set()
            for row in results:
                item_key = (row['Item_Owner'], row['Item_Name'])
                if item_key not in displayed_items:
                    item_name = row['Item_Name'][:29]
                    owner_name = row['Owner_Name'][:19]
                    owner_id = row['Item_Owner']
                    print(f"{item_name:<30}{owner_name:<20}{owner_id:<12}")
                    displayed_items.add(item_key)
            
            print("-"*80)
            print(f"\nTotal unique inventions found: {len(displayed_items)}")
            
            # Display detailed descriptions
            print("\n" + "="*80)
            print("DETAILED DESCRIPTIONS")
            print("="*80)
            
            for row in results:
                print(f"\nInvention: {row['Item_Name']}")
                print(f"  Owner: {row['Owner_Name']} (ID: {row['Item_Owner']})")
                print(f"  Description: {row['Description']}")
                print("  " + "-"*76)
            
            print("\n" + "="*80)
            
        except Error as e:
            print(f"\n✗ Error searching for inventions: {e}")
            print("="*80)

    def count_foodimals_by_species(self):
        """Count the total number of foodimals of a specific species"""
        print("\n" + "="*80)
        print("COUNT FOODIMALS OF A SPECIFIC SPECIES")
        print("="*80)
        
        species_name = input("\nEnter species name to count (e.g., 'Tacodile'): ").strip()
        
        if not species_name:
            print("✗ Species name cannot be empty.")
            return
        
        try:
            # Query to count foodimals of the specified species
            query = "SELECT fs.Species_Id, fs.Species_Name, COUNT(ifc.Creature_Id) AS Total_Count FROM FOODIMALS_SPECIES fs LEFT JOIN INDIVIDUAL_FOODIMAL_CREATURES ifc ON fs.Species_Id = ifc.Species_Id WHERE fs.Species_Name = %s GROUP BY fs.Species_Id, fs.Species_Name"
            
            self.cursor.execute(query, (species_name,))
            result = self.cursor.fetchone()
            
            if not result:
                print(f"\n✗ No species found with the name '{species_name}'.")
                print("="*80)
                return
            
            # Display result
            print(f"\nSpecies: {result['Species_Name']}")
            print(f"Species ID: {result['Species_Id']}")
            print("-"*80)
            print(f"Total Living Instances: {result['Total_Count']}")
            print("="*80)
            
        except Error as e:
            print(f"\n✗ Error counting foodimals: {e}")
            print("="*80)

    def calculate_average_intruder_intelligence(self):
        """Calculate average intelligence of intruders in a specific colony"""
        print("\n" + "="*80)
        print("CALCULATE AVERAGE INTRUDER INTELLIGENCE")
        print("="*80)
        
        try:
            # First, show available colonies
            query_colonies = "SELECT c.Colony_Id, r.Region_Name FROM LIVECORP_COLONY c JOIN ISLAND_REGIONS r ON c.Region_Id = r.Region_Id ORDER BY c.Colony_Id"
            self.cursor.execute(query_colonies)
            colonies = self.cursor.fetchall()
            
            if not colonies:
                print("\n✗ No colonies found in the database.")
                print("="*80)
                return
            
            print("\nAvailable Colonies:")
            print("-"*80)
            for colony in colonies:
                print(f"Colony ID: {colony['Colony_Id']} - Region: {colony['Region_Name']}")
            print("-"*80)
            
        except Error as e:
            print(f"\n✗ Error fetching colonies: {e}")
            print("="*80)
            return
        
        colony_id = input("\nEnter Colony ID: ").strip()
        
        if not colony_id:
            print("✗ Colony ID cannot be empty.")
            return
        
        try:
            # Query to calculate average intelligence of intruders associated with the colony
            query = "SELECT c.Colony_Id, r.Region_Name, AVG(i.Intelligence) AS Average_Intelligence, COUNT(DISTINCT i.User_Id) AS Total_Intruders FROM LIVECORP_COLONY c JOIN ISLAND_REGIONS r ON c.Region_Id = r.Region_Id LEFT JOIN SUSPIOUS_ACTIVITIES sa ON c.Colony_Id = sa.Colony_Id LEFT JOIN INTRUDERS i ON sa.Intruder_Id = i.User_Id WHERE c.Colony_Id = %s GROUP BY c.Colony_Id, r.Region_Name"
            
            self.cursor.execute(query, (colony_id,))
            result = self.cursor.fetchone()
            
            if not result:
                print(f"\n✗ No colony found with ID '{colony_id}'.")
                print("="*80)
                return
            
            # Display result
            print(f"\nColony ID: {result['Colony_Id']}")
            print(f"Region: {result['Region_Name']}")
            print("-"*80)
            print(f"Total Intruders Associated: {result['Total_Intruders']}")
            
            if result['Average_Intelligence'] is not None:
                print(f"Average Intelligence: {result['Average_Intelligence']:.2f}")
            else:
                print("Average Intelligence: N/A (No intruders associated with this colony)")
            
            print("="*80)
            
        except Error as e:
            print(f"\n✗ Error calculating average intelligence: {e}")
            print("="*80)

    def display_intruder_threat_profiles(self):
        """Display Name, Intelligence, and Threat Status of all intruders"""
        print("\n" + "="*80)
        print("INTRUDER THREAT PROFILES")
        print("="*80)
        
        try:
            # Query to get Name, Intelligence, and Threat Status (calculated)
            query = "SELECT Name, Intelligence, (Intelligence * Intelligence + Height - Weight / Height) AS Threat_Status FROM INTRUDERS ORDER BY Threat_Status DESC"
            
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            if not results:
                print("\n✗ No intruder data found.")
                print("="*80)
                return
            
            # Display results in formatted table
            print("\n" + "-"*80)
            print(f"{'Name':<30}{'Intelligence':<20}{'Threat Status':<20}")
            print("-"*80)
            
            for row in results:
                name = row['Name'][:29]
                intelligence = row['Intelligence']
                threat_status = f"{row['Threat_Status']:.2f}"
                print(f"{name:<30}{intelligence:<20}{threat_status:<20}")
            
            print("-"*80)
            print(f"\nTotal Intruders: {len(results)}")
            print("\nThreat Status Formula: Intelligence² + Height - Weight/Height")
            print("="*80)
            
        except Error as e:
            print(f"\n✗ Error generating report: {e}")
            print("="*80)

    def list_foodimal_species_recipes(self):
        """List all Foodimal species and their recipes (Animal + Food Item combination)"""
        print("\n" + "="*80)
        print("FOODIMAL SPECIES AND RECIPES")
        print("="*80)
        
        try:
            # Query to get species with their animal and food item components
            query = "SELECT fs.Species_Name, a.Name AS Animal_Component, fi.Name AS Food_Component FROM FOODIMALS_SPECIES fs LEFT JOIN ANIMAL a ON fs.Species_Id = a.Species_Id LEFT JOIN FOOD_ITEM fi ON fs.Species_Id = fi.Species_Id ORDER BY fs.Species_Name"
            
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            if not results:
                print("\n✗ No species data found.")
                print("="*80)
                return
            
            # Group results by species to combine multiple animals/food items
            species_recipes = {}
            for row in results:
                species = row['Species_Name']
                if species not in species_recipes:
                    species_recipes[species] = {'animals': set(), 'foods': set()}
                
                if row['Animal_Component']:
                    species_recipes[species]['animals'].add(row['Animal_Component'])
                if row['Food_Component']:
                    species_recipes[species]['foods'].add(row['Food_Component'])
            
            # Display results
            print("\n" + "-"*80)
            print(f"{'Species Name':<30}{'Recipe (Animal + Food)':<50}")
            print("-"*80)
            
            for species in sorted(species_recipes.keys()):
                animals = ', '.join(sorted(species_recipes[species]['animals'])) if species_recipes[species]['animals'] else 'N/A'
                foods = ', '.join(sorted(species_recipes[species]['foods'])) if species_recipes[species]['foods'] else 'N/A'
                recipe = f"{animals} + {foods}"
                
                # Handle long recipes with wrapping
                if len(recipe) > 48:
                    recipe = recipe[:45] + "..."
                
                print(f"{species:<30}{recipe:<50}")
            
            print("-"*80)
            print(f"\nTotal Species: {len(species_recipes)}")
            
            # Display detailed breakdown
            print("\n" + "="*80)
            print("DETAILED RECIPE BREAKDOWN")
            print("="*80)
            
            for species in sorted(species_recipes.keys()):
                print(f"\n{species}:")
                print(f"  Animal Components: {', '.join(sorted(species_recipes[species]['animals'])) if species_recipes[species]['animals'] else 'None'}")
                print(f"  Food Components: {', '.join(sorted(species_recipes[species]['foods'])) if species_recipes[species]['foods'] else 'None'}")
            
            print("\n" + "="*80)
            
        except Error as e:
            print(f"\n✗ Error generating report: {e}")
            print("="*80)

    def identify_high_threat_intruders(self):
        """Identify intruders with threat status above a critical threshold"""
        print("\n" + "="*80)
        print("IDENTIFY HIGH-THREAT INTRUDERS")
        print("="*80)
        
        threshold_input = input("\nEnter critical threat threshold (e.g., 10): ").strip()
        
        if not threshold_input:
            print("✗ Threshold cannot be empty.")
            return
        
        try:
            threshold = float(threshold_input)
        except ValueError:
            print("✗ Invalid threshold value. Please enter a number.")
            return
        
        try:
            # Query to get all intruders with threat status above threshold
            query = "SELECT User_Id, Name, Gender, Height, Weight, Intelligence, Time_Of_Entry, Location_Id, (Intelligence * Intelligence + Height - Weight / Height) AS Threat_Status FROM INTRUDERS HAVING Threat_Status > %s ORDER BY Threat_Status DESC"
            
            self.cursor.execute(query, (threshold,))
            results = self.cursor.fetchall()
            
            if not results:
                print(f"\n✗ No intruders found with threat status above {threshold}.")
                print("="*80)
                return
            
            # Display results in formatted table
            print(f"\nIntruders with Threat Status > {threshold}:")
            print("-"*80)
            print(f"{'User ID':<10}{'Name':<20}{'Gender':<10}{'Intelligence':<15}{'Threat Status':<15}")
            print("-"*80)
            
            for row in results:
                user_id = row['User_Id']
                name = row['Name'][:19]
                gender = row['Gender']
                intelligence = row['Intelligence']
                threat_status = f"{row['Threat_Status']:.2f}"
                print(f"{user_id:<10}{name:<20}{gender:<10}{intelligence:<15}{threat_status:<15}")
            
            print("-"*80)
            print(f"\nTotal High-Threat Intruders: {len(results)}")
            
            # Display detailed breakdown
            print("\n" + "="*80)
            print("DETAILED INTRUDER RECORDS")
            print("="*80)
            
            for row in results:
                print(f"\nUser ID: {row['User_Id']}")
                print(f"  Name: {row['Name']}")
                print(f"  Gender: {row['Gender']}")
                print(f"  Height: {row['Height']} cm")
                print(f"  Weight: {row['Weight']} kg")
                print(f"  Intelligence: {row['Intelligence']}")
                print(f"  Time of Entry: {row['Time_Of_Entry']}")
                print(f"  Location ID: {row['Location_Id']}")
                print(f"  Threat Status: {row['Threat_Status']:.2f}")
            
            print("\n" + "="*80)
            
        except Error as e:
            print(f"\n✗ Error retrieving high-threat intruders: {e}")
            print("="*80)

    def find_foodimals_in_region(self):
        """Find all individual foodimals in a specific region"""
        print("\n" + "="*80)
        print("FIND FOODIMALS IN A SPECIFIC REGION")
        print("="*80)
        
        try:
            # First, show available regions
            query_regions = "SELECT Region_Id, Region_Name FROM ISLAND_REGIONS ORDER BY Region_Name"
            self.cursor.execute(query_regions)
            regions = self.cursor.fetchall()
            
            if not regions:
                print("\n✗ No regions found in the database.")
                print("="*80)
                return
            
            print("\nAvailable Regions:")
            print("-"*80)
            for region in regions:
                print(f"  {region['Region_Id']}: {region['Region_Name']}")
            print("-"*80)
            
        except Error as e:
            print(f"\n✗ Error fetching regions: {e}")
            print("="*80)
            return
        
        region_name = input("\nEnter region name (e.g., 'The Rock Candy Mountains'): ").strip()
        
        if not region_name:
            print("✗ Region name cannot be empty.")
            return
        
        try:
            # Query to find all foodimals in the specified region
            query = "SELECT ifc.Creature_Id, ifc.Species_Id, fs.Species_Name, ifc.Location_Id, r.Region_Name, ifc.Populatory_Species_Id FROM INDIVIDUAL_FOODIMAL_CREATURES ifc JOIN FOODIMALS_SPECIES fs ON ifc.Species_Id = fs.Species_Id JOIN ISLAND_REGIONS r ON ifc.Location_Id = r.Region_Id WHERE r.Region_Name = %s ORDER BY fs.Species_Name, ifc.Creature_Id"
            
            self.cursor.execute(query, (region_name,))
            results = self.cursor.fetchall()
            
            if not results:
                print(f"\n✗ No foodimals found in region '{region_name}'.")
                print("="*80)
                return
            
            # Display results in formatted table
            print(f"\nFoodimals in '{region_name}':")
            print("-"*80)
            print(f"{'Creature ID':<15}{'Species Name':<30}{'Species ID':<15}{'Pop. Species ID':<20}")
            print("-"*80)
            
            for row in results:
                creature_id = row['Creature_Id']
                species_name = row['Species_Name'][:29]
                species_id = row['Species_Id']
                pop_species_id = row['Populatory_Species_Id'] if row['Populatory_Species_Id'] else 'N/A'
                print(f"{creature_id:<15}{species_name:<30}{species_id:<15}{str(pop_species_id):<20}")
            
            print("-"*80)
            print(f"\nTotal Foodimals in Region: {len(results)}")
            
            # Display species distribution
            species_count = {}
            for row in results:
                species = row['Species_Name']
                species_count[species] = species_count.get(species, 0) + 1
            
            print("\n" + "="*80)
            print("SPECIES DISTRIBUTION IN REGION")
            print("="*80)
            print(f"\n{'Species Name':<40}{'Count':<10}")
            print("-"*80)
            
            for species, count in sorted(species_count.items(), key=lambda x: x[1], reverse=True):
                print(f"{species:<40}{count:<10}")
            
            print("\n" + "="*80)
            
        except Error as e:
            print(f"\n✗ Error retrieving foodimals: {e}")
            print("="*80)

    def list_inventions_against_species(self):
        """List all inventions effective against a specific foodimal species"""
        print("\n" + "="*80)
        print("LIST INVENTIONS EFFECTIVE AGAINST A SPECIES")
        print("="*80)
        
        try:
            # First, show available species
            query_species = "SELECT Species_Id, Species_Name FROM FOODIMALS_SPECIES ORDER BY Species_Name"
            self.cursor.execute(query_species)
            species_list = self.cursor.fetchall()
            
            if not species_list:
                print("\n✗ No species found in the database.")
                print("="*80)
                return
            
            print("\nAvailable Foodimal Species:")
            print("-"*80)
            for species in species_list:
                print(f"  {species['Species_Id']}: {species['Species_Name']}")
            print("-"*80)
            
        except Error as e:
            print(f"\n✗ Error fetching species: {e}")
            print("="*80)
            return
        
        species_name = input("\nEnter species name (e.g., 'Cheespider'): ").strip()
        
        if not species_name:
            print("✗ Species name cannot be empty.")
            return
        
        try:
            # Query to find all inventions that are weaknesses for the species
            query = "SELECT fs.Species_Name, fs.Species_Id, inv.Item_Name, inv.Item_Owner, i.Name AS Owner_Name FROM WEAKNESS w JOIN FOODIMALS_SPECIES fs ON w.Species_Id = fs.Species_Id JOIN INVENTIONS inv ON w.Item_Inventor_Id = inv.Item_Owner AND w.Item_Name = inv.Item_Name JOIN INTRUDERS i ON inv.Item_Owner = i.User_Id WHERE fs.Species_Name = %s ORDER BY inv.Item_Name"
            
            self.cursor.execute(query, (species_name,))
            results = self.cursor.fetchall()
            
            if not results:
                print(f"\n✗ No inventions found that are effective against '{species_name}'.")
                print("="*80)
                return
            
            # Display results in formatted table
            print(f"\nInventions Effective Against '{species_name}':")
            print("-"*80)
            print(f"{'Item Name':<35}{'Owner Name':<25}{'Owner ID':<15}")
            print("-"*80)
            
            for row in results:
                item_name = row['Item_Name'][:34]
                owner_name = row['Owner_Name'][:24]
                owner_id = row['Item_Owner']
                print(f"{item_name:<35}{owner_name:<25}{owner_id:<15}")
            
            print("-"*80)
            print(f"\nTotal Effective Inventions: {len(results)}")
            
            # Display detailed breakdown
            print("\n" + "="*80)
            print("DETAILED INVENTORY")
            print("="*80)
            
            for row in results:
                print(f"\nInvention: {row['Item_Name']}")
                print(f"  Owner: {row['Owner_Name']} (ID: {row['Item_Owner']})")
                print(f"  Effective Against: {row['Species_Name']} (Species ID: {row['Species_Id']})")
            
            print("\n" + "="*80)
            
        except Error as e:
            print(f"\n✗ Error retrieving inventions: {e}")
            print("="*80)

    def find_most_dangerous_region(self):
        """Find the island region with the highest threat to intruders"""
        print("\n" + "="*80)
        print("FIND THE MOST DANGEROUS REGION")
        print("="*80)
        
        try:
            # Query to find the region with maximum threat value
            query = "SELECT Region_Id, Region_Name, Threat_To_Intruders FROM ISLAND_REGIONS WHERE Threat_To_Intruders = (SELECT MAX(Threat_To_Intruders) FROM ISLAND_REGIONS)"
            
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            if not results:
                print("\n✗ No regions found in the database.")
                print("="*80)
                return
            
            # Display results
            print("\nMost Dangerous Region(s):")
            print("-"*80)
            print(f"{'Region ID':<15}{'Region Name':<30}{'Threat Level':<15}")
            print("-"*80)
            
            for row in results:
                region_id = row['Region_Id']
                region_name = row['Region_Name'][:29]
                threat_level = row['Threat_To_Intruders']
                print(f"{region_id:<15}{region_name:<30}{threat_level:<15}")
            
            print("-"*80)
            
            if len(results) > 1:
                print(f"\nNote: {len(results)} regions share the highest threat level.")
            
            print("\nInterpretation: Higher threat values indicate greater danger to intruders.")
            print("="*80)
            
        except Error as e:
            print(f"\n✗ Error finding most dangerous region: {e}")
            print("="*80)

    def retrieval_operations(self):
        """Handle retrieval operations submenu"""
        while True:
            self.display_retrieval_operations_menu()
            
            try:
                choice = input("\nEnter your choice (1-11): ").strip()
                
                if choice == '1':
                    self.find_species_by_food_item()
                elif choice == '2':
                    self.search_invention_descriptions()
                elif choice == '3':
                    self.count_foodimals_by_species()
                elif choice == '4':
                    self.calculate_average_intruder_intelligence()
                elif choice == '5':
                    self.find_most_dangerous_region()
                elif choice == '6':
                    self.display_intruder_threat_profiles()
                elif choice == '7':
                    self.list_foodimal_species_recipes()
                elif choice == '8':
                    self.identify_high_threat_intruders()
                elif choice == '9':
                    self.find_foodimals_in_region()
                elif choice == '10':
                    self.list_inventions_against_species()
                elif choice == '11':
                    break
                else:
                    print("✗ Invalid choice! Please enter a number between 1 and 11.")
                    
            except ValueError:
                print("✗ Please enter a valid number!")

    def analysis_reports(self):
        """Handle analysis reports submenu"""
        while True:
            self.display_analysis_reports_menu()
            
            try:
                choice = input("\nEnter your choice (1-4): ").strip()
                
                if choice == '1':
                    self.intruder_threat_assessment()
                elif choice == '2':
                    self.foodimal_defensive_readiness()
                elif choice == '3':
                    self.combat_effectiveness_analysis()
                elif choice == '4':
                    break
                else:
                    print("✗ Invalid choice! Please enter a number between 1 and 4.")
                    
            except ValueError:
                print("✗ Please enter a valid number!")

    def run(self):
        """Main application loop"""
        print("\n" + "="*60)
        print("WELCOME TO MINI WORLD DATABASE CLI")
        print("="*60)
        
        if not self.connect_to_database():
            return
        
        while True:
            self.display_menu()
            
            try:
                choice = input("\nEnter your choice (1-7): ").strip()
                
                if choice == '1':
                    self.insert_data()
                elif choice == '2':
                    self.update_data()
                elif choice == '3':
                    self.delete_data()
                elif choice == '4':
                    table = self.select_table()
                    if table:
                        self.display_table_data(table)
                elif choice == '5':
                    self.retrieval_operations()
                elif choice == '6':
                    self.analysis_reports()
                elif choice == '7':
                    print("\n✓ Closing database connection...")
                    if self.cursor:
                        self.cursor.close()
                    if self.connection:
                        self.connection.close()
                    print("✓ Thank you for using Mini World Database CLI!")
                    break
                else:
                    print("✗ Invalid choice! Please enter a number between 1 and 7.")
                    
            except KeyboardInterrupt:
                print("\n\n✓ Interrupted by user. Closing connection...")
                if self.cursor:
                    self.cursor.close()
                if self.connection:
                    self.connection.close()
                break
            except Exception as e:
                print(f"\n✗ An unexpected error occurred: {e}")


def main():
    cli = DatabaseCLI()
    cli.run()


if __name__ == "__main__":
    main()
