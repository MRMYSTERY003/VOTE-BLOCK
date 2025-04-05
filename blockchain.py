import hashlib
import datetime
import sqlite3

class Blockchain:
    def __init__(self):
        self.current_votes = []
        self.db = sqlite3.connect('db.sqlite3', check_same_thread=False)
        self.init_db()

    def init_db(self):
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blockchain (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                votes TEXT,
                proof INTEGER,
                previous_hash TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS voters (
                voter_id TEXT PRIMARY KEY,
                has_voted INTEGER DEFAULT 0
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin (
                username TEXT PRIMARY KEY,
                password TEXT
            )
        ''')
        cursor.execute("INSERT OR IGNORE INTO admin (username, password) VALUES (?, ?)",
                       ('admin', hashlib.sha256('admin123'.encode()).hexdigest()))
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidates (
                name TEXT PRIMARY KEY
            )
        ''')


        self.db.commit()

    def is_valid_voter(self, voter_id):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM voters WHERE voter_id=?", (voter_id,))
        return cursor.fetchone() is not None

    def has_voted(self, voter_id):
        cursor = self.db.cursor()
        cursor.execute("SELECT has_voted FROM voters WHERE voter_id=?", (voter_id,))
        row = cursor.fetchone()
        return row and row[0] == 1

    def mark_voted(self, voter_id):
        cursor = self.db.cursor()
        cursor.execute("UPDATE voters SET has_voted=1 WHERE voter_id=?", (voter_id,))
        self.db.commit()

    def add_voter(self, voter_id):
        cursor = self.db.cursor()
        cursor.execute("INSERT OR IGNORE INTO voters (voter_id) VALUES (?)", (voter_id,))
        self.db.commit()



    def get_last_block(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM blockchain ORDER BY id DESC LIMIT 1")
        return cursor.fetchone()

    def proof_of_work(self, previous_proof):
        new_proof = 1
        while True:
            hash_val = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_val[:4] == '0000':
                return new_proof
            new_proof += 1

    def hash_block(self, block):
        return hashlib.sha256(str(block).encode()).hexdigest()

    def add_vote(self, voter_id, candidate):
        cursor = self.db.cursor()
        
        # Check if the voter has already voted
        cursor.execute("SELECT has_voted FROM voters WHERE voter_id = ?", (voter_id,))
        row = cursor.fetchone()
        if row and row[0] == 1:
            return False

        self.current_votes.append({'voter_id': voter_id, 'candidate': candidate})
        cursor.execute("UPDATE voters SET has_voted = 1 WHERE voter_id = ?", (voter_id,))
        self.db.commit()
        return True


    def mine_block(self):
        last = self.get_last_block()
        previous_proof = last[3] if last else 1
        previous_hash = self.hash_block(last) if last else '0'
        proof = self.proof_of_work(previous_proof)
        timestamp = str(datetime.datetime.now())
        votes_str = str(self.current_votes)
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO blockchain (timestamp, votes, proof, previous_hash) VALUES (?, ?, ?, ?)",
                       (timestamp, votes_str, proof, previous_hash))
        self.db.commit()
        self.current_votes = []

    def get_vote_count(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT votes FROM blockchain")
        all_blocks = cursor.fetchall()
        vote_counts = {}
        for row in all_blocks:
            votes = eval(row[0])
            for vote in votes:
                name = vote['candidate']
                vote_counts[name] = vote_counts.get(name, 0) + 1
        return vote_counts

    def get_chain(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM blockchain")
        return cursor.fetchall()

    def reset_election(self):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM blockchain")
        cursor.execute("DELETE FROM voters")
        self.db.commit()

    def check_admin(self, username, password):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM admin WHERE username=? AND password=?",
                       (username, hashlib.sha256(password.encode()).hexdigest()))
        return cursor.fetchone() is not None




    def add_candidate(self, name):
        try:
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO candidates (name) VALUES (?)", (name,))
            self.db.commit()
            return True
        except:
            return False

    def delete_candidate(self, name):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM candidates WHERE name=?", (name,))
        self.db.commit()

    def get_candidates(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT name FROM candidates")
        return [row[0] for row in cursor.fetchall()]
