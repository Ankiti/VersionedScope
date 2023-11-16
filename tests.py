from versionScope import VersionedScope
from datetime import datetime

def run_tests():
    # Test Case 1: Basic usage
    scope = VersionedScope()

    scope.set('name', 'John')
    scope.set('age', 25)
    version1 = scope.commit()

    scope.set('name', 'Jane')
    scope.set('city', 'New York')
    version2 = scope.commit()

    
    assert scope.properties == {'name': 'Jane', 'age': 25, 'city': 'New York'}
    
    assert scope.get_property_version('name') == version2
    assert scope.get_property_version('city') == version2

    # Test Case 2: Conflict resolution
    scope.set('name', 'Jack')
    scope.set('age', 30)
    version3 = scope.commit()

    scope.set('name', 'Jake')
    scope.set('city', 'Los Angeles')
    version4 = scope.commit()

    assert scope.properties == {'name': 'Jake', 'age': 30, 'city': 'Los Angeles'}
    assert scope.get_property_version('name') == version4
    assert scope.get_property_version('city') == version4

    # Test Case 3: Rollback
    scope.rollback(version3)
 
    assert scope.properties == {'name': 'Jack', 'age': 30, 'city': 'New York'}
    
    assert scope.get_property_version('name') == version3
    assert scope.get_property_version('city') == version2

    # Test Case 4: Query historical states
    history = scope.query_history()
    assert len(history) == 4  # Four transactions (initial, commit1, commit2, rollback)

    point_in_time = scope.history[1]['timestamp']
    history_at_point = scope.query_history(point_in_time=point_in_time)
    assert history_at_point == scope.history[1]

    transactions_prior = 2
    history_prior = scope.query_history(transactions_prior=transactions_prior)
    assert len(history_prior) == transactions_prior

    # Test Case 5: Error handling
    try:
        scope.rollback(0)  # Invalid version number
    except ValueError as e:
        assert str(e) == "Invalid version number"

    try:
        scope.rollback(10)  # Version doesn't exist
    except ValueError as e:
        assert str(e) == "Invalid version number"

    try:
        scope.commit()  # No changes to commit
    except ValueError as e:
        assert str(e) == "No changes to commit"


    # Test Case 6: Conflicting deletes
    new_scope = VersionedScope()

    new_scope.set('name', 'John')
    new_scope.set('age', 25)
    version1 = new_scope.commit()

    new_scope.delete('name')
    new_scope.set('city', 'New York')
    version2 = new_scope.commit()

    assert new_scope.properties == {'age': 25, 'city': 'New York'}
    assert new_scope.get_property_version('name') is None
    assert new_scope.get_property_version('city') == version2

    # Test Case 7: Multiple rollbacks
    new_scope.rollback(version1)
    assert new_scope.properties == {'name': 'John', 'age': 25}
    assert new_scope.get_property_version('name') == version1
    assert new_scope.get_property_version('city') is None

    new_scope.rollback(version2)
  
    assert new_scope.properties == {'age': 25, 'city': 'New York'}
    assert new_scope.get_property_version('name') is None
    assert new_scope.get_property_version('city') == version2

    # Test Case 8: Query history with non-existent timestamp
    assert new_scope.query_history(point_in_time=datetime(2022, 1, 1)) is None

    # Test Case 9: Query history with invalid transactions_prior
    assert new_scope.query_history(transactions_prior=0) == new_scope.query_history()

    print("All test cases passed!")

# Run the tests
run_tests()

