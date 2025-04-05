from flask import Flask, render_template, request, redirect, session
from blockchain import Blockchain

app = Flask(__name__)
app.secret_key = 'supersecretkey'
blockchain = Blockchain()

@app.route('/')
def index():
    candidates = blockchain.get_candidates()
    return render_template('index.html', candidates=candidates)


@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        voter_id = request.form['voter_id'].strip()
        candidate = request.form['candidate']

        if not blockchain.is_valid_voter(voter_id):
            return render_template('index.html', error="Invalid Voter ID", candidates=blockchain.get_candidates())

        if blockchain.has_voted(voter_id):
            return render_template('index.html', error="You have already voted!", candidates=blockchain.get_candidates())

        blockchain.add_vote(voter_id, candidate)
        blockchain.mark_voted(voter_id)
        return render_template('index.html', success="Your vote has been recorded successfully!", candidates=blockchain.get_candidates())

    # GET request
    return render_template('index.html', candidates=blockchain.get_candidates())



@app.route('/mine')
def mine():
    blockchain.mine_block()
    return render_template('mine.html')

@app.route('/result')
def result():
    votes = blockchain.get_vote_count()
    return render_template('result.html', votes=votes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if blockchain.check_admin(request.form['username'], request.form['password']):
            session['admin'] = True
            return redirect('/admin')
        else:
            return "Invalid login"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        return redirect('/login')

    message = ""
    if request.method == 'POST':
        action = request.form['action']
        if action == 'reset':
            blockchain.reset_election()
            message = "Election reset."
        elif action == 'add_candidate':
            name = request.form['candidate_name'].strip()
            if name:
                if blockchain.add_candidate(name):
                    message = f"Candidate '{name}' added."
                else:
                    message = f"Candidate '{name}' already exists."
        elif action == 'delete_candidate':
            name = request.form['candidate_name'].strip()
            blockchain.delete_candidate(name)
            message = f"Candidate '{name}' deleted."

        elif action == 'add_voter':
            new_voter = request.form['new_voter'].strip()
            if new_voter:
                blockchain.add_voter(new_voter)
                message = f"Voter '{new_voter}' added."


    votes = blockchain.get_vote_count()
    chain = blockchain.get_chain()
    candidates = blockchain.get_candidates()
    return render_template('admin.html', votes=votes, chain=chain, message=message, candidates=candidates)


if __name__ == '__main__':
    app.run(debug=True)
