"""
Implementation of the MOD_IND route - Individual modification page.
"""
from flask import render_template, request, g
from datetime import date


def get_mock_individual_data(person_id):
    """
    Generate mock data for an individual based on their ID.
    In production, this would query the database.
    """
    # Mock person data
    person = {
        'id': person_id,
        'index': person_id,  # For compatibility with template
        'first_name': 'az',
        'surname': 'bg',
        'number': '0',
        'sex': 'M',  # M, F, or U (unspecified)
        'public_name': 'az bg',
        'image': 'portrait_8.jpg',
        'access': 'public',  # public, private, if_titles
        'nickname': 'The Great',
    'sobriquets': ['The Great'],
    'alt_first_names': ['Jean-Baptiste'],
        'alias': ['az the Great', 'bg Junior'],
        'surnames': ['von bg', 'de bg'],
        'occupations': ['Prince', 'Warrior'],
    'source': 'Compiled from multiple biographies',
        # alive, dead, killed, murdered, executed, disappeared, dont_know, obviously_dead
        'death_status': 'dead',

        # Birth information
        'birth': {
            'date': {
                'day': '15',
                'month': '3',
                'year': '1950',
                'calendar': 'gregorian',  # gregorian, julian, french_republican, hebrew
            },
            'place': 'Paris, France',
            'source': 'Parish records',
            'note': 'Born at home',
            'witnesses': [
                {
                    'index': 101,
                    'kind': 'info',
                    'first_name': 'Pierre',
                    'surname': 'Martin',
                    'occ': '0',
                    'sex': 'M',
                    'occupation': 'Doctor',
                    'public': True,
                },
                {
                    'index': 102,
                    'kind': 'atte',
                    'first_name': 'Marie',
                    'surname': 'Dubois',
                    'occ': '0',
                    'sex': 'F',
                    'occupation': 'Midwife',
                    'public': True,
                },
            ],
        },

        # Baptism information
        'baptism': {
            'date': {
                'day': '20',
                'month': '3',
                'year': '1950',
                'calendar': 'gregorian',
            },
            'place': 'Notre-Dame Cathedral, Paris',
            'source': 'Church records',
            'note': 'Baptized by Father Leclerc',
            'witnesses': [
                {
                    'index': 103,
                    'kind': 'godp',
                    'first_name': 'Jean',
                    'surname': 'Durand',
                    'occ': '0',
                    'sex': 'M',
                    'occupation': 'Merchant',
                    'public': True,
                },
                {
                    'index': 104,
                    'kind': 'godp',
                    'first_name': 'Sophie',
                    'surname': 'Moreau',
                    'occ': '0',
                    'sex': 'F',
                    'occupation': 'Teacher',
                    'public': True,
                },
            ],
        },

        # Death information (only if not alive)
        'death': {
            'date': {
                'day': '10',
                'month': '12',
                'year': '2020',
                'calendar': 'gregorian',
            },
            'place': 'Paris, France',
            'source': 'Death certificate',
            'note': 'Died peacefully',
            'age': '',
            'witnesses': [
                {
                    'index': 105,
                    'kind': 'info',
                    'first_name': 'Robert',
                    'surname': 'Lefebvre',
                    'occ': '0',
                    'sex': 'M',
                    'occupation': 'Notary',
                    'public': True,
                },
            ],
        },

        # Burial information
        'burial': {
            'date': {
                'day': '15',
                'month': '12',
                'year': '2020',
                'calendar': 'gregorian',
            },
            'place': 'Père Lachaise Cemetery, Paris',
            'source': 'Burial records',
            'note': 'Family burial plot',
            'type': 'burial',
            'witnesses': [
                {
                    'index': 106,
                    'kind': 'offi',
                    'first_name': 'Claude',
                    'surname': 'Bernard',
                    'occ': '0',
                    'sex': 'M',
                    'occupation': 'Priest',
                    'public': True,
                },
                {
                    'index': 107,
                    'kind': 'atte',
                    'first_name': 'Anne',
                    'surname': 'Petit',
                    'occ': '0',
                    'sex': 'F',
                    'occupation': '',
                    'public': True,
                },
            ],
        },

        # Events
        'events': [
            {
                'type': 'residence',
                'date': {'day': '1', 'month': '1', 'year': '1960', 'calendar': 'gregorian'},
                'place': 'London, UK',
                'source': 'Census records',
                'note': 'Living at 10 Downing Street',
                'witnesses': [
                    {
                        'index': 108,
                        'kind': 'atte',
                        'first_name': 'Thomas',
                        'surname': 'Wilson',
                        'occ': '0',
                        'sex': 'M',
                        'occupation': 'Census taker',
                        'public': True,
                    },
                ],
            },
            {
                'type': 'military_service',
                'date': {'day': '15', 'month': '6', 'year': '1968', 'calendar': 'gregorian'},
                'place': 'French Army',
                'source': 'Military archives',
                'note': 'Served in the infantry',
                'witnesses': [
                    {
                        'index': 109,
                        'kind': 'offi',
                        'first_name': 'Colonel',
                        'surname': 'Dupont',
                        'occ': '0',
                        'sex': 'M',
                        'occupation': 'Military Officer',
                        'public': True,
                    },
                    {
                        'index': 110,
                        'kind': 'atte',
                        'first_name': 'Sergeant',
                        'surname': 'Laurent',
                        'occ': '0',
                        'sex': 'M',
                        'occupation': 'Sergeant',
                        'public': True,
                    },
                ],
            },
        ],

        # Relations
        'relations': [
            {
                'type': 'Adoption',
                'father': {
                    'first_name': 'John',
                    'surname': 'Doe',
                    'occ': '0',
                    'occupation': 'Merchant',
                    'action': 'link',
                    'dead': False,
                    'public': True,
                },
                'mother': {
                    'first_name': 'Jane',
                    'surname': 'Doe',
                    'occ': '0',
                    'occupation': 'Teacher',
                    'action': 'link',
                    'dead': False,
                    'public': True,
                },
            },
            {
                'type': 'GodParent',
                'father': {
                    'first_name': 'Paul',
                    'surname': 'Smith',
                    'occ': '1',
                    'occupation': 'Priest',
                    'action': 'create',
                    'dead': True,
                    'public': True,
                },
                'mother': {
                    'first_name': 'Mary',
                    'surname': 'Smith',
                    'occ': '0',
                    'occupation': '',
                    'action': 'create',
                    'dead': False,
                    'public': True,
                },
            },
        ],

        # Parents
        'parents': {
            'father': {
                'id': 12,
                'name': 'Father bg',
                'first_name': 'Father',
                'surname': 'bg',
            },
            'mother': {
                'id': 13,
                'name': 'Mother bg',
                'first_name': 'Mother',
                'surname': 'bg',
            },
        },

        # Families (unions)
        'families': [
            {
                'id': 4,
                'spouse': {
                    'id': 9,
                    'name': 'Spouse Name',
                    'first_name': 'Spouse',
                    'surname': 'Name',
                },
                'marriage': {
                    'date': {'day': '10', 'month': '6', 'year': '1975', 'calendar': 'gregorian'},
                    'place': 'Paris, France',
                    'source': 'Marriage certificate',
                },
                'divorce': {
                    'date': {'day': '', 'month': '', 'year': '', 'calendar': 'gregorian'},
                    'source': '',
                },
                'children': [
                    {'id': 14, 'name': 'Child One bg', 'birth_year': '1976'},
                    {'id': 15, 'name': 'Child Two bg', 'birth_year': '1978'},
                    {'id': 16, 'name': 'Child Three bg', 'birth_year': '1980'},
                ],
            },
        ],

        # Titles
        'titles': [
            {
                'title': 'Duke',
                'place': 'Normandy',
                'date_start': {'day': '1', 'month': '1', 'year': '1980', 'calendar': 'gregorian'},
                'date_end': {'day': '31', 'month': '12', 'year': '1990', 'calendar': 'gregorian'},
                'nth': '3rd',
            },
            {
                'title': 'Count',
                'place': 'Provence',
                'date_start': {'day': '1', 'month': '1', 'year': '1970', 'calendar': 'gregorian'},
                'date_end': {'day': '', 'month': '', 'year': '', 'calendar': 'gregorian'},
                'nth': '1st',
            },
        ],

        # Notes
        'notes': 'This is a mock person for testing purposes.\n\nImportant historical figure.\nKnown for their contributions to society.',
    }

    return person


