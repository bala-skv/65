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
        print("5. Exit")
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
                choice = input("\nEnter your choice (1-5): ").strip()
                
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
                    print("\n✓ Closing database connection...")
                    if self.cursor:
                        self.cursor.close()
                    if self.connection:
                        self.connection.close()
                    print("✓ Thank you for using Mini World Database CLI!")
                    break
                else:
                    print("✗ Invalid choice! Please enter a number between 1 and 5.")
                    
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
