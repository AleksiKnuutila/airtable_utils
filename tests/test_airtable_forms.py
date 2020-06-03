import pytest
import hypothesis

import airtable_forms

def test_airtable_forms_version():
    """Test that the package exists and has a version"""
    assert airtable_forms.__version__

