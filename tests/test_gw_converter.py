# """Tests for GeneWeb to application type converter.

# Tests the conversion from GwSyntax (parsed GeneWeb) to application types
# defined in libraries/.
# """

# from typing import List
# import pytest
# from dataclasses import replace

# from script.gw_parser.gw_converter import GwConverter, convert_gw_file
# from script.gw_parser.data_types import (
#     FamilyGwSyntax,
#     Key,
#     NotesGwSyntax,
#     PersonalEventsGwSyntax,
#     RelationsGwSyntax,
#     Somebody,
#     SomebodyDefined,
#     SomebodyUndefined,
# )
# from libraries.person import Person, Sex
# from libraries.family import (
#     Family,
#     Parents,
#     Relation,
#     Ascendants,
#     MaritalStatus,
#     NotDivorced,
#     RelationToParentType,
# )
# from libraries.consanguinity_rate import ConsanguinityRate
# from libraries.events import PersGraduate, PersonalEvent
# from libraries.date import CalendarDate, DateValue, Calendar, Sure
# from libraries.burial_info import UnknownBurial
# from libraries.death_info import NotDead
# from libraries.title import AccessRight


# @pytest.fixture
# def simple_person() -> Person[int, int, str, int]:
#     """Create a simple person for testing."""
#     date = CalendarDate(
#         dmy=DateValue(day=1, month=1, year=1950, prec=Sure(), delta=0),
#         cal=Calendar.GREGORIAN
#     )
#     return Person(
#         index=0,
#         first_name="John",
#         surname="Doe",
#         occ=0,
#         image="",
#         public_name="",
#         qualifiers=[],
#         aliases=[],
#         first_names_aliases=[],
#         surname_aliases=[],
#         titles=[],
#         non_native_parents_relation=[],
#         related_persons=[],
#         occupation="",
#         sex=Sex.MALE,
#         access_right=AccessRight.PUBLIC,
#         birth_date=date,
#         birth_place="",
#         birth_note="",
#         birth_src="",
#         baptism_date=None,
#         baptism_place="",
#         baptism_note="",
#         baptism_src="",
#         death_status=NotDead(),
#         death_place="",
#         death_note="",
#         death_src="",
#         burial=UnknownBurial(),
#         burial_place="",
#         burial_note="",
#         burial_src="",
#         personal_events=[],
#         notes="",
#         src="",
#         ascend=Ascendants(
#             parents=None,
#             consanguinity_rate=ConsanguinityRate.from_integer(-1)
#         ),
#         families=[],
#     )


# @pytest.fixture
# def another_person() -> Person[int, int, str, int]:
#     """Create another person for testing."""
#     date = CalendarDate(
#         dmy=DateValue(day=1, month=1, year=1952, prec=Sure(), delta=0),
#         cal=Calendar.GREGORIAN
#     )
#     return Person(
#         index=1,
#         first_name="Jane",
#         surname="Smith",
#         occ=0,
#         image="",
#         public_name="",
#         qualifiers=[],
#         aliases=[],
#         first_names_aliases=[],
#         surname_aliases=[],
#         titles=[],
#         non_native_parents_relation=[],
#         related_persons=[],
#         occupation="",
#         sex=Sex.FEMALE,
#         access_right=AccessRight.PUBLIC,
#         birth_date=date,
#         birth_place="",
#         birth_note="",
#         birth_src="",
#         baptism_date=None,
#         baptism_place="",
#         baptism_note="",
#         baptism_src="",
#         death_status=NotDead(),
#         death_place="",
#         death_note="",
#         death_src="",
#         burial=UnknownBurial(),
#         burial_place="",
#         burial_note="",
#         burial_src="",
#         personal_events=[],
#         notes="",
#         src="",
#         ascend=Ascendants(
#             parents=None,
#             consanguinity_rate=ConsanguinityRate.from_integer(-1)
#         ),
#         families=[],
#     )


# class TestGwConverterInit:
#     """Test converter initialization."""

#     def test_converter_initialization(self):
#         """Test that converter initializes with empty structures."""
#         converter = GwConverter()

