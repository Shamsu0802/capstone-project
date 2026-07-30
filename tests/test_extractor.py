from unittest.mock import MagicMock, patch

from app.extraction.extractor import extract_patient_features


def test_extract_features():

    fake_response = MagicMock()
    fake_response.content = """
    {
        "fever": 1,
        "cough": 1
    }
    """

    with patch("app.extraction.extractor.llm", new=MagicMock()) as mock_llm:

        mock_llm.invoke.return_value = fake_response

        result = extract_patient_features(
            "I have fever and cough."
        )

        assert result["fever"] == 1
        assert result["cough"] == 1