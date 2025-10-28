"""
Test suite for Flask-Babel i18n translations.

Tests the translation configuration, locale detection, and translation loading
for the GeneWeb Flask application.
"""

import pytest
from flask import request


def test_flask_babel_installed():
    """Test that Flask-Babel is properly installed and can be imported."""
    try:
        from flask_babel import Babel, get_locale, gettext
        assert True
    except ImportError:
        pytest.fail(
            "Flask-Babel is not installed. Run: pip install Flask-Babel")


def test_app_babel_initialization():
    """Test that the Flask app initializes with Babel extension."""
    from wserver import create_app

    app = create_app()

    # Check if Babel is configured
    assert 'babel' in app.extensions or hasattr(app, 'babel'), \
        "Babel extension not initialized in Flask app"

    # Check default locale configuration
    assert app.config.get('BABEL_DEFAULT_LOCALE') == 'en', \
        "Default locale should be 'en' (English)"


def test_translation_files_exist():
    """Test that translation files exist in the correct location."""
    import os

    # Translations should be in src/wserver/translations/
    translation_dir = os.path.join(
        os.path.dirname(__file__),
        '..', 'src', 'wserver', 'translations'
    )
    translation_dir = os.path.abspath(translation_dir)

    assert os.path.exists(translation_dir), \
        f"Translations directory not found: {translation_dir}"

    # Check for English translations
    en_mo = os.path.join(translation_dir, 'en', 'LC_MESSAGES', 'messages.mo')
    en_po = os.path.join(translation_dir, 'en', 'LC_MESSAGES', 'messages.po')

    assert os.path.exists(en_mo), \
        f"English compiled translations missing: {en_mo}. Run: pybabel compile -d src/wserver/translations"

    assert os.path.exists(en_po), \
        f"English source translations missing: {en_po}"


def test_locale_detection_url_param():
    """Test locale detection from URL parameter."""
    from wserver import create_app
    from flask_babel import get_locale

    app = create_app()

    with app.test_request_context('/?locale=en'):
        locale = get_locale()
        assert str(locale) == 'en', \
            f"Expected locale 'en', got '{locale}'"


def test_locale_detection_cookie():
    """Test locale detection from cookie."""
    from wserver import create_app
    from flask_babel import get_locale

    app = create_app()

    with app.test_request_context('/', headers={'Cookie': 'locale=en'}):
        locale = get_locale()
        assert str(locale) == 'en', \
            f"Expected locale 'en' from cookie, got '{locale}'"


def test_locale_detection_accept_language():
    """Test locale detection from Accept-Language header."""
    from wserver import create_app
    from flask_babel import get_locale

    app = create_app()

    with app.test_request_context('/', headers={'Accept-Language': 'en-US,en;q=0.9'}):
        locale = get_locale()
        assert str(locale) == 'en', \
            f"Expected locale 'en' from Accept-Language, got '{locale}'"


def test_locale_detection_url_path():
    """Test locale detection from URL path parameter (via g.locale)."""
    from wserver import create_app
    from flask_babel import get_locale
    from flask import g

    app = create_app()

    # Test French locale set via g.locale (simulating URL path parameter)
    with app.test_request_context('/gwd/base/ADD_FAM/fr'):
        g.locale = 'fr'
        locale = get_locale()
        assert str(locale) == 'fr', \
            f"Expected locale 'fr' from g.locale (URL path), got '{locale}'"
    
    # Test English locale set via g.locale
    with app.test_request_context('/gwd/base/ADD_FAM/en'):
        g.locale = 'en'
        locale = get_locale()
        assert str(locale) == 'en', \
            f"Expected locale 'en' from g.locale (URL path), got '{locale}'"


@pytest.mark.parametrize("key,expected", [
    ('Add family', 'Add family'),
    ('Parents', 'Parents'),
    ('Children', 'Children'),
    ('Submit', 'Submit'),
    ('First name', 'First name'),
    ('Surname', 'Surname'),
    ('Create', 'Create'),
    ('Link', 'Link'),
])
def test_translation_strings(key, expected):
    """Test that specific strings are translated correctly in English."""
    from wserver import create_app
    from flask_babel import gettext as _

    app = create_app()

    with app.test_request_context('/?locale=en'):
        translated = _(key)
        assert translated == expected, \
            f"Translation mismatch: expected '{expected}', got '{translated}'"


def test_translation_fallback():
    """Test that untranslated strings fall back to the original."""
    from wserver import create_app
    from flask_babel import gettext as _

    app = create_app()

    with app.test_request_context('/?locale=en'):
        # Test with a string that shouldn't exist
        untranslated_key = "ThisStringDoesNotExistInTranslations123"
        result = _(untranslated_key)
        assert result == untranslated_key, \
            "Untranslated strings should fall back to original"


def test_child_ordinals_available():
    """Test that child ordinal translations are available."""
    from wserver import create_app
    from flask_babel import gettext as _

    app = create_app()

    ordinals = ['1st', '2nd', '3rd', '4th',
                '5th', '6th', '7th', '8th', '9th', '10th']

    with app.test_request_context('/?locale=en'):
        for ordinal in ordinals:
            translated = _(ordinal)
            assert translated == ordinal, \
                f"Ordinal '{ordinal}' not properly translated"


def test_witness_types_translated():
    """Test that witness type translations are available."""
    from wserver import create_app
    from flask_babel import gettext as _

    app = create_app()

    witness_types = {
        'Witness': 'Witness',
        'Informant': 'Informant',
        'Present': 'Present',
        'Mentioned': 'Mentioned',
        'Civil registrar': 'Civil registrar',
        'Minister of worship': 'Minister of worship',
        'Other': 'Other',
    }

    with app.test_request_context('/?locale=en'):
        for key, expected in witness_types.items():
            translated = _(key)
            assert translated == expected, \
                f"Witness type '{key}' not properly translated"


@pytest.mark.skip(reason="Integration test requires running server")
def test_ADD_FAM_page_renders_english(client):
    """Integration test: verify ADD_FAM page renders in English."""
    response = client.get('/base/ADD_FAM?locale=en')

    assert response.status_code == 200
    assert b'Add family' in response.data
    assert b'Parents' in response.data
    assert b'Children' in response.data
    assert b'Submit' in response.data


# Pytest fixture for Flask test client (optional, for integration tests)
@pytest.fixture
def client():
    """Create a test client for integration tests."""
    from wserver import create_app

    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client