#         assert converter.person_index_counter == 0
#         assert converter.family_index_counter == 0
#         assert len(converter.person_by_key) == 0
#         assert len(converter.families) == 0
#         assert len(converter.notes) == 0
#         assert len(converter.relations) == 0
#         assert len(converter.personal_events) == 0


# class TestKeyTuple:
#     """Test key tuple conversion."""

#     def test_key_tuple_conversion(self):
#         """Test converting Key to tuple."""
#         converter = GwConverter()
#         key = Key(pk_first_name="John", pk_surname="Doe", pk_occ=0)

#         result = converter.key_tuple(key)

#         assert result == ("John", "Doe", 0)

#     def test_key_tuple_with_occurrence(self):
#         """Test key tuple with non-zero occurrence."""
#         converter = GwConverter()
#         key = Key(pk_first_name="John", pk_surname="Doe", pk_occ=5)

#         result = converter.key_tuple(key)

#         assert result == ("John", "Doe", 5)


# class TestResolveSomebody:
#     """Test resolving Somebody references."""

#     def test_resolve_somebody_defined(self, simple_person):
#         """Test resolving a SomebodyDefined."""
#         converter = GwConverter()
#         somebody = SomebodyDefined(person=simple_person)

#         result = converter.resolve_somebody(somebody)

#         assert result == simple_person
#         assert result.first_name == "John"
#         assert result.surname == "Doe"

#     def test_resolve_somebody_undefined_success(self, simple_person):
#         """Test resolving a SomebodyUndefined that exists."""
#         converter = GwConverter()
#         key = Key(pk_first_name="John", pk_surname="Doe", pk_occ=0)

#         # Register the person first
#         converter.person_by_key[("John", "Doe", 0)] = simple_person

#         somebody = SomebodyUndefined(key=key)
#         result = converter.resolve_somebody(somebody)

#         assert result == simple_person

#     def test_resolve_somebody_undefined_failure(self):
#         """Test resolving SomebodyUndefined creates dummy if doesn't exist."""
#         converter = GwConverter()
#         key = Key(pk_first_name="Unknown", pk_surname="Person", pk_occ=0)
#         somebody = SomebodyUndefined(key=key)

#         # Should create a dummy person
#         result = converter.resolve_somebody(somebody)

#         assert result.first_name == "Unknown"
#         assert result.surname == "Person"
#         assert result.occ == 0
#         # Check it's marked as a dummy
#         key_tuple = converter.key_tuple(key)
#         assert key_tuple in converter.dummy_persons

#     def test_resolve_somebody_invalid_type(self):
#         """Test resolving an invalid Somebody type."""
#         converter = GwConverter()

#         with pytest.raises(TypeError, match="Unknown Somebody type"):
#             converter.resolve_somebody("invalid")  # type: ignore

#     def test_resolve_somebody_list(self, simple_person, another_person):
#         """Test resolving a list of Somebody references."""
#         converter = GwConverter()
#         somebodies: List[Somebody] = [
#             SomebodyDefined(person=simple_person),
#             SomebodyDefined(person=another_person),
#         ]

#         results = converter.resolve_somebody_list(somebodies)

#         assert len(results) == 2
#         assert results[0] == simple_person
#         assert results[1] == another_person


# class TestConvertFamily:
#     """Test family conversion."""

#     def test_convert_simple_family(self, simple_person, another_person):
#         """Test converting a simple family."""
#         converter = GwConverter()

#         # Create a simple family
#         family = Family[int, Person[int, int, str, int], str](
#             index=0,
#             marriage_date=None,
#             marriage_place="",
#             marriage_note="",
#             marriage_src="",
#             witnesses=[],
#             relation_kind=MaritalStatus.MARRIED,
#             divorce_status=NotDivorced(),
#             family_events=[],
#             comment="",
#             origin_file="test.gw",
#             src="",
#             parents=Parents([simple_person, another_person]),
#             children=[],
#         )

#         family_gw = FamilyGwSyntax(
#             couple=Parents([
#                 SomebodyDefined(person=simple_person),
#                 SomebodyDefined(person=another_person),
#             ]),
#             father_sex=Sex.MALE,
#             mother_sex=Sex.FEMALE,
#             witnesses=[],
#             events=[],
#             family=family,
#             descend=[],
#         )

