#!/usr/bin/env python3
"""
Script to export the SQLAlchemy database schema to a SQL file.
This script generates DDL (Data Definition Language) statements for all tables
defined in the database models.
"""

from database.descend_children import DescendChildren
from database.family_witness import FamilyWitness
from database.family_event_witness import FamilyEventWitness
from database.person_event_witness import PersonEventWitness
from database.person_titles import PersonTitles
from database.person_non_native_relations import PersonNonNativeRelations
from database.person_relations import PersonRelations
from database.family_events import FamilyEvents
from database.person_events import PersonEvents
from database.family_event import FamilyEvent
from database.personal_event import PersonalEvent
from database.titles import Titles
from database.relation import Relation
from database.place import Place
from database.date import Date, Precision
from database.union_families import UnionFamilies
from database.unions import Unions
from database.descends import Descends
from database.ascends import Ascends
from database.couple import Couple
from database.family import Family
from database.person import Person
from database import Base
import sys
import enum
from pathlib import Path
from sqlalchemy import create_engine, event, Enum as SQLEnum
from sqlalchemy.schema import CreateTable
from typing import Dict, Set

# Add the src directory to Python path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))


# Import all models to ensure they're registered with Base.metadata


def get_enum_values_from_table(table) -> Dict[str, Set[str]]:
    """
    Extract enum column names and their possible values from a table.

    Returns:
        Dictionary mapping column names to sets of enum values
    """
    enum_values = {}

    for column in table.columns:
        if isinstance(column.type, SQLEnum):
            # Get the enum class from the column type
            enum_class = column.type.enum_class
            if enum_class and issubclass(enum_class, enum.Enum):
                # Extract all enum values
                values = [e.value for e in enum_class]
                enum_values[column.name] = values

    return enum_values


def create_table_with_check_constraints(table, engine) -> str:
    """
    Generate CREATE TABLE statement with inline CHECK constraints for enums.

    Args:
        table: SQLAlchemy Table object
        engine: SQLAlchemy engine for dialect-specific compilation

    Returns:
        String containing the CREATE TABLE statement with CHECK constraints
    """
    from sqlalchemy.schema import CreateTable
    from sqlalchemy import CheckConstraint

    # Get enum values for this table
    enum_values = get_enum_values_from_table(table)

    # If there are enum columns, add CHECK constraints to the table
    if enum_values:
        for column_name, values in enum_values.items():
            # Create CHECK constraint for this enum column
            values_str = "', '".join(values)
            constraint_name = f"chk_{table.name}_{column_name}"
            check_expr = f"{column_name} IN ('{values_str}')"

            # Add the constraint to the table (if not already present)
            constraint_exists = any(
                isinstance(c, CheckConstraint) and constraint_name in str(c)
                for c in table.constraints
            )
            if not constraint_exists:
                table.append_constraint(
                    CheckConstraint(check_expr, name=constraint_name)
                )

    # Generate the CREATE TABLE DDL
    return str(CreateTable(table).compile(engine))


