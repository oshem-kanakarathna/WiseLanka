"""Mocked Gemini tests; no API credentials or participant data are used."""

import json

from fastapi.testclient import TestClient

from backend.app.api.main import app
from backend.app.eligibility.engine import assess_academic_gaps
from backend.app.gemini_exploration import service
from backend.app.gemini_exploration.shortlisting import build_candidate_shortlist


client = TestClient(app)

PROFILE = {
    "education": {"A_LEVEL": {"Combined Mathematics": "B", "Physics": "C", "Chemistry": "C"}},
    "career_intention": "PRIVATE_SENTINEL_NAME and private interests",
    "interests": ["PRIVATE_SENTINEL_INTEREST"],
}


def payload(**overrides):
    value = {
        "learner_profile": PROFILE,
        "exploration_domain": "Information Technology",
    }
    value.update(overrides)
    return value


def enable(monkeypatch):
    monkeypatch.setenv("GEMINI_EXPLORATION_ENABLED", "true")


def test_disabled_by_default_and_does_not_call_provider(monkeypatch):
    monkeypatch.delenv("GEMINI_EXPLORATION_ENABLED", raising=False)
    monkeypatch.setattr(service, "_provider_generate", lambda *_: (_ for _ in ()).throw(AssertionError("called")))
    response = client.post("/gemini/pathway-exploration", json=payload())
    assert response.status_code == 503
    assert response.json()["detail"] == "Gemini pathway exploration is disabled."


def test_local_catalogue_and_local_eligibility_are_grounded_and_separate(monkeypatch):
    enable(monkeypatch)
    captured = {}

    def provider(prompt, schema):
        captured["prompt"] = prompt
        captured["schema"] = schema
        return json.dumps({
            "pathways": [
                {"programme_id": "PRG0002", "progression_ids": [], "reason_code": "INTEREST_AREA_MATCH"},
                {"programme_id": "PRG0001", "progression_ids": [], "reason_code": "COMPARISON_OPTION"},
            ],
            "unverified_ideas": ["An emerging robotics pathway"],
        })

    monkeypatch.setattr(service, "_provider_generate", provider)
    response = client.post("/gemini/pathway-exploration", json=payload())
    assert response.status_code == 200, response.text
    result = response.json()
    assert "PRIVATE_SENTINEL_NAME" not in captured["prompt"]
    assert "PRIVATE_SENTINEL_INTEREST" not in captured["prompt"]
    assert '"career_intention":' not in captured["prompt"]
    assert '"education":' not in captured["prompt"]
    assert result["mode"] == "GEMINI_ASSISTED_PATHWAY_EXPLORATION"
    assert [p["academic_assessment"]["status"] for p in result["pathways"]] == sorted(
        [p["academic_assessment"]["status"] for p in result["pathways"]],
        key={"MET": 0, "NOT_ASSESSED": 1, "NOT_MET": 2}.get,
    )
    for pathway in result["pathways"]:
        expected = assess_academic_gaps(
            pathway["programme_id"],
            PROFILE["education"],
            {},
            [],
        )
        assert pathway["academic_assessment"] == expected
        assert all(rule["source_url"].startswith("https://") for rule in pathway["entry_requirements"])
        assert pathway["programme_source"]["url"].startswith("https://")
        if pathway["qualification_source"]:
            assert pathway["qualification_source"]["url"].startswith("https://")
        assert "not admission" in result["notice"].lower()
    assert result["unverified_ideas"][0]["status"] == "UNVERIFIED"


def test_missing_entry_rules_are_not_labelled_fully_verified(monkeypatch):
    enable(monkeypatch)
    monkeypatch.setattr(service, "_provider_generate", lambda *_: json.dumps({
        "pathways": [{"programme_id": "PRG0005", "progression_ids": ["PROG0001"], "reason_code": "DOCUMENTED_PROGRESSION"}],
        "unverified_ideas": [],
    }))
    result = client.post("/gemini/pathway-exploration", json=payload()).json()
    selected = next(item for item in result["pathways"] if item["programme_id"] == "PRG0005")
    assert selected["pathway_evidence_status"] == "PARTIALLY_VERIFIED"
    assert selected["entry_requirement_status"] == "NOT_ASSESSED"
    assert selected["progression"][0]["progression_id"] == "PROG0001"
    assert selected["progression"][0]["guaranteed"] is False