#         result_family, children = converter.convert_family(family_gw)

#         assert result_family.index == 0
#         assert result_family.relation_kind == MaritalStatus.MARRIED
#         assert result_family.origin_file == "test.gw"
#         assert len(children) == 0
#         assert converter.family_index_counter == 1

#     def test_convert_family_with_children(self, simple_person, another_person):
#         """Test converting a family with children."""
#         converter = GwConverter()

#         # Create a child
#         child = replace(simple_person, first_name="Child", surname="Doe")

#         family = Family[int, Person[int, int, str, int], str](
#             index=0,
#             marriage_date=None,
#             marriage_place="",
#             marriage_note="",
#             marriage_src="",
#             witnesses=[],
#             relation_kind=MaritalStatus.MARRIED,
#             divorce_status=NotDivorced(),
#             family_events=[],
#             comment="",
#             origin_file="test.gw",
#             src="",
#             parents=Parents([simple_person, another_person]),
#             children=[child],
#         )

#         family_gw = FamilyGwSyntax(
#             couple=Parents([
#                 SomebodyDefined(person=simple_person),
#                 SomebodyDefined(person=another_person),
#             ]),
#             father_sex=Sex.MALE,
#             mother_sex=Sex.FEMALE,
#             witnesses=[],
#             events=[],
#             family=family,
#             descend=[child],
#         )

#         result_family, children = converter.convert_family(family_gw)

#         assert len(children) == 1
#         assert children[0].first_name == "Child"
#         # Child should be registered
#         assert ("Child", "Doe", 0) in converter.person_by_key

#     def test_convert_family_with_witnesses(
#         self,
#         simple_person,
#         another_person
#     ):
#         """Test converting a family with witnesses."""
#         converter = GwConverter()

#         # Register a witness
#         witness = replace(
#             simple_person,
#             first_name="Witness",
#             surname="Person"
#         )
#         converter.person_by_key[("Witness", "Person", 0)] = witness

#         family = Family[int, Person[int, int, str, int], str](
#             index=0,
#             marriage_date=None,
#             marriage_place="",
#             marriage_note="",
#             marriage_src="",
#             witnesses=[],
#             relation_kind=MaritalStatus.MARRIED,
#             divorce_status=NotDivorced(),
#             family_events=[],
#             comment="",
#             origin_file="test.gw",
#             src="",
#             parents=Parents([simple_person, another_person]),
#             children=[],
#         )

#         family_gw = FamilyGwSyntax(
#             couple=Parents([
#                 SomebodyDefined(person=simple_person),
#                 SomebodyDefined(person=another_person),
#             ]),
#             father_sex=Sex.MALE,
#             mother_sex=Sex.FEMALE,
#             witnesses=[
#                 (SomebodyUndefined(
#                     key=Key("Witness", "Person", 0)
#                 ), Sex.MALE)
#             ],
#             events=[],
#             family=family,
#             descend=[],
#         )

#         result_family, children = converter.convert_family(family_gw)

#         assert len(result_family.witnesses) == 1
#         assert result_family.witnesses[0].first_name == "Witness"


# class TestConvertNotes:
#     """Test notes conversion."""

#     def test_convert_notes(self):
#         """Test converting notes."""
#         converter = GwConverter()
#         key = Key(pk_first_name="John", pk_surname="Doe", pk_occ=0)
#         notes_gw = NotesGwSyntax(key=key, content="These are my notes")

#         converter.convert_notes(notes_gw)

#         assert ("John", "Doe", 0) in converter.notes
#         assert converter.notes[("John", "Doe", 0)] == "These are my notes"

#     def test_convert_multiple_notes(self):
#         """Test converting notes for multiple persons."""
#         converter = GwConverter()

#         notes1 = NotesGwSyntax(
#             key=Key("John", "Doe", 0),
#             content="John's notes"
#         )
#         notes2 = NotesGwSyntax(
#             key=Key("Jane", "Smith", 0),
#             content="Jane's notes"
#         )

#         converter.convert_notes(notes1)
#         converter.convert_notes(notes2)

