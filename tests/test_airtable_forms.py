import pytest
import hypothesis

import airtable_utils


def test_airtable_utils_version():
    """Test that the package exists and has a version"""
    assert airtable_forms.__version__
