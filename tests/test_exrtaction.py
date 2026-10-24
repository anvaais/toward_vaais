import pytest
from app.services.model_extraction import validate_model_output, extract_from_inquiry


def test_valid_json_passes():
    raw_output = """
    {
        "leads": [
            {
                "travelers": 4,
                "location": "Hunza",
                "price": 50000.0,
                "source_text": "budget is 50000"
            }
        ],
        "errors": []
    }
    """
    result = validate_model_output(raw_output, inquiry_text="We are 4 people visiting Hunza, budget is 50000")
    assert len(result.leads) == 1
    assert result.leads[0].price == 50000.0
    assert result.leads[0].source_text == "budget is 50000"


def test_imagined_price_without_source_raises_value_error():
    raw_output = """
    {
        "leads": [
            {
                "travelers": 4,
                "location": "Hunza",
                "price": 50000.0
            }
        ],
        "errors": []
    }
    """
    with pytest.raises(ValueError, match="Imagined price rejected"):
        validate_model_output(raw_output)


def test_invalid_json_raises_value_error():
    malformed_json = '{"leads": [{"travelers": 4, "location": "Hunza"'  # Missing closing brackets
    with pytest.raises(ValueError, match="Invalid model output"):
        validate_model_output(malformed_json)


def test_extra_field_raises_value_error():
    extra_field_json = """
    {
        "leads": [
            {
                "travelers": 4,
                "unexpected_extra_field": "hacked"
            }
        ],
        "errors": []
    }
    """
    with pytest.raises(ValueError, match="Invalid model output"):
        validate_model_output(extra_field_json)


def test_vague_date_and_contradictory_message():
    # Vague date test
    res_vague = extract_from_inquiry("We want to visit Skardu maybe next month", mode="mock")
    assert res_vague.leads[0].dates is None
    assert res_vague.leads[0].needs_review is True

    # Contradictory message test
    res_contra = extract_from_inquiry("We are 6 people, actually no make it 3 people", mode="mock")
    assert res_contra.leads[0].travelers is None
    assert res_contra.leads[0].needs_review is True