#         assert len(converter.notes) == 2
#         assert converter.notes[("John", "Doe", 0)] == "John's notes"
#         assert converter.notes[("Jane", "Smith", 0)] == "Jane's notes"


# class TestConvertRelations:
#     """Test relations conversion."""

#     def test_convert_relations(self, simple_person, another_person):
#         """Test converting relations."""
#         converter = GwConverter()

#         # Register persons
#         converter.person_by_key[("John", "Doe", 0)] = simple_person
#         converter.person_by_key[("Father", "Person", 0)] = another_person

#         relation = Relation[Somebody, str](
#             type=RelationToParentType.ADOPTION,
#             father=SomebodyUndefined(Key("Father", "Person", 0)),
#             mother=None,
#             sources="adoption records",
#         )

#         relations_gw = RelationsGwSyntax(
#             person=SomebodyDefined(person=simple_person),
#             sex=Sex.MALE,
#             relations=[relation],
#         )

#         converter.convert_relations(relations_gw)

#         assert ("John", "Doe", 0) in converter.relations
#         relations_list = converter.relations[("John", "Doe", 0)]
#         assert len(relations_list) == 1
#         assert relations_list[0].type == RelationToParentType.ADOPTION
#         assert relations_list[0].father == another_person
#         assert relations_list[0].mother is None

#     def test_convert_relations_with_both_parents(self, simple_person):
#         """Test converting relations with both parents."""
#         converter = GwConverter()

#         father = replace(simple_person, first_name="Dad", surname="Smith")
#         mother = replace(simple_person, first_name="Mom", surname="Jones")

#         converter.person_by_key[("John", "Doe", 0)] = simple_person
#         converter.person_by_key[("Dad", "Smith", 0)] = father
#         converter.person_by_key[("Mom", "Jones", 0)] = mother

#         relation = Relation[Somebody, str](
#             type=RelationToParentType.GODPARENT,
#             father=SomebodyUndefined(Key("Dad", "Smith", 0)),
#             mother=SomebodyUndefined(Key("Mom", "Jones", 0)),
#             sources="church records",
#         )

#         relations_gw = RelationsGwSyntax(
#             person=SomebodyDefined(person=simple_person),
#             sex=Sex.MALE,
#             relations=[relation],
#         )

#         converter.convert_relations(relations_gw)

#         relations_list = converter.relations[("John", "Doe", 0)]
#         assert relations_list[0].father is not None
#         assert relations_list[0].father.first_name == "Dad"
#         assert relations_list[0].mother is not None
#         assert relations_list[0].mother.first_name == "Mom"


# class TestConvertPersonalEvents:
#     """Test personal events conversion."""

#     def test_convert_personal_events(self, simple_person):
#         """Test converting personal events."""
#         converter = GwConverter()
#         converter.person_by_key[("John", "Doe", 0)] = simple_person

#         event = PersonalEvent[Somebody, str](
#             name=PersGraduate(),
#             date=None,
#             place="",
#             reason="",
#             note="",
#             src="",
#             witnesses=[],
#         )

#         events_gw = PersonalEventsGwSyntax(
#             person=SomebodyDefined(person=simple_person),
#             sex=Sex.MALE,
#             events=[event],
#         )

#         converter.convert_personal_events(events_gw)

#         assert ("John", "Doe", 0) in converter.personal_events
#         events_list = converter.personal_events[("John", "Doe", 0)]
#         assert len(events_list) == 1
#         assert isinstance(events_list[0].name, PersGraduate)


# class TestConvert:
#     """Test the main convert method."""

#     def test_convert_family_syntax(self, simple_person, another_person):
#         """Test converting FamilyGwSyntax."""
#         converter = GwConverter()

#         family = Family[int, Person[int, int, str, int], str](
#             index=0,
#             marriage_date=None,
#             marriage_place="",
#             marriage_note="",
#             marriage_src="",
#             witnesses=[],
#             relation_kind=MaritalStatus.MARRIED,
#             divorce_status=NotDivorced(),
#             family_events=[],
#             comment="",
#             origin_file="test.gw",
#             src="",
#             parents=Parents([simple_person, another_person]),
#             children=[],
#         )

