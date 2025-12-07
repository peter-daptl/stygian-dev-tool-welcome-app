# Stygian OS - Welcome App

**By Developers, For Developers**

A modern, interactive developer environment setup tool for Stygian OS.

Built with assistance from Claude (Anthropic).

---

## 📋 Overview

The Stygian OS Welcome App is an interactive GUI tool that helps developers quickly set up their development environment. Instead of manually installing dozens of tools, users simply select what they need and generate a custom bash installation script.

### ✨ Features

- 🎨 **Beautiful Dark UI** - Custom dark theme with brass/gold accents
- 📦 **70+ Development Tools** - Organized into 10 categories
- 🔧 **Smart Script Generation** - Creates optimized bash scripts with conflict handling
- 🚀 **One-Click Installation** - Generate and run scripts directly from the app
- 💾 **Save & Share** - Export scripts for later use or distribution
- ⚙️ **User Preferences** - Remember settings, hide on startup option
- 🔍 **No Snap Packages** - Uses native apt repositories for better integration

---

## 🛠️ Tool Categories

The app organizes tools into logical categories:

| Category | Tools Included |
|----------|---------------|
| **Dev Tools & Editors** | VS Code, Cursor, Git, Build Essentials, ripgrep, fzf, Homebrew |
| **Containerization** | Docker Engine, Docker Desktop, Portainer |
| **Languages & Runtimes** | Node.js, Python, Rust, Go, PHP, Java |
| **Python Tooling** | pyenv, Poetry, pipx, uv, Ruff |
| **Databases (Servers)** | PostgreSQL, MySQL, MariaDB, MongoDB, Redis |
| **Database GUIs** | DBeaver, pgAdmin, Compass, RedisInsight, Beekeeper Studio |
| **Shell & Utilities** | Zsh, Oh My Zsh, Oh My Bash, CLI utilities, Nerd Fonts |
| **Terminals** | Tilix, Kitty, Alacritty |
| **Web Browsers** | Chrome, Firefox (no snap), Chromium, Brave |
| **VPNs** | WireGuard, OpenVPN, Tailscale, strongSwan |

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Ubuntu/Debian-based Linux distribution
- `pip` package manager

### Method 1: Virtual Environment (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/stygian-os-welcome-app.git
cd stygian-os-welcome-app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python3 welcome_app_modern.py
```

### Method 2: System-wide Installation

```bash
# Install dependencies
pip install customtkinter pyyaml pillow

# Run the app
python3 welcome_app_modern.py
```

### Method 3: System Integration (Optional)

Install to `/opt` for system-wide access:

```bash
sudo mkdir -p /opt/welcome-app
sudo cp -r . /opt/welcome-app/
cd /opt/welcome-app
python3 -m venv venv
sudo ./venv/bin/pip install -r requirements.txt

# Create launcher
sudo tee /usr/local/bin/welcome-app > /dev/null << 'EOF'
#!/bin/bash
/opt/welcome-app/venv/bin/python3 /opt/welcome-app/welcome_app_modern.py
EOF
sudo chmod +x /usr/local/bin/welcome-app

# Run from anywhere
welcome-app
```

---

## 🚀 Usage

### Quick Start

1. **Launch the app:**
   ```bash
   python3 welcome_app_modern.py
   ```

2. **Browse categories:**
   - Click through the category tabs
   - Check boxes next to tools you want

3. **Generate script:**
   - Go to "Generate Script" tab
   - Click "🔧 Generate Script"
   - Review the generated bash script

4. **Install tools:**
   - Option A: Click "▶️ Run Script" (runs in terminal)
   - Option B: Click "💾 Save Script" (save for later)
   - Option C: Copy/paste the script manually

### Running Generated Scripts

Scripts require sudo privileges:

```bash
chmod +x install-dev-env.sh
sudo -E ./install-dev-env.sh
```

The `-E` flag preserves environment variables (important for user-specific installations).

---

## ⚙️ Configuration

### config.yaml

The `config.yaml` file defines all available tools and their installation scripts. You can customize it to:

- Add new tools
- Modify installation commands
- Create custom categories
- Adjust descriptions

Example structure:

```yaml
categories:
  - name: "Your Category"
    description: "Description of tools"
    options:
      - id: "tool-id"
        label: "Tool Name"
        script: |
          apt install -y package-name
```

### stygian_theme.json

Customize the app's appearance by editing color values:

```json
{
  "CTkButton": {
    "fg_color": ["#b8860b", "#b8860b"],
    "hover_color": ["#d4a017", "#d4a017"]
  }
}
```

### user_settings.ini

Automatically created to store user preferences:

```ini
[General]
hide_on_startup = False
```

---

## 🎨 Customization

### Adding Your Logo

Replace `logo.png` with your own logo (recommended size: 128x128px or larger).

### Modifying Colors

Edit `stygian_theme.json` to change:
- Button colors
- Background colors
- Text colors
- Border colors

### Adding Tools

1. Open `config.yaml`
2. Add your tool to the appropriate category:

```yaml
- id: "mytool"
  label: "My Tool"
  script: |
    apt install -y mytool
```

3. Restart the app

---

## 🐛 Troubleshooting

### Dependencies Not Found

```bash
# Ensure pip is updated
pip install --upgrade pip

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### App Won't Start

```bash
# Check Python version (must be 3.8+)
python3 --version

# Run with verbose output
python3 -v welcome_app_modern.py
```

### Script Execution Fails

- Always run with `sudo -E` to preserve environment variables
- Check `/var/log/syslog` for errors
- Ensure internet connection is active
- Verify repository keys are up to date

### Theme Not Loading

```bash
# Verify theme file exists
ls -la stygian_theme.json

# Check file permissions
chmod 644 stygian_theme.json
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Adding Tools

1. Fork the repository
2. Edit `config.yaml` to add your tool
3. Test the installation script
4. Submit a pull request

### Reporting Bugs

Create an issue with:
- Operating system and version
- Python version
- Steps to reproduce
- Error messages or screenshots

### Suggesting Features

Open an issue with the `enhancement` label describing:
- The feature you'd like
- Why it would be useful
- How it might work

---

## 📄 Project Structure

```
stygian-os-welcome-app/
├── welcome_app_modern.py      # Main application
├── config.yaml                # Tool definitions
├── stygian_theme.json         # UI theme
├── requirements.txt           # Python dependencies
├── user_settings.ini          # User preferences (auto-generated)
├── logo.png                   # App logo
├── README.md                  # This file
└── LICENSE                    # License file
```

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.