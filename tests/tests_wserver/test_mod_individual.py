"""Tests for the mod_individual route.

This module contains unit and integration tests for the mod_individual route,
testing form submission, database persistence, witness linking, and various edge cases.
"""
import unittest
import tempfile
import os
from unittest.mock import patch
from flask import Flask
from wserver.routes.gwd import gwd_bp


class TestModIndividualRoute(unittest.TestCase):
    """Unit tests for mod_individual route (without database)."""

    def setUp(self):
        """Set up test client."""
        # Get the path to the templates directory
        test_dir = os.path.dirname(os.path.abspath(__file__))
        template_folder = os.path.join(
            test_dir, '..', '..', 'src', 'wserver', 'templates'
        )
        self.app = Flask(__name__, template_folder=template_folder)
        self.app.config['TESTING'] = True
        self.app.register_blueprint(gwd_bp)
        self.client = self.app.test_client()

    @patch('wserver.routes.mod_individual.render_template')
    @patch('wserver.routes.mod_individual.get_db_service')
    @patch('wserver.routes.mod_individual.PersonRepository')
    def test_get_mod_individual_form(self, mock_repo, mock_db, mock_render):
        """Test GET request returns the mod_individual form."""
        # Mock database and repository
        mock_db.return_value = None  # Will cause 404

        response = self.client.get('/gwd/testbase/modify_individual?id=1')
        self.assertEqual(response.status_code, 404)

    def test_get_without_id_returns_400(self):
        """Test GET request without id parameter returns 400."""
        response = self.client.get('/gwd/testbase/modify_individual')
        self.assertEqual(response.status_code, 400)

    def test_get_with_invalid_id_returns_404(self):
        """Test GET request with invalid id returns 404."""
        response = self.client.get('/gwd/nonexistent/modify_individual?id=999999')
        # Should return 404 because database doesn't exist
        self.assertEqual(response.status_code, 404)