def test_hallucinated_programme_id_is_rejected(monkeypatch):
    enable(monkeypatch)
    monkeypatch.setattr(service, "_provider_generate", lambda *_: json.dumps({
        "pathways": [{"programme_id": "PRG9999", "progression_ids": [], "reason_code": "INTEREST_AREA_MATCH"}],
        "unverified_ideas": [],
    }))
    response = client.post("/gemini/pathway-exploration", json=payload())
    assert response.status_code == 502


def test_unrelated_progression_connection_is_rejected(monkeypatch):
    enable(monkeypatch)
    monkeypatch.setattr(service, "_provider_generate", lambda *_: json.dumps({
        "pathways": [{"programme_id": "PRG0001", "progression_ids": ["PROG0001"], "reason_code": "DOCUMENTED_PROGRESSION"}],
        "unverified_ideas": [],
    }))
    response = client.post("/gemini/pathway-exploration", json=payload())
    assert response.status_code == 502


def test_invalid_json_is_rejected(monkeypatch):
    enable(monkeypatch)
    monkeypatch.setattr(service, "_provider_generate", lambda *_: "{broken")
    response = client.post("/gemini/pathway-exploration", json=payload())
    assert response.status_code == 502


def test_provider_unavailable_returns_safe_error(monkeypatch):
    enable(monkeypatch)

    def unavailable(*_):
        raise service.GeminiUnavailable("Gemini pathway exploration is temporarily unavailable.")

    monkeypatch.setattr(service, "_provider_generate", unavailable)
    response = client.post("/gemini/pathway-exploration", json=payload())
    assert response.status_code == 200
    result = response.json()
    assert result["mode"] == "LOCAL_SHORTLIST_FALLBACK"
    assert "temporarily unavailable" not in result["notice"].casefold()
    assert all(item["selection_source"] == "LOCAL_FALLBACK" for item in result["pathways"])
    assert "PRIVATE_SENTINEL" not in response.text


def test_unknown_comparison_id_and_questionnaire_fields_are_rejected(monkeypatch):
    enable(monkeypatch)
    assert client.post(
        "/gemini/pathway-exploration",
        json=payload(compare_programme_ids=["PRG9999"]),
    ).status_code == 422
    assert client.post(
        "/gemini/pathway-exploration",
        json=payload(questionnaire_answers={"Q1": 5}),
    ).status_code == 422


def test_transport_uses_current_response_format_and_parses_structured_response(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "synthetic-secret")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    captured = {}
    programmes, _ = service.verified_catalogue()
    selected_id = programmes[0]["programme_id"]
    structured_result = {
        "pathways": [{
            "programme_id": selected_id,
            "progression_ids": [],
            "reason_code": "INTEREST_AREA_MATCH",
        }],
        "unverified_ideas": [],
    }

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *_):
            return False

        def read(self, limit):
            captured["read_limit"] = limit
            envelope = {"candidates": [{"content": {"parts": [{
                "text": json.dumps(structured_result),
            }]}}]}
            return json.dumps(envelope).encode("utf-8")

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["key_header"] = request.get_header("X-goog-api-key")
        captured["timeout"] = timeout
        captured["body"] = json.loads(request.data)
        return Response()

    monkeypatch.setattr(service, "urlopen", fake_urlopen)
    selected, _, _ = service.generate_selection(
        "Information Technology", [], programmes, service.verified_catalogue()[1]
    )
    assert selected.pathways[0].programme_id == selected_id
    assert "synthetic-secret" not in captured["url"]
    assert captured["key_header"] == "synthetic-secret"
    assert captured["timeout"] == service.TIMEOUT_SECONDS == 8
    assert captured["read_limit"] == service.MAX_PROVIDER_RESPONSE_BYTES + 1
    assert captured["body"]["generationConfig"]["maxOutputTokens"] == 700
    assert captured["url"].endswith("/models/gemini-3.5-flash-lite:generateContent")
    generation = captured["body"]["generationConfig"]
    assert "responseSchema" not in generation
    assert "responseMimeType" not in generation
    assert generation["responseFormat"]["text"]["mimeType"] == "APPLICATION_JSON"
    schema = generation["responseFormat"]["text"]["schema"]
    assert schema["type"] == "object"
    assert schema["properties"]["pathways"]["items"]["properties"]["programme_id"]["enum"] == [
        item["programme_id"] for item in programmes
    ]


