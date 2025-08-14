#!/usr/bin/env python3
"""
Test script for the Empathetic Code Reviewer
"""

import json
from empathetic_reviewer import EmpathethicCodeReviewer

def test_with_example():
    """Test the reviewer with the provided example."""
    
    # Load example data
    with open('example_input.json', 'r') as f:
        test_data = json.load(f)
    
    print("🔍 Testing Empathetic Code Reviewer")
    print("=" * 50)
    print(f"Code snippet: {test_data['code_snippet'][:50]}...")
    print(f"Number of comments: {len(test_data['review_comments'])}")
    print("\nOriginal comments:")
    for i, comment in enumerate(test_data['review_comments'], 1):
        print(f"  {i}. {comment}")
    
    print("\n" + "=" * 50)
    print("🤖 Generating empathetic review...")
    print("=" * 50)
    
    try:
        # Note: This requires OPENAI_API_KEY to be set
        reviewer = EmpathethicCodeReviewer()
        result = reviewer.process_json_input(test_data)
        
        print(result)
        
        # Save result to file
        with open('example_output.md', 'w') as f:
            f.write(result)
        print(f"\n✅ Review saved to example_output.md")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nNote: Make sure to set your OPENAI_API_KEY environment variable")

def test_different_scenarios():
    """Test with different types of feedback scenarios."""
    
    scenarios = [
        {
            "name": "JavaScript with Harsh Comments",
            "data": {
                "code_snippet": "function calculateTotal(items) {\n    var total = 0;\n    for (var i = 0; i < items.length; i++) {\n        total = total + items[i].price;\n    }\n    return total;\n}",
                "review_comments": [
                    "Don't use var, it's terrible practice.",
                    "This loop is ancient. Use modern JavaScript.",
                    "No error handling. What if items is null?"
                ]
            }
        },
        {
            "name": "Python with Mixed Severity",
            "data": {
                "code_snippet": "class UserManager:\n    def __init__(self):\n        self.users = []\n    \n    def add_user(self, user):\n        self.users.append(user)\n        return True",
                "review_comments": [
                    "Consider adding input validation for the user parameter.",
                    "The return value True doesn't provide useful information.",
                    "This class could benefit from type hints."
                ]
            }
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🧪 Testing: {scenario['name']}")
        print("-" * 40)
        
        try:
            reviewer = EmpathethicCodeReviewer()
            result = reviewer.process_json_input(scenario['data'])
            
            # Save to file
            filename = f"test_{scenario['name'].lower().replace(' ', '_')}.md"
            with open(filename, 'w') as f:
                f.write(result)
            print(f"✅ Saved to {filename}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Empathetic Code Reviewer Test Suite")
    print("=" * 50)
    
    # Test with the main example
    test_with_example()
    
    # Test with additional scenarios
    print("\n" + "=" * 50)
    print("🔬 Testing Additional Scenarios")
    print("=" * 50)
    test_different_scenarios()