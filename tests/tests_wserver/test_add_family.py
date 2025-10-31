"""Tests for the add_family route.

This module contains unit and integration tests for the add_family route,
testing form submission, database persistence, and various edge cases.
"""

import unittest
import tempfile
import os
from unittest.mock import patch
from flask import Flask
from wserver.routes.gwd import gwd_bp


class TestAddFamilyRoute(unittest.TestCase):
    """Unit tests for add_family route (without database)."""

    def setUp(self):
        """Set up test client."""
        # Get the path to the templates directory
        test_dir = os.path.dirname(os.path.abspath(__file__))
        template_folder = os.path.join(test_dir, "..", "src", "wserver", "templates")
        self.app = Flask(__name__, template_folder=template_folder)
        self.app.config["TESTING"] = True
        self.app.register_blueprint(gwd_bp)
        self.client = self.app.test_client()

    @patch("wserver.routes.add_family.render_template")
    def test_get_add_family_form(self, mock_render):
        """Test GET request returns the add_family form."""
        mock_render.return_value = '<html><input name="pa1_fn"/></html>'
        response = self.client.get("/gwd/testbase/ADD_FAM/")
        self.assertEqual(response.status_code, 200)
        # Verify render_template was called with correct template
        mock_render.assert_called_once()
        args, kwargs = mock_render.call_args
        self.assertEqual(args[0], "gwd/add_family.html")
        self.assertEqual(kwargs["base"], "testbase")
        self.assertEqual(kwargs["lang"], "en")

    @patch("wserver.routes.add_family.render_template")
    def test_get_add_family_form_with_lang(self, mock_render):
        """Test GET request with language parameter."""
        mock_render.return_value = "<html>ok</html>"
        response = self.client.get("/gwd/testbase/ADD_FAM?lang=fr")
        self.assertEqual(response.status_code, 200)
        # Verify language was passed correctly
        args, kwargs = mock_render.call_args
        self.assertEqual(kwargs["lang"], "fr")

    def test_post_without_database_returns_404(self):
        """Test POST request when database doesn't exist returns 404."""
        response = self.client.post(
            "/gwd/nonexistent/ADD_FAM/",
            data={
                "pa1_fn": "John",
                "pa1_sn": "Doe",
            },
        )
        # Should return 404 because database doesn't exist
        self.assertEqual(response.status_code, 404)

    def test_post_json_without_database_returns_404_json(self):
        """Test POST request with JSON accept header returns JSON 404."""
        response = self.client.post(
            "/gwd/nonexistent/ADD_FAM/",
            data={"pa1_fn": "John"},
            headers={"Accept": "application/json"},
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")


class TestAddFamilyWithDatabase(unittest.TestCase):
    """Integration tests for add_family route with database."""

    def setUp(self):
        """Set up test client and temporary database."""
        # Get the path to the templates directory
        test_dir = os.path.dirname(os.path.abspath(__file__))
        template_folder = os.path.join(test_dir, "..", "src", "wserver", "templates")
        self.app = Flask(__name__, template_folder=template_folder)
        self.app.config["TESTING"] = True
        self.app.register_blueprint(gwd_bp)
        self.client = self.app.test_client()

        # Create temporary database
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        # Use a predictable base name and path for the test DB
        # The Flask app looks for databases relative to src/wserver/bases
        # So we need to put it in the ACTUAL src directory, not tests/src
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        bases_dir = os.path.join(project_root, "bases")
        os.makedirs(bases_dir, exist_ok=True)
        self.base_name = "testdb"
        self.test_db_path = os.path.join(bases_dir, f"{self.base_name}.db")
        if os.path.exists(self.test_db_path):
            os.unlink(self.test_db_path)
        # Create the database file directly at the correct location
        with open(self.test_db_path, "wb") as f:
            pass  # Just create the file

        # Import ALL models before creating database to register all tables
        # This is critical - SQLAlchemy needs all models imported
        # before Base.metadata.create_all() is called
        from database import Base  # noqa
        from database.person import Person  # noqa
        from database.family import Family  # noqa
        from database.couple import Couple  # noqa
        from database.family_event import FamilyEvent  # noqa
        from database.family_event_witness import FamilyEventWitness  # noqa
        from database.family_witness import FamilyWitness  # noqa
        from database.personal_event import PersonalEvent  # noqa
        from database.person_event_witness import PersonEventWitness  # noqa
        from database.titles import Titles  # noqa
        from database.family import Family  # noqa
        from database.couple import Couple  # noqa
        from database.relation import Relation  # noqa
        from database.place import Place  # noqa
        from database.date import Date  # noqa
        from database.ascends import Ascends  # noqa
        from database.descends import Descends  # noqa
        from database.unions import Unions  # noqa
        from database.person_relations import PersonRelations  # noqa
        from database.person_non_native_relations import (
            PersonNonNativeRelations,
        )  # noqa
        from database.person_titles import PersonTitles  # noqa
        from database.union_families import UnionFamilies  # noqa
        from database.descend_children import DescendChildren  # noqa
        from database.family_events import FamilyEvents  # noqa
        from database.person_events import PersonEvents  # noqa

        from database.sqlite_database_service import SQLiteDatabaseService

        db_service = SQLiteDatabaseService(self.test_db_path)
        db_service.connect()
        db_service.disconnect()

    def tearDown(self):
        """Clean up temporary database."""
        if hasattr(self, "test_db_path") and os.path.exists(self.test_db_path):
            os.unlink(self.test_db_path)

    def verify_person_in_db(self, first_name, surname, occ=0):
        """Helper method to verify a person exists in the database."""
        # Import all models first (required for SQLAlchemy metadata)
        from database.person import Person  # noqa
        from database.family import Family  # noqa
        from database.couple import Couple  # noqa
        from database.relation import Relation  # noqa
        from database.place import Place  # noqa
        from database.date import Date  # noqa
        from database.ascends import Ascends  # noqa
        from database.descends import Descends  # noqa
        from database.unions import Unions  # noqa
        from database.person_relations import PersonRelations  # noqa
        from database.person_non_native_relations import (
            PersonNonNativeRelations,
        )  # noqa
        from database.person_titles import PersonTitles  # noqa
        from database.union_families import UnionFamilies  # noqa
        from database.descend_children import DescendChildren  # noqa
        from database.family_events import FamilyEvents  # noqa
        from database.person_events import PersonEvents  # noqa

        from database.sqlite_database_service import SQLiteDatabaseService

        db_service = SQLiteDatabaseService(self.test_db_path)
        db_service.connect()
        session = db_service.get_session()

        person = (
            session.query(Person)
            .filter_by(first_name=first_name, surname=surname, occ=occ)
            .first()
        )

        session.close()
        db_service.disconnect()
        return person

    def verify_family_in_db(self):
        """Helper method to verify a family exists in the database."""
        from database.family import Family  # noqa
        from database.couple import Couple  # noqa
        from database.relation import Relation  # noqa
        from database.place import Place  # noqa
        from database.date import Date  # noqa
        from database.ascends import Ascends  # noqa
        from database.descends import Descends  # noqa
        from database.unions import Unions  # noqa
        from database.person_relations import PersonRelations  # noqa
        from database.person_non_native_relations import (
            PersonNonNativeRelations,
        )  # noqa
        from database.person_titles import PersonTitles  # noqa
        from database.union_families import UnionFamilies  # noqa
        from database.descend_children import DescendChildren  # noqa
        from database.family_events import FamilyEvents  # noqa
        from database.person_events import PersonEvents  # noqa

        from database.sqlite_database_service import SQLiteDatabaseService

        db_service = SQLiteDatabaseService(self.test_db_path)
        db_service.connect()
        session = db_service.get_session()

        families = session.query(Family).all()

        session.close()
        db_service.disconnect()
        return families

    def test_create_family_with_two_parents(self):
        """Test creating a family with two parents."""
        response = self.client.post(
            f"/gwd/{self.base_name}/ADD_FAM/",
            data={
                "pa1_fn": "John",
                "pa1_sn": "Doe",
                "pa1_occ": "0",
                "pa1b_dd": "15",
                "pa1b_mm": "3",
                "pa1b_yyyy": "1980",
                "pa1b_pl": "New York",
                "pa1_occu": "Engineer",
                "pa2_fn": "Jane",
                "pa2_sn": "Smith",
                "pa2_occ": "0",
                "pa2b_dd": "20",
                "pa2b_mm": "6",
                "pa2b_yyyy": "1982",
                "pa2b_pl": "Boston",
                "pa2_occu": "Doctor",
                "e_name1": "#marr",
            },
        )
        # Should redirect after successful submission
        self.assertEqual(response.status_code, 302)
        self.assertIn("/gwd/", response.location)

        # Verify both persons and family were created in database
        john = self.verify_person_in_db("John", "Doe", 0)
        self.assertIsNotNone(john, "Father 'John Doe' not found in database")
        jane = self.verify_person_in_db("Jane", "Smith", 0)
        self.assertIsNotNone(jane, "Mother 'Jane Smith' not found in database")
        families = self.verify_family_in_db()
        self.assertGreater(len(families), 0, "No families found in database")

    def test_create_family_with_dead_parent(self):
        """Test creating a family with a deceased parent."""
        response = self.client.post(
            f"/gwd/{self.base_name}/ADD_FAM/",
            data={
                "pa1_fn": "Robert",
                "pa1_sn": "Johnson",
                "pa1_occ": "0",
                "pa1b_dd": "10",
                "pa1b_mm": "1",
                "pa1b_yyyy": "1950",
                "pa1d_dd": "15",  # Death date
                "pa1d_mm": "12",
                "pa1d_yyyy": "2020",
                "pa1d_pl": "Los Angeles",
                "pa2_fn": "Mary",
                "pa2_sn": "Williams",
                "pa2_occ": "0",
            },
        )
        self.assertEqual(response.status_code, 302)

        # Verify death status was set correctly by checking database
        try:
            # Import all models first (required for SQLAlchemy metadata)
            from database.person import Person  # noqa
            from database.family import Family  # noqa
            from database.couple import Couple  # noqa
            from database.relation import Relation  # noqa
            from database.place import Place  # noqa
            from database.date import Date  # noqa
            from database.ascends import Ascends  # noqa
            from database.descends import Descends  # noqa
            from database.unions import Unions  # noqa
            from database.person_relations import PersonRelations  # noqa
            from database.person_non_native_relations import (
                PersonNonNativeRelations,
            )  # noqa
            from database.person_titles import PersonTitles  # noqa
            from database.union_families import UnionFamilies  # noqa
            from database.descend_children import DescendChildren  # noqa
            from database.family_events import FamilyEvents  # noqa
            from database.person_events import PersonEvents  # noqa

            from database.sqlite_database_service import SQLiteDatabaseService

            db_service = SQLiteDatabaseService(self.test_db_path)
            db_service.connect()
            session = db_service.get_session()

            # Find the person we just created
            person = (
                session.query(Person)
                .filter_by(first_name="Robert", surname="Johnson", occ=0)
                .first()
            )

            self.assertIsNotNone(
                person, "Person 'Robert Johnson' not found in database"
            )
            # Death status should be set (not None or NotDead)
            self.assertIsNotNone(
                person.death_status, "Death status should be set for deceased person"
            )

            session.close()
            db_service.disconnect()
        except ImportError:
            self.skipTest("Cannot verify - SQLAlchemy not available")

    def test_create_family_with_children(self):
        """Test creating a family with children."""
        response = self.client.post(
            f"/gwd/{self.base_name}/ADD_FAM/",
            data={
                "pa1_fn": "Thomas",
                "pa1_sn": "Anderson",
                "pa1_occ": "0",
                "pa2_fn": "Sarah",
                "pa2_sn": "Connor",
                "pa2_occ": "0",
                "ch1_fn": "Emily",
                "ch1_sn": "Anderson",
                "ch1_occ": "0",
                "ch1_sex": "F",
                "ch1b_dd": "10",
                "ch1b_mm": "5",
                "ch1b_yyyy": "2010",
                "ch2_fn": "Michael",
                "ch2_sn": "Anderson",
                "ch2_occ": "0",
                "ch2_sex": "M",
                "ch2b_dd": "20",
                "ch2b_mm": "8",
                "ch2b_yyyy": "2012",
            },
        )
        self.assertEqual(response.status_code, 302)

        # Verify parents and children were created in database
        thomas = self.verify_person_in_db("Thomas", "Anderson", 0)
        self.assertIsNotNone(thomas, "Father 'Thomas Anderson' not found in database")
        sarah = self.verify_person_in_db("Sarah", "Connor", 0)
        self.assertIsNotNone(sarah, "Mother 'Sarah Connor' not found in database")
        emily = self.verify_person_in_db("Emily", "Anderson", 0)
        self.assertIsNotNone(emily, "Child 'Emily Anderson' not found in database")
        michael = self.verify_person_in_db("Michael", "Anderson", 0)
        self.assertIsNotNone(michael, "Child 'Michael Anderson' not found in database")

    def test_create_family_with_events(self):
        """Test creating a family with events (marriage)."""
        response = self.client.post(
            f"/gwd/{self.base_name}/ADD_FAM/",
            data={
                "pa1_fn": "David",
                "pa1_sn": "Miller",
                "pa1_occ": "0",
                "pa2_fn": "Lisa",
                "pa2_sn": "Brown",
                "pa2_occ": "0",
                "e_name1": "#marr",
                "e1_dd": "15",
                "e1_mm": "6",
                "e1_yyyy": "2005",
                "e1_pl": "Paris",
                "e1_note": "Beautiful ceremony",
                "e1_src": "Marriage certificate",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_create_family_with_witnesses(self):
        """Test creating a family with event witnesses."""
        response = self.client.post(
            f"/gwd/{self.base_name}/ADD_FAM/",
            data={
                "pa1_fn": "James",
                "pa1_sn": "Wilson",
                "pa1_occ": "0",
                "pa2_fn": "Patricia",
                "pa2_sn": "Taylor",
                "pa2_occ": "0",
                "e_name1": "#marr",
                "e1_dd": "20",
                "e1_mm": "9",
                "e1_yyyy": "2008",
                "e1_pl": "London",
                "e1_witn1_fn": "Richard",
                "e1_witn1_sn": "Moore",
                "e1_witn1_occ": "0",
                "e1_witn1_sex": "M",
                "e1_witn1_kind": "WITNESS",
                "e1_witn2_fn": "Jennifer",
                "e1_witn2_sn": "Garcia",
                "e1_witn2_occ": "0",
                "e1_witn2_sex": "F",
                "e1_witn2_kind": "WITNESS",
            },
        )
        self.assertEqual(response.status_code, 302)

        # Verify parents and witnesses were created in database
        james = self.verify_person_in_db("James", "Wilson", 0)
        self.assertIsNotNone(james, "Father 'James Wilson' not found in database")
        patricia = self.verify_person_in_db("Patricia", "Taylor", 0)
        self.assertIsNotNone(patricia, "Mother 'Patricia Taylor' not found in database")
        richard = self.verify_person_in_db("Richard", "Moore", 0)
        self.assertIsNotNone(richard, "Witness 'Richard Moore' not found in database")
        jennifer = self.verify_person_in_db("Jennifer", "Garcia", 0)
        self.assertIsNotNone(
            jennifer, "Witness 'Jennifer Garcia' not found in database"
        )

    def test_create_family_minimal_data(self):
        """Test creating a family with minimal required data."""
        response = self.client.post(
            f"/gwd/{self.base_name}/ADD_FAM/",
            data={
                "pa1_fn": "Min",
                "pa1_sn": "Father",
                "pa2_fn": "Min",
                "pa2_sn": "Mother",
            },
        )
        self.assertEqual(response.status_code, 302)

        # Verify persons were created in database
        father = self.verify_person_in_db("Min", "Father", 0)
        self.assertIsNotNone(father, "Father 'Min Father' not found in database")
        mother = self.verify_person_in_db("Min", "Mother", 0)
        self.assertIsNotNone(mother, "Mother 'Min Mother' not found in database")

    def test_json_response_includes_family_id(self):
        """Test JSON response includes the created family ID."""
        response = self.client.post(
            f"/gwd/{self.base_name}/ADD_FAM/",
            data={
                "pa1_fn": "Json",
                "pa1_sn": "Test",
                "pa2_fn": "Json",
                "pa2_sn": "Test2",
            },
            headers={"Accept": "application/json"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

        json_data = response.get_json()
        self.assertTrue(json_data.get("ok"))
        self.assertIn("family_id", json_data)
        self.assertIsInstance(json_data["family_id"], int)

    def test_link_existing_parent(self):
        """Test linking to an existing parent person."""
        # First, create a person
        self.client.post(
            f"/gwd/{self.base_name}/ADD_FAM/",
            data={
                "pa1_fn": "Existing",
                "pa1_sn": "Person",
                "pa1_occ": "0",
                "pa2_fn": "New",
                "pa2_sn": "Person",
            },
        )

        # Now create a new family linking to the existing person
        response = self.client.post(
            f"/gwd/{self.base_name}/ADD_FAM/",
            data={
                "pa1_p": "link",  # Link mode
                "pa1_fn": "Existing",
                "pa1_sn": "Person",
                "pa1_occ": "0",
                "pa2_fn": "Another",
                "pa2_sn": "Person",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_link_nonexistent_parent_fails(self):
        """Test that linking to a nonexistent parent returns error."""
        response = self.client.post(
            f"/gwd/{self.base_name}/ADD_FAM/",
            data={
                "pa1_p": "link",
                "pa1_fn": "DoesNotExist",
                "pa1_sn": "Person",
                "pa1_occ": "0",
                "pa2_fn": "Test",
                "pa2_sn": "Person",
            },
        )
        # Should fail with 400 bad request
        self.assertEqual(response.status_code, 400)

    def test_multiple_events(self):
        """Test creating a family with multiple events."""
        response = self.client.post(
            f"/gwd/{self.base_name}/ADD_FAM/",
            data={
                "pa1_fn": "Multi",
                "pa1_sn": "Event",
                "pa2_fn": "Multi",
                "pa2_sn": "Event2",
                "e_name1": "#marr",
                "e1_dd": "10",
                "e1_mm": "5",
                "e1_yyyy": "2000",
                "e_name2": "divorce",
                "e2_dd": "15",
                "e2_mm": "8",
                "e2_yyyy": "2010",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_different_marital_statuses(self):
        """Test creating families with different marital statuses."""
        test_cases = [
            ("#marr", "married couple"),
            ("not married", "unmarried couple"),
            ("engaged", "engaged couple"),
            ("civil union", "civil union"),
            ("residence", "residence"),
        ]

        for event_name, description in test_cases:
            with self.subTest(marital_status=description):
                response = self.client.post(
                    f"/gwd/{self.base_name}/ADD_FAM/",
                    data={
                        "pa1_fn": f'Test_{description.replace(" ", "_")}',
                        "pa1_sn": "Father",
                        "pa2_fn": f'Test_{description.replace(" ", "_")}',
                        "pa2_sn": "Mother",
                        "e_name1": event_name,
                    },
                )
                self.assertEqual(response.status_code, 302)


class TestAddFamilyHelperFunctions(unittest.TestCase):
    """Unit tests for helper functions in add_family route."""

    def setUp(self):
        """Set up test environment."""
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True

    def test_form_field_parsing(self):
        """Test that form fields are parsed correctly."""
        # This would require accessing internal functions
        # or refactoring them to be testable independently
        pass

    def test_date_parsing(self):
        """Test calendar date parsing logic."""
        # Test various date formats
        # This would require the parse_calendar_date function to be importable
        pass


class TestAddFamilyEdgeCases(unittest.TestCase):
    """Tests for edge cases and error handling."""

    def setUp(self):
        """Set up test client."""
        # Get the path to the templates directory
        test_dir = os.path.dirname(os.path.abspath(__file__))
        template_folder = os.path.join(test_dir, "..", "src", "wserver", "templates")
        self.app = Flask(__name__, template_folder=template_folder)
        self.app.config["TESTING"] = True
        self.app.register_blueprint(gwd_bp)
        self.client = self.app.test_client()

    def test_empty_post_request(self):
        """Test POST with no data."""
        response = self.client.post("/gwd/testbase/ADD_FAM/", data={})
        # Should return 404 (database doesn't exist) or handle gracefully
        self.assertIn(response.status_code, [400, 404])


if __name__ == "__main__":
    unittest.main()