#         family_gw = FamilyGwSyntax(
#             couple=Parents([
#                 SomebodyDefined(person=simple_person),
#                 SomebodyDefined(person=another_person),
#             ]),
#             father_sex=Sex.MALE,
#             mother_sex=Sex.FEMALE,
#             witnesses=[],
#             events=[],
#             family=family,
#             descend=[],
#         )

#         converter.convert(family_gw)

#         assert len(converter.families) == 1

#     def test_convert_notes_syntax(self):
#         """Test converting NotesGwSyntax."""
#         converter = GwConverter()
#         notes_gw = NotesGwSyntax(
#             key=Key("John", "Doe", 0),
#             content="Notes"
#         )

#         converter.convert(notes_gw)

#         assert len(converter.notes) == 1

#     def test_convert_unknown_syntax(self):
#         """Test converting unknown syntax type."""
#         converter = GwConverter()

#         with pytest.raises(TypeError, match="Unknown GwSyntax type"):
#             converter.convert("invalid")  # type: ignore


# class TestConvertAll:
#     """Test converting multiple blocks."""

#     def test_convert_all_blocks(self, simple_person):
#         """Test converting multiple GwSyntax blocks."""
#         converter = GwConverter()

#         family = Family[int, Person[int, int, str, int], str](
#             index=0,
#             marriage_date=None,
#             marriage_place="",
#             marriage_note="",
#             marriage_src="",
#             witnesses=[],
#             relation_kind=MaritalStatus.MARRIED,
#             divorce_status=NotDivorced(),
#             family_events=[],
#             comment="",
#             origin_file="test.gw",
#             src="",
#             parents=Parents([simple_person]),
#             children=[],
#         )

#         blocks = [
#             FamilyGwSyntax(
#                 couple=Parents([SomebodyDefined(person=simple_person)]),
#                 father_sex=Sex.MALE,
#                 mother_sex=Sex.FEMALE,
#                 witnesses=[],
#                 events=[],
#                 family=family,
#                 descend=[],
#             ),
#             NotesGwSyntax(
#                 key=Key("John", "Doe", 0),
#                 content="Some notes"
#             ),
#         ]

#         converter.convert_all(blocks)

#         assert len(converter.families) == 1
#         assert len(converter.notes) == 1


# class TestGetMethods:
#     """Test getter methods."""

#     def test_get_all_persons(self, simple_person, another_person):
#         """Test getting all registered persons."""
#         converter = GwConverter()
#         converter.person_by_key[("John", "Doe", 0)] = simple_person
#         converter.person_by_key[("Jane", "Smith", 0)] = another_person

#         persons = converter.get_all_persons()

#         assert len(persons) == 2
#         assert simple_person in persons
#         assert another_person in persons

#     def test_get_all_families(self, simple_person, another_person):
#         """Test getting all registered families."""
#         converter = GwConverter()

#         family = Family[int, Person[int, int, str, int], str](
#             index=0,
#             marriage_date=None,
#             marriage_place="",
#             marriage_note="",
#             marriage_src="",
#             witnesses=[],
#             relation_kind=MaritalStatus.MARRIED,
#             divorce_status=NotDivorced(),
#             family_events=[],
#             comment="",
#             origin_file="test.gw",
#             src="",
#             parents=Parents([simple_person, another_person]),
#             children=[],
#         )

#         family_gw = FamilyGwSyntax(
#             couple=Parents([
#                 SomebodyDefined(person=simple_person),
#                 SomebodyDefined(person=another_person),
#             ]),
#             father_sex=Sex.MALE,
#             mother_sex=Sex.FEMALE,
#             witnesses=[],
#             events=[],
#             family=family,
#             descend=[],
#         )

#         converter.convert_family(family_gw)

#         families = converter.get_all_families()

#         assert len(families) == 1
#         assert families[0].index == 0

#     def test_get_person_by_key_found(self, simple_person):
#         """Test looking up a person by key when found."""
#         converter = GwConverter()
#         converter.person_by_key[("John", "Doe", 0)] = simple_person

#         result = converter.get_person_by_key("John", "Doe", 0)

#         assert result == simple_person

