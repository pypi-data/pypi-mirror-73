from .osrm import NearestResponse, RouteResponse, TableResponse, MatchResponse, parse_google_coords, LatLng 

def test_parse_google_coords():
    a = parse_google_coords('1,2|3,4|5,6')
    assert len(a) == 3
    assert a[0] == LatLng(lat=1,lng=2)
    assert a[1] == LatLng(lat=3,lng=4)
    assert a[2] == LatLng(lat=5,lng=6)

    b = parse_google_coords('1,2')
    assert len(b) == 1
    assert b[0] == LatLng(lat=1,lng=2)


def test_nearest_response():
    mock = {
        'code': 'Ok',
        'waypoints': [
            {
                'hint': '',
                'distance': 1.0,
                'name': 'whocares',
                'location': [1.0, 2.0],
                'nodes':[1, 20],
            },
        ],
    }
    NearestResponse(**mock)


def test_route_response():
    mock = {
        'code': 'Ok',
        'routes': [
            {
                'distance': 1.0,
                'duration': 1.0,
                'legs': [
                    {
                        'distance': 1.0,
                        'duration': 1.0,
                    },
                ],
            },
        ],
    }
    RouteResponse(**mock)


def test_table_response():
    mock = {
        'code': 'Ok',
        'sources': [
            {
                'name': 'whocares',
                'location': [1.0, 2.0],
            },
        ],
        'destinations': [
            {
                'name': 'whocares',
                'location': [1.0, 2.0],
            },
        ],
        'durations': [
            [
                1.0,
            ],
        ],
        'distances': [
            [
                1.0,
            ],
        ],
    }
    TableResponse(**mock)


def test_match_response():
    mock = {
        'code': 'Ok',
        'tracepoints': [
            {
                'matchings_index': 1,
                'location': [1.0, 2.0],
            },
        ],
        'matchings': [
            {
                'distance': 1.0,
            },
        ],
    }
    MatchResponse(**mock)
