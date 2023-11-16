from datetime import datetime
from collections import defaultdict

class VersionedScope:
    def __init__(self):
        self.properties = {}
        self.transactions = {}
        self.history = []
        self.pending_transaction = defaultdict(dict)

    def set(self, key, value):
        self.pending_transaction[key] = {'action': 'set', 'value': value}

    def delete(self, key):
        self.pending_transaction[key] = {'action': 'delete'}

    def commit(self):
        if self.pending_transaction:
            timestamp = datetime.now()
            version = len(self.transactions) + 1

            # Check for conflicts
            conflicts = self.detect_conflicts()
          
            if conflicts:
                # Resolve conflicts (overwrite with the latest change)
                for conflict in conflicts:
                    key = conflict['key']
                    latest_change = conflict['latest_change']
                    self.pending_transaction[key] = latest_change

            # Apply changes to properties
            for key, change in self.pending_transaction.items():
                if change['action'] == 'set':
                    self.properties[key] = change['value']
                elif change['action'] == 'delete' and key in self.properties:
                    del self.properties[key]

            # Record the transaction in history
            self.transactions[version] = {'timestamp': timestamp, 'changes': dict(self.pending_transaction)}
            self.history.append(self.transactions[version])

            # Clear pending_transaction for the next transaction
            self.pending_transaction = defaultdict(dict)

            return version
        else:
            raise ValueError("No changes to commit")

    def detect_conflicts(self):
        conflicts = []
        for key, change in self.pending_transaction.items():
            if key in self.properties:
                conflicts.append({'key': key, 'latest_change': self.pending_transaction[key]})
        return conflicts

    def rollback(self, version):
        if 1 <= version <= len(self.transactions):
            # Revert properties to the specified version
            self.properties = {}
            for v in range(1, version + 1):
                for key, change in self.transactions[v]['changes'].items():
                    if change['action'] == 'set':
                        self.properties[key] = change['value']
                    elif change['action'] == 'delete' and key in self.properties:
                        del self.properties[key]
                
        else:
            raise ValueError("Invalid version number")

    def get_property_version(self, key):
        if key not in self.properties:
            return None

        value = self.properties[key]
    
        for version, transaction in reversed(self.transactions.items()):
           
            if key in transaction['changes'] and transaction['changes'][key]['action'] == 'set':
                if value == transaction['changes'][key]['value']:
                    return version
        

    def query_history(self, point_in_time=None, transactions_prior=None):
        if point_in_time:
            return next((entry for entry in self.history if entry['timestamp'] == point_in_time), None)
        elif transactions_prior:
            start_version = max(1, len(self.transactions) - transactions_prior + 1)
            return [self.transactions[i] for i in range(start_version, len(self.transactions) + 1)]
        else:
            return self.history
