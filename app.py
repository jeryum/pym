from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
import hashlib
import base64
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Configuration
PASSWORD_FILE = "data/passwords.enc"
MASTER_KEY_FILE = "data/master.key"
CELEBRATION_PAGES_DIR = "static/celebration_pages"
os.makedirs("data", exist_ok=True)
os.makedirs(CELEBRATION_PAGES_DIR, exist_ok=True)

# Simple encryption/decryption functions
def simple_encrypt(data: str, key: str) -> str:
    """Simple XOR encryption"""
    key = hashlib.sha256(key.encode()).hexdigest()
    encrypted = []
    for i, c in enumerate(data):
        key_c = key[i % len(key)]
        encrypted_c = chr(ord(c) + ord(key_c) % 256)
        encrypted.append(encrypted_c)
    return base64.urlsafe_b64encode(''.join(encrypted).encode()).decode()

def simple_decrypt(encrypted_data: str, key: str) -> str:
    """Simple XOR decryption"""
    key = hashlib.sha256(key.encode()).hexdigest()
    encrypted_data = base64.urlsafe_b64decode(encrypted_data.encode()).decode()
    decrypted = []
    for i, c in enumerate(encrypted_data):
        key_c = key[i % len(key)]
        decrypted_c = chr(ord(c) - ord(key_c) % 256)
        decrypted.append(decrypted_c)
    return ''.join(decrypted)

# Password manager functions
def load_passwords(master_key):
    passwords = {"social media": {}, "email": {}, "other": {}}
    try:
        if os.path.exists(PASSWORD_FILE):
            with open(PASSWORD_FILE, 'r') as file:
                for line in file:
                    if line.strip():
                        try:
                            encrypted_category, encrypted_name, encrypted_data = line.strip().split('|')
                            category = simple_decrypt(encrypted_category, master_key)
                            name = simple_decrypt(encrypted_name, master_key)
                            data = simple_decrypt(encrypted_data, master_key)
                            passwords[category][name] = json.loads(data)
                        except Exception as e:
                            print(f"Error decrypting line: {e}")
                            continue
    except Exception as e:
        print(f"Error loading passwords: {e}")
    return passwords

def save_passwords(master_key, passwords):
    try:
        with open(PASSWORD_FILE, 'w') as file:
            for category in passwords:
                for name in passwords[category]:
                    data = json.dumps(passwords[category][name])
                    encrypted_category = simple_encrypt(category, master_key)
                    encrypted_name = simple_encrypt(name, master_key)
                    encrypted_data = simple_encrypt(data, master_key)
                    file.write(f"{encrypted_category}|{encrypted_name}|{encrypted_data}\n")
    except Exception as e:
        print(f"Error saving passwords: {e}")

def verify_master_key():
    """Verify or create master key"""
    if os.path.exists(MASTER_KEY_FILE):
        with open(MASTER_KEY_FILE, 'r') as f:
            stored_hash = f.read().strip()
        return stored_hash
    return None

def create_master_key(key):
    """Create a new master key"""
    with open(MASTER_KEY_FILE, 'w') as f:
        f.write(hashlib.sha256(key.encode()).hexdigest())

# Celebration page generator
def generate_celebration_page(name, age, birthday, theme):
    themes = {
        "balloons": {
            "bg_color": "#ffffff",
            "text_color": "#000000",
            "accent_color": "#bb86fc",
            "animation": "balloonAnimation"
        },
        "confetti": {
            "bg_color": "#ffffff",
            "text_color": "#000000",
            "accent_color": "#03dac6",
            "animation": "confettiAnimation"
        },
        "stars": {
            "bg_color": "#ffffff",
            "text_color": "#000000",
            "accent_color": "#ff8906",
            "animation": "starsAnimation"
        }
    }
    
    selected_theme = themes.get(theme, themes["balloons"])
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Happy Birthday {name}!</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Arial', sans-serif;
            background-color: {selected_theme['bg_color']};
            color: {selected_theme['text_color']};
            text-align: center;
            overflow-x: hidden;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            position: relative;
            z-index: 1;
        }}
        h1 {{
            font-size: 3rem;
            margin-bottom: 1rem;
            color: {selected_theme['accent_color']};
        }}
        p {{
            font-size: 1.5rem;
            margin-bottom: 2rem;
        }}
        .birthday-info {{
            background: rgba(0, 0, 0, 0.05);
            padding: 1.5rem;
            border-radius: 10px;
            margin: 2rem 0;
            backdrop-filter: blur(5px);
        }}
        .cake {{
            font-size: 5rem;
            margin: 2rem 0;
            animation: bounce 2s infinite;
        }}
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-20px); }}
        }}
        canvas {{
            position: fixed;
            top: 0;
            left: 0;
            z-index: 0;
        }}
    </style>
