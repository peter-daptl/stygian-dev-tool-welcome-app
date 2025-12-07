#!/usr/bin/env python3
"""
Modern Developer Environment Setup App
Requires: customtkinter, pyyaml, pillow (see requirements.txt)
"""

import sys
import os

# Check for required dependencies
try:
    import customtkinter as ctk
    from customtkinter import CTkFont
    import yaml
    from tkinter import filedialog, messagebox
    from PIL import Image
except ImportError as e:
    missing = str(e).split("'")[1] if "'" in str(e) else str(e)
    print(f"Error: Missing dependency: {missing}")
    print("\nTo install dependencies:")
    print("  Option 1 (with venv - recommended):")
    print("    python3 -m venv venv")
    print("    source venv/bin/activate")
    print("    pip install -r requirements.txt")
    print("\n  Option 2 (system-wide - newer Ubuntu may block):")
    print("    pip install --user customtkinter pyyaml pillow")
    print("\n  Option 3 (if installed via setup script):")
    print("    /opt/welcome-app/venv/bin/python3 /opt/welcome-app/welcome_app_modern.py")
    sys.exit(1)

import subprocess
import configparser
import urllib.request
import urllib.error

# --- Configuration ---
CONFIG_FILE = 'config.yaml'
SETTINGS_FILE = 'user_settings.ini'
GITHUB_CONFIG_URL = 'https://raw.githubusercontent.com/peter-daptl/stygian-dev-tool-welcome-app/main/config.yaml'

# Set appearance
ctk.set_appearance_mode("dark")
script_dir = os.path.dirname(os.path.abspath(__file__))
theme_path = os.path.join(script_dir, "stygian_theme.json")