#     def test_get_person_by_key_not_found(self):
#         """Test looking up a person by key when not found."""
#         converter = GwConverter()

#         result = converter.get_person_by_key("Unknown", "Person", 0)

#         assert result is None


# class TestEnrichPerson:
#     """Test person enrichment with additional data."""

#     def test_enrich_person_with_notes(self, simple_person):
#         """Test enriching person with notes."""
#         converter = GwConverter()
#         converter.person_by_key[("John", "Doe", 0)] = simple_person
#         converter.notes[("John", "Doe", 0)] = "Enriched notes"

#         enriched = converter.enrich_person_with_additional_data(simple_person)

#         assert enriched.notes == "Enriched notes"
#         assert enriched.first_name == "John"

#     def test_enrich_person_with_relations(
#         self,
#         simple_person,
#         another_person: Person[int, int, str, int]
#     ):
#         """Test enriching person with relations."""
#         converter = GwConverter()

#         relation = Relation(
#             type=RelationToParentType.ADOPTION,
#             father=another_person,
#             mother=None,
#             sources="records",
#         )

#         converter.person_by_key[("John", "Doe", 0)] = simple_person
#         converter.relations[("John", "Doe", 0)] = [relation]

#         enriched = converter.enrich_person_with_additional_data(simple_person)

#         assert len(enriched.non_native_parents_relation) == 1
#         assert enriched.non_native_parents_relation[0].type == \
#             RelationToParentType.ADOPTION

#     def test_enrich_person_without_additional_data(self, simple_person):
#         """Test enriching person when no additional data exists."""
#         converter = GwConverter()
#         converter.person_by_key[("John", "Doe", 0)] = simple_person

#         enriched = converter.enrich_person_with_additional_data(simple_person)

#         # Should return person with original data
#         assert enriched.notes == simple_person.notes
#         assert enriched.non_native_parents_relation == \
#             simple_person.non_native_parents_relation

#     def test_get_enriched_persons(self, simple_person, another_person):
#         """Test getting all enriched persons."""
#         converter = GwConverter()
#         converter.person_by_key[("John", "Doe", 0)] = simple_person
#         converter.person_by_key[("Jane", "Smith", 0)] = another_person
#         converter.notes[("John", "Doe", 0)] = "John's notes"
#         converter.notes[("Jane", "Smith", 0)] = "Jane's notes"

#         enriched_persons = converter.get_enriched_persons()

#         assert len(enriched_persons) == 2
#         # Find John and Jane in the results
#         john = [p for p in enriched_persons if p.first_name == "John"][0]
#         jane = [p for p in enriched_persons if p.first_name == "Jane"][0]
#         assert john.notes == "John's notes"
#         assert jane.notes == "Jane's notes"


# class TestConvertGwFile:
#     """Test the convenience function."""

#     def test_convert_gw_file_empty(self):
#         """Test converting an empty file."""
#         persons, families = convert_gw_file([])

#         assert len(persons) == 0
#         assert len(families) == 0

#     def test_convert_gw_file_with_data(self, simple_person):
#         """Test converting a file with data."""
#         family = Family[int, Person[int, int, str, int], str](
#             index=0,
#             marriage_date=None,
#             marriage_place="",
#             marriage_note="",
#             marriage_src="",
#             witnesses=[],
#             relation_kind=MaritalStatus.MARRIED,
#             divorce_status=NotDivorced(),
#             family_events=[],
#             comment="",
#             origin_file="test.gw",
#             src="",
#             parents=Parents([simple_person]),
#             children=[],
#         )

#         blocks = [
#             FamilyGwSyntax(
#                 couple=Parents([SomebodyDefined(person=simple_person)]),
#                 father_sex=Sex.MALE,
#                 mother_sex=Sex.FEMALE,
#                 witnesses=[],
#                 events=[],
#                 family=family,
#                 descend=[],
#             ),
#             NotesGwSyntax(
#                 key=Key("John", "Doe", 0),
#                 content="Test notes"
#             ),
#         ]

#         persons, families = convert_gw_file(blocks)

#         # Should have 0 persons from descend list (empty in this case)
#         # Notes are merged but person isn't in descend
#         assert len(families) == 1
