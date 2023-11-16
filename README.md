# VersionedScope
Implement a VersionedScope class

_Using no external library imports, Implement a class for applying groups of changes to collections of properties. Each instance of this class, at any given time should have maximum one value for a given property. There, each property set within the class is like a variable name within some scope.

Property Change Tracking: The class must track changes to properties within a VersionedScope . Each modification to a property should be recorded as a distinct event, capturing the nature of the change.
Transactional Commit System: Implement a system where changes to properties are grouped into transactions. These transactions can encompass multiple changes and should be committed as a single unit. The class must offer functionality to commit and manage these transactions.
History Management: Each 'commit' of a transaction of changes should be given a version number based on the current timestamp and stored in some private variable. The object should maintain a comprehensive history of all changes made within the VersionedScope . This history should detail each change, including the type of change (addition or deletion), the affected property, its previous and new values, and the timestamp of the change.
Conflict Detection and Resolution: The class should have the capability to detect conflicts when committing transactions (e.g., concurrent modifications to the same property). It must have mechanisms (ie, defauting) for either resolving these conflicts or aborting the transaction in case of unresolvable conflicts.
Rollback Functionality: Enable functionality to roll back the VersionedScope to a previous state. This involves reverting the properties to their values at a specified point in the history.
Querying and Retrieving Past States: The class should allow querying the historical states by at least: !"A point in time !"'# of transactions' prior to the current state 7. Querying commit version by Property: We should be able to get the transaction # or version that a current property was added.
Error Handling and Validation: The class must include robust error handling and validation mechanisms to maintain the integrity of the VersionedScope 's state. This includes managing invalid operations and handling edge cases effectively.
Stateful Commits The set and delete method for properties of a Versioned Scope should add the changes to the latest pending transaction to the versioned scope, which shouldn't update its history until a commit() method is called.