class ModernWelcomeApp:
    
    def __init__(self, master):
        """Initializes the main application window and loads configuration."""
        self.master = master
        self.master.geometry("1280x720")
        self.master.title("Developer Environment Setup")
        
        # Set minimum window size
        self.master.minsize(1000, 600)
        
        self.options = {}  # Dictionary to store IntVar for each option
        self.script_content = ""

        # Update config from GitHub before loading
        self._update_config_from_github()

        # Load application and user settings
        self.config = self._load_config()
        self.user_settings = self._load_user_settings()

        if not self.config:
            self._show_error("Configuration Error", f"Could not load or parse {CONFIG_FILE}.")
            return

        # Check for "Do not show again" setting
        if self.user_settings.getboolean('General', 'hide_on_startup', fallback=False):
            print("Auto-hiding app as 'hide_on_startup' is enabled in user settings.")
            self.master.withdraw()
            self.master.after(100, self.master.quit)
            return

        # Define fonts
        self.GLOBAL_APP_FONT = CTkFont(
            family="Fira Code",
            size=12,
            weight="normal"
        )
        
        self.TITLE_FONT = CTkFont(
            family="Fira Code",
            size=28,
            weight="bold"
        )

        self.SUB_TITLE_FONT = CTkFont(
            family="Fira Code",
            size=18,
            weight="bold"
        )
        
        self.HEADING_FONT = CTkFont(
            family="Fira Code",
            size=18,
            weight="bold"
        )
        
        self.BUTTON_FONT = CTkFont(
            family="Fira Code",
            size=13,
            weight="bold"
        )
        
        self.CODE_FONT = CTkFont(
            family="Fira Code",
            size=10,
            weight="normal"
        )

        self._create_widgets()

    def _update_config_from_github(self):
        """Downloads the latest config.yaml from GitHub."""
        try:
            print("Checking for config updates from GitHub...")
            script_dir = os.path.dirname(os.path.abspath(__file__))
            local_config = os.path.join(script_dir, CONFIG_FILE)
            
            # Download with timeout
            req = urllib.request.Request(
                GITHUB_CONFIG_URL,
                headers={'User-Agent': 'Stygian-OS-Welcome-App'}
            )
            
            with urllib.request.urlopen(req, timeout=5) as response:
                content = response.read()
                
                # Write to file
                with open(local_config, 'wb') as f:
                    f.write(content)
                
                print("✓ Config updated successfully from GitHub")
                
        except urllib.error.URLError as e:
            print(f"⚠ Could not fetch config from GitHub: {e}")
            print("  Using local config.yaml")
        except Exception as e:
            print(f"⚠ Error updating config: {e}")
            print("  Using local config.yaml")

    def _load_config(self):
        """Loads and parses the YAML configuration file."""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(script_dir, CONFIG_FILE)
            
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            self._show_error("File Not Found", f"Configuration file '{CONFIG_FILE}' not found.")
            return None
        except yaml.YAMLError as e:
            self._show_error("YAML Error", f"Error parsing YAML file: {e}")
            return None
        except Exception as e:
            self._show_error("Error", f"An unexpected error occurred: {e}")
            return None

    def _load_user_settings(self):
        """Loads persistent user settings using configparser."""
        settings = configparser.ConfigParser()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        settings_path = os.path.join(script_dir, SETTINGS_FILE)
        settings.read(settings_path)
        return settings

    def _save_user_settings(self):
        """Saves persistent user settings."""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            settings_path = os.path.join(script_dir, SETTINGS_FILE)
            with open(settings_path, 'w') as configfile:
                self.user_settings.write(configfile)
        except Exception as e:
            print(f"Warning: Could not save user settings. Error: {e}")

    def _show_error(self, title, message):
        """Displays a modal error box."""
        messagebox.showerror(title, message)
        if title in ["Configuration Error", "File Not Found"]:
            sys.exit(1)

    def _create_widgets(self):
        """Sets up the main GUI layout."""
        # Main container with grid layout
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

        # Tabview (no font parameter - it uses theme font)
        self.tabview = ctk.CTkTabview(self.master)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Create tabs
        self.welcome_tab = self.tabview.add("Welcome")
        
        # Category tabs
        self.category_tabs = {}
        for category in self.config.get('categories', []):
            tab_name = category['name']
            self.category_tabs[tab_name] = self.tabview.add(tab_name)
            self._create_category_content(self.category_tabs[tab_name], category)

        self.actions_tab = self.tabview.add("Generate Script")
        
        # Populate tabs
        self._create_welcome_content()
        self._create_actions_content()

        tab_font = CTkFont(family="Fira Code", size=11, weight="normal")
        for button in self.tabview._segmented_button._buttons_dict.values():
            button.configure(font=tab_font)

        # Bind closing event
        self.master.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _on_closing(self):
        """Handles application closure and saves settings."""
        if hasattr(self, 'hide_on_startup_var'):
            hide_state = self.hide_on_startup_var.get()
            if 'General' not in self.user_settings:
                self.user_settings['General'] = {}
            self.user_settings['General']['hide_on_startup'] = str(hide_state)
            self._save_user_settings()
        self.master.destroy()

    def _create_welcome_content(self):
        """Creates the welcome tab content."""
        # Title with brass accent
        title_frame = ctk.CTkFrame(self.welcome_tab, fg_color="transparent")
        title_frame.pack(pady=(30, 10))

        logo_loaded = False
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.join(script_dir, "logo.png")
            
            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path)
                logo_photo = ctk.CTkImage(
                    light_image=logo_img,
                    dark_image=logo_img,
                    size=(128, 128)
                )
                
                logo_label = ctk.CTkLabel(
                    self.welcome_tab,
                    image=logo_photo,
                    text=""
                )
                logo_label.place(x=20, y=10)
                
                # Keep reference
                self.logo_ref = logo_photo
        except Exception as e:
            print(f"Could not load logo: {e}")
        
        title = ctk.CTkLabel(
            title_frame,
            text=self.config.get('app_name', 'Welcome'),
            font=self.TITLE_FONT,
            text_color="#d4a017"
        )
        title.pack()

        subtitle = ctk.CTkLabel(
            self.welcome_tab,
            text=self.config.get('subtitle', 'Subtitle'),
            font=self.SUB_TITLE_FONT,
            text_color="#d4a017"
        )
        subtitle.pack()

        # Version
        version = ctk.CTkLabel(
            self.welcome_tab,
            text=f"Version {self.config.get('app_version', 'N/A')}",
            font=self.GLOBAL_APP_FONT,
            text_color="#8a8a8a"
        )
        version.pack(pady=(0, 20))

        # Info box with better contrast
        info_frame = ctk.CTkFrame(self.welcome_tab, corner_radius=10)
        info_frame.pack(padx=30, pady=10, fill="both", expand=True)

        intro_text = """Welcome to Stygian OS Developer Setup!

This tool helps you customize your development environment by generating an installation script tailored to your needs.

How to use:
1. Browse the category tabs and select the tools you want
2. Navigate to the 'Generate Script' tab
3. Click 'Generate Script' to create your custom installer
4. Save it for later or run it immediately

Manual execution:
   chmod +x install.sh
   sudo -E ./install.sh

⚠️ Important Notes:
- Stygian OS avoids snap packages in favor of native apt repositories
- Some tools (Homebrew, Rust, Poetry) install to your user account, not system-wide
- Always review the generated script before execution
- The script handles conflicts with pre-installed software
- Package versions may vary; not all combinations are extensively tested
- Config automatically updates from GitHub on each launch

This utility streamlines your path to a production-ready development environment with minimal manual configuration."""

        info_textbox = ctk.CTkTextbox(
            info_frame,
            wrap="word",
            font=CTkFont(family="Fira Code", size=14, weight="normal")
        )
        info_textbox.pack(padx=20, pady=20, fill="both", expand=True)
        info_textbox.insert("0.0", intro_text)
        info_textbox.configure(state="disabled")

        # Buttons
        button_frame = ctk.CTkFrame(self.welcome_tab, fg_color="transparent")
        button_frame.pack(pady=20)

        clear_btn = ctk.CTkButton(
            button_frame,
            text="Clear All Selections",
            command=self._clear_all,
            width=220,
            height=45,
            font=self.BUTTON_FONT
        )
        clear_btn.pack(pady=8)

        # Hide on startup checkbox
        self.hide_on_startup_var = ctk.IntVar(
            value=self.user_settings.getboolean('General', 'hide_on_startup', fallback=False)
        )
        hide_cb = ctk.CTkCheckBox(
            self.welcome_tab,
            text="Don't show this app on startup",
            variable=self.hide_on_startup_var,
            command=self._on_hide_checkbox_click,
            font=self.GLOBAL_APP_FONT
        )
        hide_cb.pack(pady=20)

    def _on_hide_checkbox_click(self):
        """Called when the 'Do not show again' checkbox is toggled."""
        state = self.hide_on_startup_var.get()
        if state == 1:
            messagebox.showinfo(
                "Preference Set",
                "This app will hide automatically on next launch.\n"
                "Delete 'user_settings.ini' to show it again."
            )
        else:
            messagebox.showinfo("Preference Cleared", "The app will show on next launch.")

    def _create_category_content(self, parent, category_data):
        """Creates content for a category tab."""
        # Description header
        desc_frame = ctk.CTkFrame(parent, fg_color="transparent")
        desc_frame.pack(padx=20, pady=(15, 10), fill="x")
        
        desc = ctk.CTkLabel(
            desc_frame,
            text=category_data.get('description', ''),
            font=CTkFont(family="Fira Code", size=12, slant="italic"),
            wraplength=1100,
            text_color="#8a8a8a"
        )
        desc.pack(anchor="w")

        # Scrollable frame for options
        scrollable = ctk.CTkScrollableFrame(parent, label_text="")
        scrollable.pack(padx=20, pady=10, fill="both", expand=True)

        # Create checkboxes with better spacing
        for option in category_data.get('options', []):
            opt_id = option['id']
            self.options[opt_id] = ctk.IntVar(value=0)

            cb = ctk.CTkCheckBox(
                scrollable,
                text=option['label'],
                variable=self.options[opt_id],
                font=self.GLOBAL_APP_FONT,
                checkbox_width=22,
                checkbox_height=22
            )
            cb.pack(pady=6, padx=15, anchor="w")

    def _create_actions_content(self):
        """Creates the actions/generate tab content."""
        # Title
        title = ctk.CTkLabel(
            self.actions_tab,
            text="Generate Installation Script",
            font=self.HEADING_FONT,
            text_color="#d4a017"
        )
        title.pack(pady=(20, 15))

        # Button frame
        button_frame = ctk.CTkFrame(self.actions_tab, fg_color="transparent")
        button_frame.pack(pady=15)

        ctk.CTkButton(
            button_frame,
            text="🔧 Generate Script",
            command=self._generate_script,
            width=210,
            height=55,
            font=self.BUTTON_FONT
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            button_frame,
            text="💾 Save Script",
            command=self._save_script,
            width=180,
            height=55,
            font=self.BUTTON_FONT
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            button_frame,
            text="▶️ Run Script",
            command=self._run_script_in_terminal,
            width=180,
            height=55,
            font=self.BUTTON_FONT,
            fg_color="#2fa572",
            hover_color="#268a5a"
        ).pack(side="left", padx=10)

        # Script output
        output_label = ctk.CTkLabel(
            self.actions_tab,
            text="Generated Script:",
            font=CTkFont(family="Fira Code", size=15, weight="bold")
        )
        output_label.pack(pady=(25, 8), anchor="w", padx=30)

        self.script_textbox = ctk.CTkTextbox(
            self.actions_tab,
            wrap="none",
            font=self.CODE_FONT
        )
        self.script_textbox.pack(padx=30, pady=(0, 25), fill="both", expand=True)

    def _clear_all(self):
        """Clears all selected options."""
        for var in self.options.values():
            var.set(0)
        messagebox.showinfo("Cleared", "All selections have been cleared.")

    def _generate_script(self):
        """Generates the installation script."""
        selected_ids = {opt_id for opt_id, var in self.options.items() if var.get() == 1}

        if not selected_ids:
            messagebox.showwarning("No Selection", "Please select at least one tool to install.")
            return

        lines = []
        lines.append("#!/usr/bin/env bash")
        lines.append("# Generated by Stygian OS Developer Environment Setup App")
        lines.append("# Handles conflicts with existing installations")
        lines.append("# Avoids snap packages, uses apt repositories")
        lines.append("set -e")
        lines.append("")
        lines.append("# Sudo check")
        lines.append('if [ "$(id -u)" != "0" ]; then')
        lines.append('  echo "Please run as root: sudo -E $0"')
        lines.append('  exit 1')
        lines.append('fi')
        lines.append("")
        lines.append("# Capture the actual user (not root)")
        lines.append('SUDO_USER=${SUDO_USER:-$USER}')
        lines.append('export DEBIAN_FRONTEND=noninteractive')
        lines.append("")
        lines.append('echo "Starting system update..."')
        lines.append('apt update')
        lines.append('apt install -y apt-transport-https ca-certificates gnupg lsb-release curl wget software-properties-common python3 python3-venv unzip zip')
        lines.append("")
        lines.append("#" * 70)

        for category in self.config.get('categories', []):
            lines.append(f"\n# --- {category['name']} ---")
            for option in category.get('options', []):
                if option['id'] in selected_ids:
                    lines.append(f"\necho 'Installing: {option['label']}...'")
                    script_content = option['script'].strip()
                    lines.append(script_content)

        lines.append("\n" + "#" * 70)
        lines.append("# Cleanup")
        lines.append("echo 'Running cleanup...'")
        lines.append("apt autoremove -y")
        lines.append("apt clean")
        lines.append("")
        lines.append('echo "Installation complete! Please restart your terminal or log out and back in."')

        self.script_content = "\n".join(lines)
        self.script_textbox.delete("0.0", "end")
        self.script_textbox.insert("0.0", self.script_content)

        # Switch to actions tab
        self.tabview.set("Generate Script")
        messagebox.showinfo("Generated", "Script generated successfully!")

    def _save_script(self):
        """Saves the generated script to a file."""
        if not self.script_content:
            self._generate_script()
            if not self.script_content:
                return

        filename = filedialog.asksaveasfilename(
            defaultextension=".sh",
            filetypes=[("Shell Scripts", "*.sh"), ("All Files", "*.*")],
            initialfile="install-dev-env.sh"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.script_content)
                os.chmod(filename, 0o755)
                messagebox.showinfo("Success", f"Script saved to:\n{filename}\n\nRun with: sudo -E {filename}")
            except Exception as e:
                self._show_error("Save Error", f"Failed to save script: {e}")

    def _run_script_in_terminal(self):
        """Runs the script in a new terminal window."""
        if not self.script_content:
            self._generate_script()
            if not self.script_content:
                return

        try:
            temp_script_path = "/tmp/install_dev_env.sh"
            with open(temp_script_path, 'w') as f:
                f.write(self.script_content)
            os.chmod(temp_script_path, 0o755)

            command = f'sudo -E "{temp_script_path}"'
            
            terminal_cmds = [
                f'gnome-terminal -- /bin/bash -c "{command}; echo; echo Press ENTER to exit; read"',
                f'konsole -e /bin/bash -c "{command}; echo; echo Press ENTER to exit; read"',
                f'xfce4-terminal -e "/bin/bash -c \'{command}; echo; echo Press ENTER to exit; read\'"',
                f'lxterminal -e "/bin/bash -c \'{command}; echo; echo Press ENTER to exit; read\'"',
                f'xterm -e /bin/bash -c "{command}; echo; echo Press ENTER to exit; read"'
            ]
            
            launched = False
            for cmd in terminal_cmds:
                terminal_name = cmd.split()[0]
                if subprocess.run(f'which {terminal_name}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                    subprocess.Popen(cmd, shell=True)
                    launched = True
                    break

            if not launched:
                messagebox.showerror(
                    "Error",
                    "Could not find a terminal emulator.\n"
                    f"Please save the script and run manually:\nsudo -E {temp_script_path}"
                )
                return

            messagebox.showinfo(
                "Running",
                "Installation script launched in a new terminal.\n"
                "You will be prompted for your sudo password."
            )

        except Exception as e:
            self._show_error("Execution Error", f"Failed to run script: {e}")


def main():
    root = ctk.CTk()
    app = ModernWelcomeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