</head>
<body>
    <canvas id="animation"></canvas>
    <div class="container" data-aos="fade-up">
        <h1>🎉 Happy {age}th Birthday, {name}! 🎉</h1>
        <div class="birthday-info" data-aos="fade-up" data-aos-delay="200">
            <p>Born on: {birthday}</p>
            <p>Today is your special day!</p>
        </div>
        <div class="cake" data-aos="zoom-in">🎂</div>
        <p data-aos="fade-up" data-aos-delay="400">Wishing you a fantastic celebration!</p>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>
    <script>
        AOS.init({{
            duration: 800,
            easing: 'ease-in-out',
            once: true
        }});
        
        // Animation script
        const canvas = document.getElementById('animation');
        const ctx = canvas.getContext('2d');
        
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        window.addEventListener('resize', () => {{
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }});
        
        {get_animation_script(selected_theme['animation'])}
    </script>
</body>
</html>
"""
    
    filename = f"celebration_{name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.html"
    filepath = os.path.join(CELEBRATION_PAGES_DIR, filename)
    
    with open(filepath, 'w') as f:
        f.write(html)
    
    return filename

def get_animation_script(animation_type):
    if animation_type == "balloonAnimation":
        return """
        // Balloon animation
        class Balloon {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = canvas.height + 100;
                this.radius = 20 + Math.random() * 30;
                this.speed = 1 + Math.random() * 3;
                this.color = `hsl(${Math.random() * 360}, 70%, 60%)`;
                this.angle = Math.random() * Math.PI * 2;
                this.swing = Math.random() * 0.1;
            }
            
            update() {
                this.y -= this.speed;
                this.x += Math.sin(this.angle) * 2;
                this.angle += this.swing;
                
                if (this.y < -100) {
                    this.y = canvas.height + 100;
                    this.x = Math.random() * canvas.width;
                }
            }
            
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                ctx.fill();
                
                // Balloon string
                ctx.beginPath();
                ctx.moveTo(this.x, this.y + this.radius);
                ctx.lineTo(this.x + Math.sin(this.angle) * 10, this.y + this.radius + 30);
                ctx.strokeStyle = '#000000';
                ctx.lineWidth = 1;
                ctx.stroke();
            }
        }
        
        const balloons = [];
        for (let i = 0; i < 20; i++) {
            balloons.push(new Balloon());
        }
        
        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            balloons.forEach(balloon => {
                balloon.update();
                balloon.draw();
            });
            
            requestAnimationFrame(animate);
        }
        
        animate();
        """
    elif animation_type == "confettiAnimation":
        return """
        // Confetti animation
        class Confetti {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * -canvas.height;
                this.size = Math.random() * 10 + 5;
                this.color = `hsl(${Math.random() * 360}, 80%, 60%)`;
                this.speed = Math.random() * 3 + 2;
                this.angle = Math.random() * Math.PI * 2;
                this.rotation = Math.random() * 0.2 - 0.1;
                this.rotationSpeed = Math.random() * 0.1 - 0.05;
                this.shape = Math.random() > 0.5 ? 'square' : 'circle';
            }
            
            update() {
                this.y += this.speed;
                this.x += Math.sin(this.angle) * 2;
                this.angle += 0.1;
                this.rotation += this.rotationSpeed;
                
                if (this.y > canvas.height) {
                    this.y = Math.random() * -50;
                    this.x = Math.random() * canvas.width;
                }
            }
            
            draw() {
                ctx.save();
                ctx.translate(this.x, this.y);
                ctx.rotate(this.rotation);
                
                ctx.fillStyle = this.color;
                
                if (this.shape === 'square') {
                    ctx.fillRect(-this.size/2, -this.size/2, this.size, this.size);
                } else {
                    ctx.beginPath();
                    ctx.arc(0, 0, this.size/2, 0, Math.PI * 2);
                    ctx.fill();
                }
                
                ctx.restore();
            }
        }
        
        const confetti = [];
        for (let i = 0; i < 100; i++) {
            confetti.push(new Confetti());
        }
        
        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            confetti.forEach(particle => {
                particle.update();
                particle.draw();
            });
            
            requestAnimationFrame(animate);
        }
        
        animate();
        """
    else:  # starsAnimation
        return """
        // Stars animation
        class Star {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 3;
                this.color = '#000000';
                this.speed = Math.random() * 0.5;
                this.opacity = Math.random();
                this.direction = Math.random() > 0.5 ? 1 : -1;
            }
            
            update() {
                this.y -= this.speed;
                this.x += Math.sin(this.y * 0.01) * this.direction * 0.5;
                this.opacity += (Math.random() - 0.5) * 0.05;
                this.opacity = Math.max(0.2, Math.min(1, this.opacity));
                
                if (this.y < 0) {
                    this.y = canvas.height;
                    this.x = Math.random() * canvas.width;
                }
            }
            
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(0, 0, 0, ${this.opacity})`;
                ctx.fill();
                
                // Add a glow effect
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size * 2, 0, Math.PI * 2);
                const gradient = ctx.createRadialGradient(
                    this.x, this.y, 0, 
                    this.x, this.y, this.size * 2
                );
                gradient.addColorStop(0, `rgba(0, 0, 0, ${this.opacity * 0.3})`);
                gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
                ctx.fillStyle = gradient;
                ctx.fill();
            }
        }
        
        const stars = [];
        for (let i = 0; i < 200; i++) {
            stars.push(new Star());
        }
        
        function animate() {
            ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            stars.forEach(star => {
                star.update();
                star.draw();
            });
            
            requestAnimationFrame(animate);
        }
        
        animate();
        """

# Routes
@app.route('/')
def index():
    if 'master_key' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    stored_hash = verify_master_key()
    
    if request.method == 'POST':
        master_key = request.form.get('master_key')
        
        if not stored_hash:
            # Create new master key
            confirm_key = request.form.get('confirm_key')
            if master_key == confirm_key and len(master_key) >= 8:
                create_master_key(master_key)
                session['master_key'] = master_key
                return redirect(url_for('dashboard'))
            else:
                error = "Keys don't match or are too short (min 8 characters)" if master_key != confirm_key else "Master key must be at least 8 characters"
                return render_template('login.html', error=error, is_new=True)
        else:
            # Verify existing key
            if hashlib.sha256(master_key.encode()).hexdigest() == stored_hash:
                session['master_key'] = master_key
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error="Incorrect master key", is_new=False)
    
    return render_template('login.html', is_new=(not stored_hash))

@app.route('/dashboard')
def dashboard():
    if 'master_key' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html')

@app.route('/passwords')
def view_passwords():
    if 'master_key' not in session:
        return redirect(url_for('login'))
    
    category = request.args.get('category', 'social media')
    passwords = load_passwords(session['master_key'])
    
    return render_template('passwords.html', 
                         passwords=passwords[category], 
                         category=category,
                         categories=['social media', 'email', 'other'])

@app.route('/password/<category>/<name>')
def view_password(category, name):
    if 'master_key' not in session:
        return redirect(url_for('login'))
    
    passwords = load_passwords(session['master_key'])
    account = passwords[category].get(name)
    
    if not account:
        return redirect(url_for('view_passwords', category=category))
    
    return render_template('password_detail.html', 
                         account=account, 
                         name=name, 
                         category=category)

@app.route('/add_password', methods=['GET', 'POST'])
def add_password():
    if 'master_key' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        category = request.form.get('category')
        name = request.form.get('name')
        platform = request.form.get('platform')
        password = request.form.get('password')
        
        # Collect credentials
        credentials = {}
        cred_types = request.form.getlist('cred_type[]')
        cred_values = request.form.getlist('cred_value[]')
        
        for t, v in zip(cred_types, cred_values):
            if t and v:
                credentials[t] = v
        
        if name and password and category:
            passwords = load_passwords(session['master_key'])
            passwords[category][name] = {
                'platform': platform,
                'credentials': credentials,
                'password': password
            }
            save_passwords(session['master_key'], passwords)
            return redirect(url_for('view_passwords', category=category))
    
    return render_template('add_password.html')

@app.route('/celebrate', methods=['GET', 'POST'])
def celebrate():
    if 'master_key' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        birthday = request.form.get('birthday')
        theme = request.form.get('theme', 'balloons')
        
        if name and age and birthday:
            filename = generate_celebration_page(name, age, birthday, theme)
            return redirect(url_for('view_celebration', filename=filename))
    
    return render_template('celebrate.html')

@app.route('/celebration/<filename>')
def view_celebration(filename):
    return send_from_directory(CELEBRATION_PAGES_DIR, filename)

@app.route('/logout')
def logout():
    session.pop('master_key', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
