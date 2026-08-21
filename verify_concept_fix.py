import json
from unittest.mock import patch
from concept_generator.ai_client import ConceptGeneratorClient
from concept_generator.prompt_builder import build_prompt
from concept_generator.report_parser import normalize_report


def fake_response_for(prompt: str):
    if 'pool' in prompt and 'home theatre' in prompt.lower():
        return json.dumps({
            'concept_summary': 'Pool-forward villa with a resort-like public spine and media-focused leisure wing.',
            'zoning_logic': ['Public amenity spaces front the arrival court.', 'Private family rooms sit behind a quiet retreat corridor.'],
            'space_allocation': [
                {'zone_name': 'Public / Guest Facing', 'area_sqft': 1200, 'percent': 40.0},
                {'zone_name': 'Private / Living', 'area_sqft': 900, 'percent': 30.0},
                {'zone_name': 'Service / Back of House', 'area_sqft': 300, 'percent': 10.0},
            ],
            'adjacency_rationale': ['Pool terrace connects to guest lounge.'],
            'future_expansion': ['Future pool cabana.'],
            'disclaimer': 'Conceptual visualization only — consult a licensed architect before construction.',
        })
    return json.dumps({
        'concept_summary': 'Privacy-first multigenerational villa with a quiet service edge and strong separations between family clusters.',
        'zoning_logic': ['A protected parent wing is placed away from the front arrival zone.', 'Shared family areas are kept central but separated from service functions.'],
        'space_allocation': [
            {'zone_name': 'Public / Guest Facing', 'area_sqft': 800, 'percent': 26.7},
            {'zone_name': 'Private / Living', 'area_sqft': 1500, 'percent': 50.0},
            {'zone_name': 'Service / Back of House', 'area_sqft': 400, 'percent': 13.3},
        ],
        'adjacency_rationale': ['A protected family core reduces interference between generations.'],
        'future_expansion': ['Add a second-generation suite near the service edge.'],
        'disclaimer': 'Conceptual visualization only — consult a licensed architect before construction.',
    })

class FakeResponse:
    def __init__(self, text):
        self._text = text
    def raise_for_status(self):
        return None
    def json(self):
        return json.loads(self._text)

with patch('concept_generator.ai_client.requests.post') as mock_post:
    def side_effect(url, headers=None, data=None, timeout=None):
        payload = json.loads(data)
        prompt = payload['messages'][0]['content']
        return FakeResponse(fake_response_for(prompt))
    mock_post.side_effect = side_effect

    client = ConceptGeneratorClient(api_key='fake-key')
    req1 = {'bedrooms': 4, 'bathrooms': 4, 'car_bays': 4, 'pool': 'Yes', 'home_theatre': 'Yes', 'gym': 'Yes', 'guest_suite': 'Yes', 'staff_quarters': 'No'}
    req2 = {'bedrooms': 5, 'bathrooms': 5, 'car_bays': 4, 'pool': 'No', 'home_theatre': 'No', 'gym': 'No', 'guest_suite': 'Yes', 'staff_quarters': 'Yes'}
    plot1 = {'plot_width': 90, 'plot_length': 140, 'orientation': 'North', 'site_note': 'Bengaluru'}
    plot2 = {'plot_width': 95, 'plot_length': 150, 'orientation': 'East', 'site_note': 'Bengaluru'}
    ctx1 = 'We want a pool, home theatre and an inviting guest lounge.'
    ctx2 = 'Large joint family, want maximum privacy between generations and a quiet service edge.'

    p1 = build_prompt('villa', req1, ctx1, plot1)
    p2 = build_prompt('villa', req2, ctx2, plot2)
    print('PROMPT_1_DIFFERS:', p1 != p2)
    print('PROMPT_1_HAS_POOL:', 'pool' in p1.lower() and 'home theatre' in p1.lower())
    print('PROMPT_2_HAS_PRIVACY:', 'privacy' in p2.lower() and 'generations' in p2.lower())

    out1 = normalize_report(client.generate_concept('villa', req1, ctx1, plot1))
    out2 = normalize_report(client.generate_concept('villa', req2, ctx2, plot2))

    print('OUT1_SUMMARY:', out1['concept_summary'])
    print('OUT1_SPACE:', out1['space_allocation'])
    print('OUT1_DIAGRAM:', out1['diagram'])
    print('OUT2_SUMMARY:', out2['concept_summary'])
    print('OUT2_SPACE:', out2['space_allocation'])
    print('OUT2_DIAGRAM:', out2['diagram'])
    print('DIAGRAM_AND_SPACE_SAME_SOURCE:', out1['diagram'][0]['area'] == out1['space_allocation'][0]['area_sqft'] and out2['diagram'][0]['area'] == out2['space_allocation'][0]['area_sqft'])
