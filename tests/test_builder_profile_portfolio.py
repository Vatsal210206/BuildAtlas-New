import db

from hackathon1 import _builder_profile_payload


def test_builder_past_project_database_api_is_available():
    assert callable(db.list_builder_past_projects)
    assert callable(db.create_builder_past_project)
    assert callable(db.update_builder_past_project)
    assert callable(db.delete_builder_past_project)


def test_builder_profile_payload_normalizes_business_details():
    payload = _builder_profile_payload({
        "business_name": "  Apex Buildworks  ",
        "contact_name": "  Arjun Mehta  ",
        "phone": " 9876543210 ",
        "gst_number": " 27abcde1234f1z5 ",
        "address": " 12 Sector 18 ",
        "city": " noida ",
        "state": " uttar pradesh ",
        "portfolio_summary": " Premium villas and commercial construction ",
    })

    assert payload["business_name"] == "Apex Buildworks"
    assert payload["contact_name"] == "Arjun Mehta"
    assert payload["phone"] == "9876543210"
    assert payload["gst_number"] == "27ABCDE1234F1Z5"
    assert payload["address"] == "12 Sector 18"
    assert payload["city"] == "Noida"
    assert payload["state"] == "Uttar Pradesh"
    assert payload["portfolio_summary"] == "Premium villas and commercial construction"
