Here's a simple `README.md` file with just the essential information:

```markdown
# SecurePass

A secure password manager with celebration page generator built using Python Flask.

## Technologies Used
- **Backend**: Python 3, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: Encrypted text files

## How to Use

1. **Installation**:
```bash
git clone https://github.com/yourusername/securepass.git
cd securepass
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
pip install -r requirements.txt
mkdir -p data static/celebration_pages
```

2. **Run the app**:
```bash
python app.py
```

3. **Access in browser**:
```
http://localhost:5000
```

4. **Features**:
- Create a master password on first run
- Store passwords in encrypted format
- Generate celebration pages for special events
