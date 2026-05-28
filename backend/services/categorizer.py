import re

def smart_categorize(notes: str) -> str:
    """
    Analyzes transaction notes using heuristics to determine the most likely category
    and whether it might be a recurring subscription.
    Returns: (category, is_recurring)
    """
    if not notes:
        return 'Other', False
        
    notes_lower = notes.lower()
    
    # Heuristic maps
    categories = {
        'Food': ['mcdonald', 'burger', 'pizza', 'restaurant', 'cafe', 'starbucks', 'grocery', 'walmart', 'kroger', 'whole foods'],
        'Transport': ['uber', 'lyft', 'gas', 'shell', 'chevron', 'transit', 'train', 'bus'],
        'Housing': ['rent', 'mortgage', 'electric', 'water', 'internet', 'comcast', 'xfinity', 'utilities'],
        'Entertainment': ['netflix', 'hulu', 'spotify', 'movie', 'cinema', 'game', 'steam', 'xbox', 'playstation', 'apple music'],
        'Shopping': ['amazon', 'target', 'best buy', 'clothes', 'shoes', 'apple store'],
        'Salary': ['payroll', 'salary', 'employer', 'direct deposit', 'dividend']
    }
    
    subscriptions = ['netflix', 'hulu', 'spotify', 'internet', 'comcast', 'xfinity', 'apple music', 'gym', 'planet fitness', 'rent', 'mortgage']
    
    detected_category = 'Other'
    for cat, keywords in categories.items():
        if any(keyword in notes_lower for keyword in keywords):
            detected_category = cat
            break
            
    is_recurring = any(sub in notes_lower for sub in subscriptions)
    
    return detected_category, is_recurring
