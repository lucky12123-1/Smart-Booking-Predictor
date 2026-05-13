"""
Sample flight routes for POC testing.
"""


def get_sample_routes():
    """
    Returns a list of sample routes for testing.
    
    Returns:
        List of route dictionaries with structure:
        {
            'from': source city code,
            'to': destination city code,
            'type': 'business' or 'leisure'
        }
    """
    routes = [
        {
            'from': 'BOM',
            'to': 'DEL',
            'type': 'business'
        },
        {
            'from': 'BOM',
            'to': 'GOA',
            'type': 'leisure'
        },
        {
            'from': 'BOM',
            'to': 'BLR',
            'type': 'business'
        },
        {
            'from': 'DEL',
            'to': 'HYD',
            'type': 'business'
        }
    ]
    
    return routes


def find_sample_route(source, destination):
    """
    Find a sample route by source and destination airport codes.

    Args:
        source: Source city/airport code
        destination: Destination city/airport code

    Returns:
        Matching route dictionary, or None when the sector is unavailable
    """
    source = source.upper()
    destination = destination.upper()

    for route in get_sample_routes():
        if route['from'] == source and route['to'] == destination:
            return route

    return None