def test_transport_provider_error_is_sanitised(monkeypatch):
    from urllib.error import URLError

    monkeypatch.setenv("GEMINI_API_KEY", "synthetic-secret")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

    def fail(*_args, **_kwargs):
        raise URLError("synthetic-secret provider detail")

    monkeypatch.setattr(service, "urlopen", fail)
    try:
        service._provider_generate("synthetic prompt", {})
    except service.GeminiUnavailable as error:
        assert "synthetic-secret" not in str(error)
        assert "provider detail" not in str(error)
    else:
        raise AssertionError("Provider transport failure should be handled")


def test_missing_model_configuration_fails_closed(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    try:
        service._settings()
    except service.GeminiUnavailable:
        pass
    else:
        raise AssertionError("Missing Gemini configuration should fail closed")


def test_o_level_profile_shortlists_and_returns_m_and_future_it_routes(monkeypatch):
    enable(monkeypatch)
    captured = {}
    profile = {
        "learner_category": "O_LEVEL_LEARNER",
        "education": {
            "O_LEVEL": {
                "Mathematics": "A", "English": "B", "Science": "B",
                "ICT": "A", "Sinhala": "B", "History": "C",
                "Buddhism": "B", "Geography": "C",
                "Health and Physical Education": "B",
            }
        },
        "education_complete": {"O_LEVEL": True},
        "interests": ["computer programming"],
    }

    def provider(prompt, schema):
        captured["prompt"] = prompt
        captured["allowed_ids"] = schema["properties"]["pathways"]["items"]["properties"]["programme_id"]["enum"]
        captured["allowed_edges"] = schema["properties"]["pathways"]["items"]["properties"]["progression_ids"]["items"]["enum"]
        # The model fills all four slots with alternatives and omits the local
        # MET route. The server must retain that route within the output cap.
        return json.dumps({
            "pathways": [
                {"programme_id": "PRG0005", "progression_ids": ["PROG0001"], "reason_code": "DOCUMENTED_PROGRESSION"},
                {"programme_id": "PRG0006", "progression_ids": ["PROG0002"], "reason_code": "DOCUMENTED_PROGRESSION"},
                {"programme_id": "PRG0007", "progression_ids": ["PROG0003"], "reason_code": "DOCUMENTED_PROGRESSION"},
                {"programme_id": "PRG0001", "progression_ids": [], "reason_code": "COMPARISON_OPTION"},
            ],
            "unverified_ideas": [],
        })

    monkeypatch.setattr(service, "_provider_generate", provider)
    response = client.post("/gemini/pathway-exploration", json={
        "learner_profile": profile,
        "exploration_domain": "Information Technology",
    })
    assert response.status_code == 200, response.text
    assert "PRG0004" in captured["allowed_ids"]
    assert {"PRG0005", "PRG0006", "PRG0007"}.issubset(set(captured["allowed_ids"]))
    assert "computer programming" not in captured["prompt"]
    assert '"Mathematics":"A"' not in captured["prompt"]
    assert "O_LEVEL_LEARNER" not in captured["prompt"]

    result = response.json()
    assert len(result["pathways"]) == 4
    assert result["pathways"][0]["programme_id"] == "PRG0004"
    assert {p["programme_id"] for p in result["pathways"][1:]} == {
        "PRG0005", "PRG0006", "PRG0007",
    }
    foundation = next(p for p in result["pathways"] if p["programme_id"] == "PRG0004")
    future = next(p for p in result["pathways"] if p["programme_id"] == "PRG0005")
    assert foundation["academic_assessment"]["status"] == "MET"
    assert foundation["pathway_position"] == "IMMEDIATE_OPTION"
    assert foundation["selection_source"] == "LOCAL_SHORTLIST"
    assert foundation["future_progression_options"]
    assert all(edge["guaranteed"] is False for edge in foundation["future_progression_options"])
    assert future["academic_assessment"]["status"] == "NOT_ASSESSED"
    assert future["pathway_position"] == "FUTURE_PROGRESSION"
    assert future["progression"][0]["progression_id"] == "PROG0001"


def test_omitted_o_level_category_is_inferred_without_defaulting_to_al(monkeypatch):
    enable(monkeypatch)
    captured = {}

    def provider(prompt, schema):
        captured["ids"] = schema["properties"]["pathways"]["items"]["properties"]["programme_id"]["enum"]
        return json.dumps({
            "pathways": [{"programme_id": "PRG0004", "progression_ids": [], "reason_code": "INTEREST_AREA_MATCH"}],
            "unverified_ideas": [],
        })

    monkeypatch.setattr(service, "_provider_generate", provider)
    response = client.post("/gemini/pathway-exploration", json={
        "learner_profile": {
            "education": {"O_LEVEL": {"Mathematics": "A", "English": "B"}},
        },
        "exploration_domain": "Information Technology",
    })
    assert response.status_code == 200, response.text
    assert "PRG0004" in captured["ids"]
    foundation = next(p for p in response.json()["pathways"] if p["programme_id"] == "PRG0004")
    assert foundation["academic_assessment"]["status"] == "NOT_ASSESSED"


def test_a_level_profile_shortlists_a_level_programmes(monkeypatch):
    enable(monkeypatch)
    captured = {}

    def provider(prompt, schema):
        captured["ids"] = schema["properties"]["pathways"]["items"]["properties"]["programme_id"]["enum"]
        return json.dumps({
            "pathways": [{"programme_id": "PRG0001", "progression_ids": [], "reason_code": "INTEREST_AREA_MATCH"}],
            "unverified_ideas": [],
        })

    monkeypatch.setattr(service, "_provider_generate", provider)
    response = client.post("/gemini/pathway-exploration", json=payload())
    assert response.status_code == 200, response.text
    assert {"PRG0001", "PRG0002", "PRG0003"}.issubset(set(captured["ids"]))


def test_reported_vocational_qualification_shortlists_documented_hnd_progression(monkeypatch):
    enable(monkeypatch)
    captured = {}

    def provider(prompt, schema):
        captured["prompt"] = prompt
        captured["ids"] = schema["properties"]["pathways"]["items"]["properties"]["programme_id"]["enum"]
        return json.dumps({
            "pathways": [{
                "programme_id": "PRG0011", "progression_ids": ["PROG0005"],
                "reason_code": "DOCUMENTED_PROGRESSION",
            }],
            "unverified_ideas": [],
        })

    monkeypatch.setattr(service, "_provider_generate", provider)
    response = client.post("/gemini/pathway-exploration", json={
        "learner_profile": {
            "learner_category": "VOCATIONAL_LEARNER",
            "education": {},
            "existing_qualifications": [{
                "title": "Electrician (NVQ Level 4 Certificate)",
                "qualification_id": "QLF0012",
                "framework": "National Vocational Qualifications",
                "level": "4",
            }],
        },
        "exploration_domain": "Vocational progression",
    })
    assert response.status_code == 200, response.text
    assert {"PRG0010", "PRG0011"}.issubset(set(captured["ids"]))
    assert '"existing_qualifications"' not in captured["prompt"]
    assert "PRIVATE_QUALIFICATION_SENTINEL" not in captured["prompt"]
    pathway = next(p for p in response.json()["pathways"] if p["programme_id"] == "PRG0011")
    assert pathway["pathway_position"] == "FUTURE_PROGRESSION"
    assert pathway["progression"][0]["progression_id"] == "PROG0005"
    assert pathway["progression"][0]["guaranteed"] is False


def test_qualification_only_profile_remains_not_assessed(monkeypatch):
    enable(monkeypatch)
    monkeypatch.setattr(service, "_provider_generate", lambda _prompt, _schema: json.dumps({
        "pathways": [{"programme_id": "PRG0005", "progression_ids": [], "reason_code": "COMPARISON_OPTION"}],
        "unverified_ideas": [],
    }))
    response = client.post("/gemini/pathway-exploration", json={
        "learner_profile": {
            "learner_category": "VOCATIONAL_LEARNER",
            "education": {},
            "existing_qualifications": [{"title": "Synthetic unverified vocational award"}],
        },
        "exploration_domain": "Information Technology",
    })
    assert response.status_code == 200, response.text
    item = next(p for p in response.json()["pathways"] if p["programme_id"] == "PRG0005")
    assert item["academic_assessment"]["status"] == "NOT_ASSESSED"
    assert item["entry_requirement_status"] == "NOT_ASSESSED"


def test_o_level_category_requires_o_level_evidence(monkeypatch):
    enable(monkeypatch)
    response = client.post("/gemini/pathway-exploration", json={
        "learner_profile": {
            "learner_category": "O_LEVEL_LEARNER",
            "education": {"A_LEVEL": {"Combined Mathematics": "B"}},
        },
        "exploration_domain": "Information Technology",
    })
    assert response.status_code == 422


def test_provider_catalogue_context_is_stable_across_private_learner_profiles():
    programmes, progression = service.verified_catalogue()
    profiles = [
        {
            "learner_category": "O_LEVEL_LEARNER",
            "education": {"O_LEVEL": {"Mathematics": "A", "English": "B"}},
            "education_complete": {"O_LEVEL": False},
            "interests": ["PRIVATE_INTEREST_SENTINEL"],
        },
        {
            "learner_category": "AL_LEARNER",
            "education": {"A_LEVEL": {"Combined Mathematics": "F"}},
            "education_complete": {"A_LEVEL": True},
            "existing_qualifications": [],
            "career_intention": "PRIVATE_CAREER_SENTINEL",
        },
    ]
    prompts = []
    for profile in profiles:
        shortlist = build_candidate_shortlist(
            profile, "Information Technology", programmes, progression,
            limit=len(programmes),
        )
        prompts.append(service._build_prompt(
            "Information Technology", [],
            sorted(shortlist["programmes"], key=lambda item: item["programme_id"]),
            sorted(shortlist["progression"], key=lambda item: item["progression_id"]),
        ))
    assert prompts[0] == prompts[1]
    assert "PRIVATE_INTEREST_SENTINEL" not in prompts[0]
    assert "PRIVATE_CAREER_SENTINEL" not in prompts[0]
    assert '"education"' not in prompts[0]
    assert '"learner_category"' not in prompts[0]


def test_live_endpoint_sends_profile_independent_complete_domain_pool(monkeypatch):
    enable(monkeypatch)
    captured = []

    def provider(prompt, schema):
        ids = schema['properties']['pathways']['items']['properties']['programme_id']['enum']
        captured.append((prompt, ids))
        return json.dumps({
            'pathways': [{
                'programme_id': ids[0],
                'progression_ids': [],
                'reason_code': 'COMPARISON_OPTION',
            }],
            'unverified_ideas': [],
        })

    monkeypatch.setattr(service, '_provider_generate', provider)
    profiles = [
        {
            'learner_category': 'O_LEVEL_LEARNER',
            'education': {'O_LEVEL': {'Mathematics': 'A', 'English': 'B'}},
            'education_complete': {'O_LEVEL': True},
            'interests': ['computing'],
            'existing_qualifications': [],
        },
        {
            'learner_category': 'VOCATIONAL_LEARNER',
            'education': {},
            'existing_qualifications': [{
                'qualification_id': 'QLF0012',
                'title': 'Electrician (NVQ Level 4 Certificate)',
            }],
            'career_intention': 'private learner-entered intention',
        },
    ]
    for profile in profiles:
        response = client.post('/gemini/pathway-exploration', json={
            'learner_profile': profile,
            'exploration_domain': 'Information Technology',
        })
        assert response.status_code == 200, response.text

    assert captured[0] == captured[1]
    expected = sorted(
        p['programme_id'] for p in service.verified_catalogue()[0]
        if p['domain'] == 'Information Technology'
    )
    assert captured[0][1] == expected
    assert len(expected) > 8  # Regression: domain now exceeds the former top-N limit.
    assert 'Electrician (NVQ Level 4 Certificate)' not in captured[0][0]
    assert 'private learner-entered intention' not in captured[0][0]
