from pymongo import MongoClient

client = MongoClient("mongodb://vuln3-db:27017/")
db = client["nosqlidb"]

# USERS
if db.users.count_documents({}) == 0:
    db.users.insert_many([
        {"username": "admin", "password": "supersecret", "role": "admin"},
        {"username": "alice", "password": "alice123", "role": "employee"},
        {"username": "bob", "password": "bob456", "role": "employee"}
    ])

# DOCUMENTS
if db.documents.count_documents({}) == 0:
    db.documents.insert_many([
        {"owner": "admin", "title": "Q1 Budget Report",
         "content": "Total budget approved: $500,000."},

        {"owner": "alice", "title": "My Notes",
         "content": "Remember to submit timesheet by Friday."},

        {"owner": "bob", "title": "Project Plan",
         "content": "Phase 1 due end of month."},

        {"owner": "system", "title": "CONFIDENTIAL — Internal Credentials",
         "content": "FLAG{nosql_operator_I LOVE $$ <3}"}
    ])

print("Database initialized successfully 🚀")