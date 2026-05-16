# 🔒 PassGuard — Password Strength Checker & Generator

A cybersecurity-focused web application built with **Python** and **Flask** that helps users evaluate the strength of their passwords and generate cryptographically sound alternatives.

---

## Features

- **Real-time Password Analysis** — Instantly evaluates your password as you type
- **Entropy Score** — Calculates password entropy in bits (higher = harder to crack)
- **9-Point Checklist** — Checks length tiers, character variety, repeating patterns, and sequential patterns
- **Common Password Detection** — Flags passwords found in known breach/common-password lists
- **Strength Meter** — Visual indicator: Weak / Fair / Strong / Very Strong
- **Actionable Feedback** — Tells you exactly what to improve
- **Password Generator** — Generates cryptographically random passwords with:
  - Configurable length (4–128 characters)
  - Toggle uppercase, lowercase, numbers, and symbols
- **Copy to Clipboard** — One-click copy on all password fields
- **Modern Dark UI** — Clean cybersecurity aesthetic, fully responsive

---

## Project Structure

```
password-checker/
├── app.py              # Flask web server & API routes
├── checker.py          # Core password analysis and generation logic
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── templates/
│   └── index.html      # Web interface (Jinja2)
└── static/
    ├── style.css       # Dark-theme styling
    └── script.js       # Frontend logic (fetch API, real-time UI)
```

---

## How It Works

### Strength Scoring (0–100)

| Factor                        | Points  |
|-------------------------------|---------|
| Length ≥ 16 characters        | 35 pts  |
| Length ≥ 12 characters        | 25 pts  |
| Length ≥ 8 characters         | 15 pts  |
| Each character type present   | 10 pts each (max 40) |
| No repeating characters       | 12 pts  |
| No sequential patterns        | 13 pts  |
| Common/known password         | Score capped at 15 |

### Strength Labels

| Score   | Label       |
|---------|-------------|
| 75–100  | Very Strong |
| 50–74   | Strong      |
| 25–49   | Fair        |
| 0–24    | Weak        |

### Entropy Calculation

```
Entropy = length × log₂(charset_size)
```

Where `charset_size` is the total pool of possible characters used.

---

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip

### Steps

**1. Clone or download the project**

```bash
git clone https://github.com/yourusername/passguard.git
cd passguard
```

**2. (Optional) Create a virtual environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Run the application**

```bash
python app.py
```

**5. Open your browser**

```
http://localhost:5000
```

---

## API Endpoints

| Method | Endpoint    | Description                        |
|--------|-------------|------------------------------------|
| GET    | `/`         | Serve the web interface            |
| POST   | `/check`    | Analyze a password's strength      |
| POST   | `/generate` | Generate a random strong password  |

### POST `/check`

**Request:**
```json
{ "password": "MyP@ssw0rd!" }
```

**Response:**
```json
{
  "score": 82,
  "label": "Very Strong",
  "color": "#00e676",
  "entropy": 65.5,
  "is_common": false,
  "checks": {
    "length_8": true,
    "length_12": false,
    "has_upper": true,
    "has_lower": true,
    "has_digit": true,
    "has_symbol": true,
    "no_repeating": true,
    "no_sequential": true
  },
  "feedback": []
}
```

### POST `/generate`

**Request:**
```json
{
  "length": 20,
  "use_upper": true,
  "use_lower": true,
  "use_digits": true,
  "use_symbols": true
}
```

**Response:**
```json
{
  "password": "k#T9mZ!qRv@2pLxN^dWs",
  "strength": { ... }
}
```

---

## Technologies Used

| Layer    | Technology              |
|----------|-------------------------|
| Backend  | Python 3, Flask         |
| Frontend | HTML5, CSS3, JavaScript |
| Fonts    | Inter, JetBrains Mono (Google Fonts) |
| Logic    | `math`, `random`, `string`, `re` (stdlib only) |

---

## Security Notes

- Passwords are **never stored or logged** — all checks happen in memory per request
- Password generation uses Python's `random.choice()` over a validated charset with guaranteed character inclusion
- The common password list covers 100+ widely known weak passwords
- This tool is for **educational and personal use** — always use a dedicated password manager for production credentials

---

## License

MIT License — free to use, modify, and distribute.