def implem_route_MOD_IND(base, id, lang='en'):
    """
    Implementation of the MOD_IND route - Individual modification page.

    Args:
        base: The database base name
        id: The person ID to modify
        lang: Language code (default: 'en')

    Returns:
        Rendered template with person data
    """
    g.locale = lang
    # Get mock data for the person
    person = get_mock_individual_data(id)

    # Prepare data for the template
    context = {
        'base': base,
        'db_name': base,  # Template uses db_name
        'id': id,
        'lang': lang,
        'person': person,
        'digest': '',  # TODO: Calculate actual digest for data integrity
        'wizard_message': None,  # Optional message from wizard
        'max_aliases': 10,  # Maximum number of alias fields to show

        # Calendar types for dropdown
        'calendar_types': [
            {'value': 'gregorian', 'label': 'Gregorian'},
            {'value': 'julian', 'label': 'Julian'},
            {'value': 'french_republican', 'label': 'French Republican'},
            {'value': 'hebrew', 'label': 'Hebrew'},
        ],

        # Months for each calendar (will be populated by JavaScript)
        'gregorian_months': [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ],

        'french_republican_months': [
            'Vendémiaire', 'Brumaire', 'Frimaire', 'Nivôse', 'Pluviôse', 'Ventôse',
            'Germinal', 'Floréal', 'Prairial', 'Messidor', 'Thermidor', 'Fructidor',
            'Complémentaire'
        ],

        'hebrew_months': [
            'Tichri', 'Marhechvan', 'Kislev', 'Tevet', 'Chevat', 'Adar 1',
            'Adar 2', 'Nissan', 'Iyar', 'Sivan', 'Tamouz', 'Av', 'Eloul'
        ],

        # Sex options
        'sex_options': [
            {'value': 'M', 'label': 'Male'},
            {'value': 'F', 'label': 'Female'},
            {'value': 'U', 'label': 'Unspecified/Unknown'},
        ],

        # Access levels
        'access_levels': [
            {'value': 'public', 'label': 'Public'},
            {'value': 'private', 'label': 'Private'},
            {'value': 'if_titles', 'label': 'If titles'},
        ],

        # Death status options
        'death_statuses': [
            {'value': 'alive', 'label': 'Alive'},
            {'value': 'dead', 'label': 'Dead'},
            {'value': 'dont_know', 'label': 'Don\'t know'},
            {'value': 'obviously_dead', 'label': 'Obviously dead'},
            {'value': 'killed', 'label': 'Killed'},
            {'value': 'murdered', 'label': 'Murdered'},
            {'value': 'executed', 'label': 'Executed'},
            {'value': 'disappeared', 'label': 'Disappeared'},
        ],

        # Event types
        'event_types': [
            'birth', 'baptism', 'death', 'burial', 'residence', 'occupation',
            'military_service', 'census', 'graduation', 'award', 'other'
        ],

        # Relation types
        'relation_types': [
            {'value': 'adoptive_parents', 'label': 'Adoptive parents'},
            {'value': 'recognized_parents', 'label': 'Parents who recognized'},
            {'value': 'possible_parents', 'label': 'Possible parents'},
            {'value': 'godparents', 'label': 'Godparents'},
            {'value': 'foster_parents', 'label': 'Foster parents'},
        ],

        # Languages for footer selector
        'languages': [
            {'code': 'en', 'name': 'English'},
            {'code': 'fr', 'name': 'Français'},
            {'code': 'de', 'name': 'Deutsch'},
            {'code': 'es', 'name': 'Español'},
            {'code': 'it', 'name': 'Italiano'},
            {'code': 'pt', 'name': 'Português'},
            {'code': 'nl', 'name': 'Nederlands'},
            {'code': 'sv', 'name': 'Svenska'},
            {'code': 'da', 'name': 'Dansk'},
            {'code': 'no', 'name': 'Norsk'},
            {'code': 'fi', 'name': 'Suomi'},
            {'code': 'pl', 'name': 'Polski'},
            {'code': 'cs', 'name': 'Čeština'},
            {'code': 'ru', 'name': 'Русский'},
            {'code': 'zh', 'name': '中文'},
        ],

        # Current year for form validation
        'current_year': date.today().year,
    }

    # Handle form submission
    if request.method == 'POST':
        # TODO: Process form data and update database
        # For now, just return to the same page
        pass

    return render_template('gwd/mod_individual.html', **context)
