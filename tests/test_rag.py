from app.retrieval.rag import (
    build_search_query,
    generic_recommendation
)


def test_build_search_query():

    features = {
        "chest_pain": 1,
        "shortness_of_breath": 1
    }

    query = build_search_query(
        features,
        "Critical"
    )

    assert "chest pain" in query
    assert "shortness of breath" in query
    assert "Critical urgency" in query


def test_generic_recommendation_high():

    result = generic_recommendation("High")

    assert result["source"] == "General Medical Guidance"

    assert "immediate medical attention" in result["recommendation"]


def test_generic_recommendation_low():

    result = generic_recommendation("Low")

    assert result["source"] == "General Medical Guidance"

    assert "Monitor your symptoms" in result["recommendation"]