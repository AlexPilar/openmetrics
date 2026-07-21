import pytest
import requests

from connectors.bcb.ingestion_sgs import (
    build_url,
    fetch_data,
    save_json,
)


def test_build_url():
    # Build a URL for a valid SGS series
    url = build_url(11)

    # Check if the series ID is included in the URL
    assert "bcdata.sgs.11" in url

    # Check if the response format is JSON
    assert "formato=json" in url


def test_fetch_data_success():
    # Use a valid URL to test the expected behavior
    url = build_url(11)

    # Execute the request
    result = fetch_data("selic", url)

    # The function should return data
    assert result is not None

    # The API should return a list of records
    assert isinstance(result, list)

    # The list should contain at least one record
    assert len(result) > 0


def test_fetch_data_invalid_url():
    # The function should raise an exception for an invalid request
    with pytest.raises(requests.exceptions.RequestException):
        fetch_data(
            "test",
            "https://url-inexistente.com"
        )


def test_save_json_empty():
    # An empty dataset should not be saved
    result = save_json([], "test")

    assert result is False


def test_save_json_success():
    # Create a minimal dataset that mimics the API response
    data = [
        {
            "data": "01/01/2026",
            "valor": "13.25"
        }
    ]

    # Save the JSON file
    result = save_json(data, "test")

    # The function should report a successful save
    assert result is True
