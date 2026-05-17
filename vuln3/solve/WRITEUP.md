# Writeup — NoSQL Operator Injection (CorpPortal Document Portal)
CWE-943 | MongoDB | Flask | Port 5003

---

## The Setup

The target was an internal employee document portal called CorpPortal.
When I first opened it, I got a simple page listing three endpoints:

    POST /login      — takes username and password
    POST /documents  — returns your own documents
    POST /search     — lets you search documents by owner

Nothing fancy. Just a login page backed by MongoDB. But the moment I saw
MongoDB, I started thinking about operator injection.

---

## Finding the First Vulnerability — /login

The login endpoint takes a JSON body with username and password. The obvious
first thing to try is whether it sanitizes the input or just passes it
straight into the database query.

I sent a normal request first just to see what the response looks like:

    POST /login
    {
        "username": "admin",
        "password": "wrongpassword"
    }

Got back: "Invalid credentials." — expected.

Then I tried replacing the password with a MongoDB operator:

    POST /login
    {
        "username": "admin",
        "password": {"$gt": ""}
    }

And got back: "Welcome, admin!"

That was it. Login bypassed. The app was taking my JSON input and passing it
directly into the MongoDB query without any type checking. MongoDB saw
{"$gt": ""} and treated it as an operator instead of a string — meaning
"find a user where the password is greater than an empty string." Since any
real password satisfies that condition, it returned the admin account
immediately.

The vulnerable line in the code is this:

    user = db.users.find_one({"username": username, "password": password})

No isinstance() check. No sanitization. Whatever I send in the JSON body
goes straight into the query.

---

## Going Further — Chaining $in with $gt

At this point I had bypassed login, but I wanted to demonstrate a more
realistic attack. In a real scenario, an attacker would not even know
the admin username. So I replaced the username with a $in operator
to guess it from a list of common names, while keeping $gt on the password:

    POST /login
    {
        "username": {"$in": ["admin", "administrator", "root", "superuser"]},
        "password": {"$gt": ""}
    }

$in checks whether the stored username matches any value in my list.
$gt makes the password condition always true.

MongoDB ran both operators in one query and returned the first account
it found. The response said "Welcome, admin!" — so now I knew the real
username without having guessed it manually.

Two operators. One request. Full authentication bypass plus username discovery.

---

## The Flag Was Not Here Yet

After getting in, I checked /documents to see what the admin can access:

    POST /documents
    {
        "username": "admin"
    }

I got back the admin's documents — a budget report, nothing interesting.
No flag here.

I noticed there was a third endpoint: /search. This one lets you search
documents by owner. That sounded interesting — if it is also vulnerable,
maybe I can access documents belonging to other users, or even hidden ones.

---

## Breaking Access Control — /search with $ne

The /search endpoint takes a username to verify you are a known user,
and a doc_owner field to filter documents by owner.

I sent a normal request first:

    POST /search
    {
        "username": "admin",
        "doc_owner": "alice"
    }

Got Alice's documents. So this endpoint already lets you read anyone's
documents just by knowing their name. That is already a problem, but the
flag still was not there.

Then I tried injecting an operator into doc_owner:

    POST /search
    {
        "username": "admin",
        "doc_owner": {"$ne": null}
    }

$ne: null means "owner is not null" — which is true for every single
document in the database. MongoDB returned all documents from all owners,
including one I had never seen before:

    owner   : system
    title   : CONFIDENTIAL — Internal Credentials
    content : FLAG{nosql_operator_I LOVE $$ <3}

The "system" owner has no login account. There is no way to reach this
document through normal application flow. The /documents endpoint only
shows your own documents. The /search endpoint was the only way in —
and it was wide open to operator injection.

The vulnerable line:

    docs = list(db.documents.find(
        {"owner": doc_owner},
        {"_id": 0}
    ))

Same problem as /login. doc_owner goes straight into the query.
No type checking. No sanitization.

---

## About the Flag

The flag is FLAG{nosql_operator_I LOVE $$ <3}

The $$ in the flag is not a coincidence. Every MongoDB operator starts
with a "$" sign — $ne, $gt, $in, $where, $regex. The entire attack
worked because the application let me inject these $ operators directly
into its database queries. Without $, there is no injection.

The flag is basically laughing at the vulnerability itself.
The same "$" that broke the authentication, bypassed access control,
and leaked the hidden document — that is the "$" in "I LOVE $$."

---

## The Full Attack Chain

Here is the complete exploit from start to flag, step by step:

Step 1 — Send $in + $gt to /login in one request.
          MongoDB matches admin from the username list.
          $gt makes the password condition always true.
          Login bypassed, real username discovered from the welcome message.

Step 2 — Send $ne: null to /search as doc_owner.
          MongoDB interprets this as "owner is not null" — matches everything.
          All documents returned including the hidden system document.

Step 3 — Read the flag from the system document content.

Three operators. Two requests. Flag captured.

---

## Why This Works — Root Cause

MongoDB queries are JSON objects. When a developer writes:

    db.users.find_one({"username": username, "password": password})

They expect username and password to be plain strings. But if the app
accepts JSON input and passes it directly to the query without checking
the type, an attacker can send a JSON object instead of a string.
MongoDB cannot tell the difference between developer-intended query logic
and attacker-injected query logic. It just runs whatever it receives.

This is the core of NoSQL injection — the database treats attacker input
as query operators because the application never verified it was a string.

---

## Kill Chain (Lockheed Martin)

    Reconnaissance       — Opened / to read the API endpoint list
    Weaponization        — Prepared payloads using $in, $gt, $ne operators
    Delivery             — Sent POST /login with operator payload
    Exploitation         — MongoDB executed the operators, auth bypassed
    Installation         — Discovered real admin username from response
    Command and Control  — Sent POST /search with $ne: null
    Actions on Objective — All documents returned, hidden flag captured

---

## MITRE ATT&CK

    T1190 — Exploit Public-Facing Application
    T1078 — Valid Accounts (impersonating admin after bypass)
    T1530 — Data from Cloud Storage (document exfiltration)

---

## CVSS v3.1

    Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N
    Score: 9.1 (Critical)

    AV:N — Exploitable over the network, no physical access needed
    AC:L — No special conditions required, works every time
    PR:N — No account or privileges needed before the attack
    UI:N — Victim does not need to do anything
    C:H  — All documents exposed including confidential hidden ones
    I:H  — Authentication completely bypassed

---

## The Fix

The fix is one line per vulnerable endpoint. Check that the input is
actually a string before passing it to MongoDB:

    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({"error": "invalid input"}), 400

    if not isinstance(doc_owner, str):
        return jsonify({"error": "invalid input"}), 400

If the input is an object or array instead of a string, reject it.
MongoDB operators cannot be injected through plain strings.