# 🗳️ Blockchain-Based Online Voting System

A secure and tamper-proof **online voting system** built using **Python (Flask)** and **Blockchain technology**. This application ensures each voter can vote only once, and the votes are stored immutably using a basic blockchain mechanism.

---

## 📌 Features

- ✅ Voter authentication using Voter ID  
- ✅ Prevents double voting  
- ✅ Blockchain-powered vote storage  
- ✅ Admin panel to manage candidates and voters  
- ✅ Vote count display  
- ✅ Simple and elegant UI with Tailwind CSS  
- ✅ SQLite database for persistence  

---

## 📸 Screenshots

> Coming soon… *(add images/gifs of your app once deployed or running locally)*

---

## ⚙️ Tech Stack

| Layer       | Tech                              |
|-------------|-----------------------------------|
| Backend     | Python, Flask                     |
| Frontend    | HTML, Tailwind CSS                |
| Database    | SQLite                            |
| Security    | Blockchain, SHA256 Hashing        |
| Deployment  | *(Optional)* GitHub Pages / GCP / AWS  

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/MRMYSTERY003/VOTE-BLOCK.git
cd blockchain-voting-system
```

2. Create a Virtual Environment & Install Dependencies
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the App
```
python app.py
Visit http://127.0.0.1:5000 in your browser.
```

🔐 Admin Login
Username	Password
admin	admin123
(Credentials are stored in hashed form in the SQLite DB)

📂 Project Structure
```
.
├── app.py                    # Main Flask application
├── blockchain.py            # Blockchain class and logic
├── db.sqlite3               # SQLite database
├── templates/               # HTML templates
│   ├── index.html           # Voting page
│   ├── admin.html           # Admin panel (optional)
│   └── navbar.html          # Navbar template
├── static/                  # (Optional) CSS or JS files
├── README.md
└── requirements.txt         # Python dependencies
```

📈 Future Improvements (TODOs)
 Deploy live using GCP or AWS

 Add email verification for voters

 Live vote results dashboard

 Blockchain explorer page

 Metamask / Web3 integration (real blockchain)

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

📄 License
This project is licensed under the MIT License.