def export_schema_to_sql(output_file: str = "database_schema.sql", dialect: str = "sqlite"):
    """
    Export the database schema to a SQL file.

    Args:
        output_file: Path to the output SQL file
        dialect: SQL dialect to use ('sqlite', 'postgresql', 'mysql', etc.)
    """
    # Create an engine for the specified dialect
    # We use a dummy connection string since we only need DDL generation
    if dialect == "sqlite":
        engine = create_engine("sqlite:///:memory:", echo=False)
    elif dialect == "postgresql":
        engine = create_engine("postgresql://dummy", echo=False,
                               strategy='mock', executor=lambda sql, *_: None)
    elif dialect == "mysql":
        engine = create_engine("mysql://dummy", echo=False,
                               strategy='mock', executor=lambda sql, *_: None)
    else:
        raise ValueError(f"Unsupported dialect: {dialect}")

    # Open the output file
    output_path = Path(output_file)
    print(f"Exporting database schema to: {output_path.absolute()}")

    with open(output_path, 'w', encoding='utf-8') as f:
        # Write header
        f.write(f"-- Database Schema for GenewebPy\n")
        f.write(f"-- Generated using SQLAlchemy ORM\n")
        f.write(f"-- Dialect: {dialect}\n")
        f.write(f"-- Total tables: {len(Base.metadata.tables)}\n")
        f.write("\n")

        # Write CREATE TABLE statements for each table
        for table_name, table in Base.metadata.tables.items():
            f.write(f"-- Table: {table_name}\n")
            create_ddl = create_table_with_check_constraints(table, engine)
            f.write(create_ddl)
            f.write(";\n\n")

        # Write table list at the end for reference
        f.write("-- List of all tables:\n")
        for i, table_name in enumerate(sorted(Base.metadata.tables.keys()), 1):
            f.write(f"-- {i}. {table_name}\n")

    print(f"✓ Schema exported successfully!")
    print(f"  Total tables: {len(Base.metadata.tables)}")
    print(f"  Output file: {output_path.absolute()}")


def list_tables():
    """List all tables in the database schema."""
    print("Tables defined in the database:")
    print("-" * 50)
    for i, table_name in enumerate(sorted(Base.metadata.tables.keys()), 1):
        table = Base.metadata.tables[table_name]
        column_count = len(table.columns)
        fk_count = len(table.foreign_keys)
        print(f"{i:2}. {table_name:30} ({column_count} columns, {fk_count} FKs)")
    print("-" * 50)
    print(f"Total: {len(Base.metadata.tables)} tables")


def export_schema_with_data_template(output_file: str = "database_with_sample_data.sql"):
    """
    Export schema with INSERT statement templates for sample data.

    Args:
        output_file: Path to the output SQL file
    """
    engine = create_engine("sqlite:///:memory:", echo=False)
    output_path = Path(output_file)

    print(f"Exporting schema with data templates to: {output_path.absolute()}")

    with open(output_path, 'w', encoding='utf-8') as f:
        # Write header
        f.write("-- Database Schema with Sample Data Templates\n")
        f.write("-- Generated using SQLAlchemy ORM\n\n")

        # Write CREATE TABLE statements
        f.write("-- CREATE TABLE statements\n")
        f.write("-- " + "=" * 70 + "\n\n")

        for table_name, table in Base.metadata.tables.items():
            f.write(f"-- Table: {table_name}\n")
            create_ddl = str(CreateTable(table).compile(engine))
            f.write(create_ddl)
            f.write(";\n\n")

        # Write INSERT templates
        f.write("\n-- INSERT statement templates\n")
        f.write("-- " + "=" * 70 + "\n\n")

        for table_name, table in Base.metadata.tables.items():
            columns = [col.name for col in table.columns if col.name != 'id']
            if columns:
                f.write(f"-- Sample INSERT for {table_name}:\n")
                f.write(
                    f"-- INSERT INTO {table_name} ({', '.join(columns)})\n")
                f.write(
                    f"--   VALUES ({', '.join(['?' for _ in columns])});\n\n")

    print(f"✓ Schema with templates exported successfully!")
    print(f"  Output file: {output_path.absolute()}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Export SQLAlchemy database schema to SQL file"
    )
    parser.add_argument(
        "-o", "--output",
        default="database_schema.sql",
        help="Output SQL file path (default: database_schema.sql)"
    )
    parser.add_argument(
        "-d", "--dialect",
        choices=["sqlite", "postgresql", "mysql"],
        default="sqlite",
        help="SQL dialect (default: sqlite)"
    )
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List all tables and exit"
    )
    parser.add_argument(
        "-t", "--template",
        action="store_true",
        help="Export with INSERT statement templates"
    )

    args = parser.parse_args()

    if args.list:
        list_tables()
    elif args.template:
        export_schema_with_data_template(args.output)
    else:
        export_schema_to_sql(args.output, args.dialect)