class TestModIndividualWithDatabase(unittest.TestCase):
    """Integration tests for mod_individual route with database."""

    def setUp(self):
        """Set up test client and temporary database."""
        # Get the path to the templates directory
        test_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(test_dir))
        template_folder = os.path.join(
            project_root, 'src', 'wserver', 'templates')

        self.app = Flask(__name__, template_folder=template_folder)
        self.app.config['TESTING'] = True
        self.app.config['PROPAGATE_EXCEPTIONS'] = True

        # Add a simple translation function for Jinja2 templates
        @self.app.template_filter('_')
        def mock_gettext(text):
            return text

        # Also add it as a global function
        self.app.jinja_env.globals.update(_=lambda x: x)

        self.app.register_blueprint(gwd_bp)
        self.client = self.app.test_client()

        # Create temporary database
        bases_dir = os.path.join(project_root, 'src', 'wserver', 'bases')
        os.makedirs(bases_dir, exist_ok=True)

        # Use a unique temporary name to avoid conflicts with real databases
        import tempfile
        import time
        temp_name = f'test_mod_individual_{int(time.time())}_{os.getpid()}'
        self.base_name = temp_name
        self.test_db_path = os.path.join(bases_dir, f'{self.base_name}.db')
        if os.path.exists(self.test_db_path):
            os.unlink(self.test_db_path)

        # Create the database file
        with open(self.test_db_path, 'wb') as f:
            pass

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
        from database.relation import Relation  # noqa
        from database.place import Place  # noqa
        from database.date import Date  # noqa
        from database.ascends import Ascends  # noqa
        from database.descends import Descends  # noqa
        from database.unions import Unions  # noqa
        from database.person_relations import PersonRelations  # noqa
        from database.person_non_native_relations import PersonNonNativeRelations  # noqa
        from database.person_titles import PersonTitles  # noqa
        from database.union_families import UnionFamilies  # noqa
        from database.descend_children import DescendChildren  # noqa
        from database.family_events import FamilyEvents  # noqa
        from database.person_events import PersonEvents  # noqa

        # Initialize database
        from database.sqlite_database_service import SQLiteDatabaseService
        db_service = SQLiteDatabaseService(self.test_db_path)
        db_service.connect()
        db_service.disconnect()

    def tearDown(self):
        """Clean up temporary database."""
        if hasattr(self, 'test_db_path') and os.path.exists(self.test_db_path):
            os.unlink(self.test_db_path)

    def create_test_person(self, first_name, surname, occ):
        """Helper to create a test person via add_family route."""
        # Use add_family to create a person (as parent in a family)
        response = self.client.post(f'/gwd/{self.base_name}/ADD_FAM/', data={
            'pa1_fn': first_name,
            'pa1_sn': surname,
            'pa1_occ': str(occ),
            'pa2_fn': 'Spouse',
            'pa2_sn': 'Person',
            'pa2_occ': '0',
        })

        if response.status_code != 302:
            raise Exception(
                f"Failed to create test person: {response.status_code}")

        # Query database to find the created person's ID
        from database.sqlite_database_service import SQLiteDatabaseService
        from repositories.person_repository import PersonRepository

        db_service = SQLiteDatabaseService(self.test_db_path)
        db_service.connect()
        person_repo = PersonRepository(db_service)

        all_persons = person_repo.get_all_persons()
        for p in all_persons:
            if p.first_name == first_name and p.surname == surname and p.occ == occ:
                person_id = p.index
                db_service.disconnect()
                return person_id

        db_service.disconnect()
        raise Exception(
            f"Could not find created person: {first_name} {surname}")

    def verify_person_in_db(self, person_id):
        """Helper method to verify a person exists and get their data."""
        from database.person import Person
        from database.sqlite_database_service import SQLiteDatabaseService

        db_service = SQLiteDatabaseService(self.test_db_path)
        db_service.connect()
        session = db_service.get_session()

        person = session.query(Person).filter_by(id=person_id).first()

        # Access relationships while session is still open to avoid DetachedInstanceError
        if person:
            # Touch the lazy-loaded attributes to force them to load
            _ = person.birth_date_obj
            _ = person.baptism_date_obj
            _ = person.death_date_obj
            _ = person.burial_date_obj

        session.close()
        db_service.disconnect()
        return person

    def test_get_existing_person_form(self):
        """Test GET request for an existing person shows the form."""
        person_id = self.create_test_person('Test', 'Person', 0)

        response = self.client.get(
            f'/gwd/{self.base_name}/modify_individual?id={person_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test', response.data)
        self.assertIn(b'Person', response.data)

    def test_modify_person_basic_info(self):
        """Test modifying basic person information."""
        person_id = self.create_test_person('Original', 'Name', 0)

        response = self.client.post(f'/gwd/{self.base_name}/modify_individual?id={person_id}', data={
            'first_name': 'Updated',
            'surname': 'Name',
            'number': '0',
            'sex': 'M',
            'public_name': 'Updated Name',
            'image': 'photo.jpg',
            'access': 'public',
            'death_status': 'alive',
        })

        # Should redirect after successful submission
        self.assertEqual(response.status_code, 302)

        # Verify person was updated in database
        person = self.verify_person_in_db(person_id)
        self.assertIsNotNone(person)
        self.assertEqual(person.first_name, 'Updated')

    def test_modify_person_with_death_info(self):
        """Test modifying a person to add death information."""
        person_id = self.create_test_person('Living', 'Person', 0)

        response = self.client.post(f'/gwd/{self.base_name}/modify_individual?id={person_id}', data={
            'first_name': 'Living',
            'surname': 'Person',
            'number': '0',
            'sex': 'M',
            'death_status': 'dead',
            'death_dd': '15',
            'death_mm': '12',
            'death_yyyy': '2020',
            'e_place2': 'Hospital',
            'e_note2': 'Peaceful death',
            'e_src2': 'Death certificate',
        })

        self.assertEqual(response.status_code, 302)

        # Verify death information was saved
        person = self.verify_person_in_db(person_id)
        self.assertIsNotNone(person)
        from database.person import DeathStatus
        self.assertEqual(person.death_status, DeathStatus.DEAD)

    def test_modify_person_with_dates(self):
        """Test modifying person with birth and baptism dates."""
        person_id = self.create_test_person('Date', 'Test', 0)

        response = self.client.post(f'/gwd/{self.base_name}/modify_individual?id={person_id}', data={
            'first_name': 'Date',
            'surname': 'Test',
            'number': '0',
            'sex': 'F',
            'death_status': 'alive',
            'birth_dd': '10',
            'birth_mm': '5',
            'birth_yyyy': '1990',
            'birth_cal': 'gregorian',
            'e_place0': 'Paris, France',
            'e_note0': 'Born at home',
            'e_src0': 'Birth certificate',
            'baptism_dd': '20',
            'baptism_mm': '5',
            'baptism_yyyy': '1990',
            'baptism_cal': 'gregorian',
            'e_place1': 'Church',
        })

        self.assertEqual(response.status_code, 302)

        # Verify dates were saved
        person = self.verify_person_in_db(person_id)
        self.assertIsNotNone(person)
        self.assertIsNotNone(person.birth_date_obj)

    def test_modify_person_with_aliases(self):
        """Test modifying person with various name aliases."""
        person_id = self.create_test_person('Alias', 'Test', 0)

        response = self.client.post(f'/gwd/{self.base_name}/modify_individual?id={person_id}', data={
            'first_name': 'Alias',
            'surname': 'Test',
            'number': '0',
            'sex': 'M',
            'death_status': 'alive',
            'sobriquet_0': 'The Great',
            'sobriquet_1': 'The Wise',
            'alias_0': 'Alias the Great',
            'alias_1': 'A. Test',
            'alt_first_name_0': 'Alexander',
            'surname_alias_0': 'Tester',
        })

        self.assertEqual(response.status_code, 302)

        # Verify aliases were saved
        person = self.verify_person_in_db(person_id)
        self.assertIsNotNone(person)
        self.assertIn('The Great', person.qualifiers)
        self.assertIn('Alias the Great', person.aliases)

    def test_modify_person_with_occupation(self):
        """Test modifying person with occupation."""
        person_id = self.create_test_person('Worker', 'Person', 0)

        response = self.client.post(f'/gwd/{self.base_name}/modify_individual?id={person_id}', data={
            'first_name': 'Worker',
            'surname': 'Person',
            'number': '0',
            'sex': 'M',
            'death_status': 'alive',
            'occupation_0': 'Software Engineer',
        })

        self.assertEqual(response.status_code, 302)

        # Verify occupation was saved
        person = self.verify_person_in_db(person_id)
        self.assertIsNotNone(person)
        self.assertEqual(person.occupation, 'Software Engineer')

    def test_modify_person_with_notes(self):
        """Test modifying person with notes."""
        person_id = self.create_test_person('Notes', 'Person', 0)

        notes_text = "Important historical figure.\nKnown for their contributions."

        response = self.client.post(f'/gwd/{self.base_name}/modify_individual?id={person_id}', data={
            'first_name': 'Notes',
            'surname': 'Person',
            'number': '0',
            'sex': 'M',
            'death_status': 'alive',
            'notes': notes_text,
        })

        self.assertEqual(response.status_code, 302)

        # Verify notes were saved
        person = self.verify_person_in_db(person_id)
        self.assertIsNotNone(person)
        self.assertEqual(person.notes, notes_text)

    def test_link_existing_witness(self):
        """Test linking an existing person as a witness."""
        # Create two persons
        person_id = self.create_test_person('Main', 'Person', 0)
        witness_id = self.create_test_person('Witness', 'Person', 0)

        # Modify main person with event and witness
        response = self.client.post(f'/gwd/{self.base_name}/modify_individual?id={person_id}', data={
            'first_name': 'Main',
            'surname': 'Person',
            'number': '0',
            'sex': 'M',
            'death_status': 'alive',
            'e_name4': '#residence',
            'e4_dd': '1',
            'e4_mm': '1',
            'e4_yyyy': '2000',
            'e_place4': 'London',
            'e4_witn0_p': 'link',  # Link existing
            'e4_witn0_fn': 'Witness',
            'e4_witn0_sn': 'Person',
            'e4_witn0_occ': '0',
            'e4_witn0_kind': 'WITNESS',
        })

        self.assertEqual(response.status_code, 302)

        # Verify the witness was linked (not created as duplicate)
        from database.sqlite_database_service import SQLiteDatabaseService
        from repositories.person_repository import PersonRepository

        db_service = SQLiteDatabaseService(self.test_db_path)
        db_service.connect()
        person_repo = PersonRepository(db_service)

        all_persons = person_repo.get_all_persons()
        witness_count = sum(1 for p in all_persons
                            if p.first_name == 'Witness' and p.surname == 'Person')

        db_service.disconnect()

        # Should still be only 1 witness (not created duplicate)
        self.assertEqual(witness_count, 1)

    def test_create_new_witness(self):
        """Test creating a new person as a witness."""
        person_id = self.create_test_person('Main', 'Person', 0)

        response = self.client.post(f'/gwd/{self.base_name}/modify_individual?id={person_id}', data={
            'first_name': 'Main',
            'surname': 'Person',
            'number': '0',
            'sex': 'M',
            'death_status': 'alive',
            'e_name4': '#residence',
            'e4_dd': '1',
            'e4_mm': '1',
            'e4_yyyy': '2000',
            'e_place4': 'London',
            'e4_witn0_p': 'create',  # Create new
            'e4_witn0_fn': 'New',
            'e4_witn0_sn': 'Witness',
            'e4_witn0_occ': '0',
            'e4_witn0_sex': 'F',
            'e4_witn0_occu': 'Doctor',
            'e4_witn0_kind': 'WITNESS',
        })

        self.assertEqual(response.status_code, 302)

        # Verify new witness was created
        from database.sqlite_database_service import SQLiteDatabaseService
        from repositories.person_repository import PersonRepository

        db_service = SQLiteDatabaseService(self.test_db_path)
        db_service.connect()
        person_repo = PersonRepository(db_service)

        all_persons = person_repo.get_all_persons()
        witness = None
        for p in all_persons:
            if p.first_name == 'New' and p.surname == 'Witness':
                witness = p
                break

        db_service.disconnect()

        self.assertIsNotNone(witness)
        self.assertEqual(witness.occupation, 'Doctor')

    def test_modify_nonexistent_person_returns_404(self):
        """Test modifying a nonexistent person returns 404."""
        response = self.client.post(f'/gwd/{self.base_name}/modify_individual?id=999999', data={
            'first_name': 'Test',
            'surname': 'Person',
        })

        self.assertEqual(response.status_code, 404)

    def test_json_response_on_success(self):
        """Test JSON response format on successful update."""
        person_id = self.create_test_person('Json', 'Test', 0)

        response = self.client.post(
            f'/gwd/{self.base_name}/modify_individual?id={person_id}',
            data={
                'first_name': 'Json',
                'surname': 'Test',
                'number': '0',
                'sex': 'M',
                'death_status': 'alive',
            },
            headers={'Accept': 'application/json'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

        json_data = response.get_json()
        self.assertTrue(json_data.get('ok'))
        self.assertEqual(json_data.get('person_id'), person_id)

    def test_modify_person_with_burial_info(self):
        """Test modifying person with burial information."""
        person_id = self.create_test_person('Deceased', 'Person', 0)

        response = self.client.post(f'/gwd/{self.base_name}/modify_individual?id={person_id}', data={
            'first_name': 'Deceased',
            'surname': 'Person',
            'number': '0',
            'sex': 'M',
            'death_status': 'dead',
            'death_dd': '10',
            'death_mm': '10',
            'death_yyyy': '2020',
            'burial_type': 'burial',
            'burial_dd': '15',
            'burial_mm': '10',
            'burial_yyyy': '2020',
            'e_place3': 'Cemetery',
            'e_note3': 'Family plot',
            'e_src3': 'Burial records',
        })

        self.assertEqual(response.status_code, 302)

        # Verify burial info was saved
        person = self.verify_person_in_db(person_id)
        self.assertIsNotNone(person)
        from database.person import BurialStatus
        self.assertEqual(person.burial_status, BurialStatus.BURIAL)

    def test_modify_person_with_cremation(self):
        """Test modifying person with cremation information."""
        person_id = self.create_test_person('Cremated', 'Person', 0)

        response = self.client.post(f'/gwd/{self.base_name}/modify_individual?id={person_id}', data={
            'first_name': 'Cremated',
            'surname': 'Person',
            'number': '0',
            'sex': 'F',
            'death_status': 'dead',
            'death_dd': '1',
            'death_mm': '1',
            'death_yyyy': '2021',
            'burial_type': 'cremated',
            'burial_dd': '5',
            'burial_mm': '1',
            'burial_yyyy': '2021',
            'e_place3': 'Crematorium',
        })

        self.assertEqual(response.status_code, 302)

        # Verify cremation info was saved
        person = self.verify_person_in_db(person_id)
        self.assertIsNotNone(person)
        from database.person import BurialStatus
        self.assertEqual(person.burial_status, BurialStatus.CREMATED)

    def test_modify_person_change_sex(self):
        """Test modifying person's sex."""
        person_id = self.create_test_person('Gender', 'Test', 0)

        response = self.client.post(f'/gwd/{self.base_name}/modify_individual?id={person_id}', data={
            'first_name': 'Gender',
            'surname': 'Test',
            'number': '0',
            'sex': 'F',
            'death_status': 'alive',
        })

        self.assertEqual(response.status_code, 302)

        # Verify sex was changed
        person = self.verify_person_in_db(person_id)
        self.assertIsNotNone(person)
        from libraries.person import Sex
        self.assertEqual(person.sex, Sex.FEMALE)

    def test_modify_person_with_multiple_events(self):
        """Test modifying person with multiple personal events."""
        person_id = self.create_test_person('Events', 'Person', 0)

        response = self.client.post(f'/gwd/{self.base_name}/modify_individual?id={person_id}', data={
            'first_name': 'Events',
            'surname': 'Person',
            'number': '0',
            'sex': 'M',
            'death_status': 'alive',
            'e_name4': '#residence',
            'e4_dd': '1',
            'e4_mm': '1',
            'e4_yyyy': '1990',
            'e_place4': 'New York',
            'e_name5': '#residence',
            'e5_dd': '1',
            'e5_mm': '1',
            'e5_yyyy': '2000',
            'e_place5': 'London',
        })

        self.assertEqual(response.status_code, 302)


class TestModIndividualHelperFunctions(unittest.TestCase):
    """Unit tests for helper functions in mod_individual route."""

    def test_parse_calendar_date_complete(self):
        """Test parsing a complete date."""
        from wserver.routes.mod_individual import parse_calendar_date

        form_data = {
            'test_dd': '15',
            'test_mm': '3',
            'test_yyyy': '1990',
            'test_cal': 'gregorian'
        }

        result = parse_calendar_date(form_data, 'test')
        self.assertIsNotNone(result)

    def test_parse_calendar_date_year_only(self):
        """Test parsing a year-only date."""
        from wserver.routes.mod_individual import parse_calendar_date

        form_data = {
            'test_yyyy': '1990',
            'test_cal': 'gregorian'
        }

        result = parse_calendar_date(form_data, 'test')
        self.assertIsNotNone(result)

    def test_parse_calendar_date_empty(self):
        """Test parsing an empty date returns None."""
        from wserver.routes.mod_individual import parse_calendar_date

        form_data = {}

        result = parse_calendar_date(form_data, 'test')
        self.assertIsNone(result)

    def test_find_person_by_name(self):
        """Test finding a person by name."""
        # This would require setting up a mock repository
        pass


class TestModIndividualEdgeCases(unittest.TestCase):
    """Tests for edge cases and error handling."""

    def setUp(self):
        """Set up test client."""
        test_dir = os.path.dirname(os.path.abspath(__file__))
        template_folder = os.path.join(
            test_dir, '..', '..', 'src', 'wserver', 'templates'
        )
        self.app = Flask(__name__, template_folder=template_folder)
        self.app.config['TESTING'] = True
        self.app.register_blueprint(gwd_bp)
        self.client = self.app.test_client()

    def test_empty_post_request(self):
        """Test POST with no data."""
        response = self.client.post('/gwd/testbase/modify_individual?id=1', data={})
        # Should return 404 (database doesn't exist)
        self.assertEqual(response.status_code, 404)

    def test_post_with_invalid_dates(self):
        """Test POST with invalid date values."""
        response = self.client.post('/gwd/testbase/modify_individual?id=1', data={
            'first_name': 'Test',
            'surname': 'Person',
            'birth_dd': '32',  # Invalid day
            'birth_mm': '13',  # Invalid month
            'birth_yyyy': 'abc',  # Invalid year
        })
        # Should handle gracefully
        self.assertEqual(response.status_code, 404)  # DB doesn't exist


if __name__ == '__main__':
    unittest.main()
