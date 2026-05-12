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
