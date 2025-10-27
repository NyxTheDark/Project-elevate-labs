# Educational Keylogger with Encrypted Data Exfiltration

## ⚠️ CRITICAL ETHICAL WARNING ⚠️

**THIS SOFTWARE IS STRICTLY FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY!**

### Legal Notice

Unauthorized use of keylogger software is **ILLEGAL** in most jurisdictions and can result in:
- Criminal prosecution
- Civil lawsuits
- Severe fines and penalties
- Imprisonment

**By using this software, you accept full legal responsibility for your actions.**

### Ethical Requirements

✅ **ONLY USE THIS SOFTWARE IF:**
- You own the computer/device being monitored
- You have explicit written permission from the device owner
- You are conducting authorized security research in a controlled environment
- You are using it for educational demonstration in a cybersecurity course
- You comply with all applicable laws and regulations

❌ **NEVER USE THIS SOFTWARE TO:**
- Capture passwords or sensitive information without consent
- Monitor others without their knowledge or permission
- Steal personal information or credentials
- Violate privacy rights
- Engage in illegal surveillance or hacking activities

---

## Project Overview

This project is an **educational proof-of-concept** keylogger designed for cybersecurity students and professionals to understand:
- How keystroke logging works
- Encryption techniques for data security
- Data exfiltration simulation
- Windows persistence mechanisms
- Kill switch implementation
- Defensive security measures

### Key Features

1. **Keystroke Logging**: Captures keyboard input using the `pynput` library
2. **Fernet Encryption**: Encrypts all logged data using symmetric cryptography
3. **Timestamp Logging**: Records exact time of each keystroke session
4. **Data Exfiltration Simulation**: Simulates sending data to a localhost server
5. **Windows Registry Persistence**: Demonstrates startup persistence (optional)
6. **Kill Switch**: F12 key immediately stops the keylogger
7. **Ethical Constraints**: Built-in warnings and consent mechanisms

---

## System Requirements

### Operating System
- **Primary**: Windows 10/11 (for full functionality including registry persistence)
- **Compatible**: Linux, macOS (limited functionality - no registry persistence)

### Python Version
- Python 3.8 or higher required

### Dependencies
- `pynput`: Keyboard monitoring
- `cryptography`: Fernet encryption
- `pywin32`: Windows registry access (Windows only)

---

## Installation Guide

### Step 1: Clone or Download the Project

```bash
git clone <repository-url>
cd educational-keylogger
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python educational_keylogger.py --help
```

---

## Usage Instructions

### Running the Keylogger

1. **Start the Educational Keylogger**
   ```bash
   python educational_keylogger.py
   ```

2. **Read and Accept Ethical Warning**
   - The program will display ethical guidelines
   - Type "yes" to confirm you understand and accept the terms

3. **Configure Startup Persistence** (Optional)
   - When prompted, choose whether to add registry persistence
   - This demonstrates how malware achieves persistence

4. **Monitoring Active**
   - The keylogger will now capture keystrokes
   - All data is encrypted before storage
   - Press **F12** to activate the kill switch

5. **View Decrypted Logs**
   - After stopping, you can decrypt and view captured data
   - This demonstrates the data that could be compromised

### Running the Exfiltration Server

In a **separate terminal**, start the localhost server:

```bash
python localhost_exfil_server.py
```

- Server runs on `http://localhost:8888`
- Open browser to see status page
- Receives simulated exfiltrated data from keylogger
- All received data is logged with timestamps

---

## Project Architecture

### File Structure

```
educational-keylogger/
│
├── educational_keylogger.py    # Main keylogger implementation
├── localhost_exfil_server.py   # Simulated exfiltration server
├── requirements.txt             # Python dependencies
├── README.md                    # This file
│
├── encrypted_keylog.dat        # Encrypted keystroke logs (generated)
├── encryption.key              # Fernet encryption key (generated)
├── keylogger.log               # Application log file (generated)
└── exfiltrated_data_*.json     # Simulated exfiltration files (generated)
```

### Component Breakdown

#### 1. Keystroke Capture (`pynput`)
- Monitors keyboard events in real-time
- Captures both regular and special keys
- Non-blocking event-driven architecture

#### 2. Encryption Module (`cryptography.fernet`)
- Generates 256-bit encryption keys
- Symmetric encryption for fast operation
- Base64 encoding for safe storage
- Persistent key storage for decryption

#### 3. Data Storage
- JSON format for structured logging
- Timestamp with each session
- Session hash for tracking
- Base64-encoded encrypted entries

#### 4. Exfiltration Simulation
- HTTP POST simulation to localhost
- Encrypted data transmission
- JSON payload with metadata
- File-based simulation (no actual network traffic)

#### 5. Persistence Mechanism (Windows)
- Registry key: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
- Disguised entry name for demonstration
- Automatic startup after reboot
- Clean removal on exit

#### 6. Kill Switch
- F12 key activation
- Immediate logging termination
- Data cleanup before exit
- Registry persistence removal

---

## Technical Implementation Details

### Encryption Process

1. **Key Generation**
   ```python
   key = Fernet.generate_key()  # 256-bit key
   cipher_suite = Fernet(key)
   ```

2. **Data Encryption**
   ```python
   log_entry = {'timestamp': ..., 'keystrokes': ...}
   encrypted_data = cipher_suite.encrypt(json.dumps(log_entry).encode())
   ```

3. **Storage Format**
   ```
   Base64(Encrypted(JSON_data)) + newline
   ```

### Data Exfiltration Simulation

```python
exfiltration_data = {
    'timestamp': datetime.now().isoformat(),
    'data_size': len(encrypted_logs),
    'encrypted_logs': base64.b64encode(encrypted_logs).decode(),
    'source': 'educational_keylogger'
}
```

### Registry Persistence

```python
key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
key_name = "WindowsSecurityUpdate"
winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, script_path)
```

---

## Educational Objectives

### Learning Outcomes

After completing this project, students will understand:

1. **Offensive Security Concepts**
   - How keyloggers capture sensitive data
   - Encryption techniques used by malware
   - Data exfiltration methods
   - Persistence mechanisms

2. **Defensive Security Measures**
   - Detection techniques for keyloggers
   - Endpoint protection strategies
   - Registry monitoring for suspicious entries
   - Network traffic analysis

3. **Ethical Considerations**
   - Legal implications of unauthorized monitoring
   - Privacy rights and compliance
   - Responsible disclosure practices
   - Cybersecurity ethics

### Demonstration Scenarios

#### Scenario 1: Attack Simulation
- Deploy keylogger in controlled VM environment
- Capture sample keystrokes
- Analyze encrypted logs
- Understand attacker perspective

#### Scenario 2: Defense Analysis
- Use endpoint detection tools
- Monitor registry for suspicious entries
- Analyze network traffic patterns
- Implement detection signatures

#### Scenario 3: Incident Response
- Identify keylogger presence
- Safely remove malware
- Analyze captured data
- Implement preventive measures

---

## Security Best Practices

### For Users

1. **Endpoint Protection**
   - Install reputable antivirus software
   - Enable real-time scanning
   - Keep security software updated

2. **Registry Monitoring**
   - Use tools like Autoruns (Sysinternals)
   - Regularly review startup entries
   - Monitor registry changes

3. **Behavioral Analysis**
   - Watch for unusual keyboard lag
   - Monitor for suspicious processes
   - Check network connections

4. **Application Whitelisting**
   - Allow only known applications
   - Block unsigned executables
   - Use Windows AppLocker

### For Organizations

1. **Employee Training**
   - Security awareness programs
   - Phishing simulation exercises
   - Incident reporting procedures

2. **Technical Controls**
   - Endpoint Detection and Response (EDR)
   - Network segmentation
   - Least privilege access
   - Multi-factor authentication

3. **Monitoring and Logging**
   - Centralized log management
   - Security Information and Event Management (SIEM)
   - Regular security audits

---

## Troubleshooting

### Common Issues

#### 1. ImportError: No module named 'pynput'
```bash
pip install pynput cryptography
```

#### 2. Permission denied when accessing registry
- Run as Administrator (Windows)
- Or disable persistence feature

#### 3. Encryption key not found
- The program generates a key on first run
- Ensure write permissions in the directory

#### 4. Server port already in use
```bash
# Change port in localhost_exfil_server.py
start_exfiltration_server(port=9999)
```

---

## Deliverables Checklist

✅ **Main Components**
- [x] Educational keylogger with pynput
- [x] Fernet encryption implementation
- [x] Timestamp logging functionality
- [x] Localhost exfiltration simulation
- [x] Windows registry persistence
- [x] F12 kill switch implementation

✅ **Documentation**
- [x] Comprehensive README with warnings
- [x] Ethical guidelines and legal notices
- [x] Installation instructions
- [x] Usage guide
- [x] Technical implementation details

✅ **Educational Materials**
- [x] Code comments and documentation
- [x] Security best practices
- [x] Learning objectives
- [x] Defensive measures

---

## Project Deliverables for Elavate Labs

### Required Submissions

1. **Source Code**
   - `educational_keylogger.py`
   - `localhost_exfil_server.py`
   - `requirements.txt`

2. **Documentation**
   - This README file
   - Code comments
   - Ethical guidelines

3. **Demonstration Materials**
   - Sample encrypted logs
   - Decryption examples
   - Server simulation output

### Presentation Points

1. **Technical Implementation**
   - Keystroke capture mechanism
   - Encryption process
   - Data exfiltration simulation
   - Persistence techniques

2. **Security Analysis**
   - Attack vectors
   - Detection methods
   - Defensive strategies
   - Mitigation techniques

3. **Ethical Considerations**
   - Legal compliance
   - Responsible use
   - Privacy protection
   - Industry standards

---

## Future Enhancements (Educational)

### Potential Improvements

1. **Advanced Features**
   - Screenshot capture
   - Clipboard monitoring
   - Process injection techniques
   - Network protocol analysis

2. **Detection Evasion**
   - Code obfuscation
   - Anti-debugging techniques
   - Sandbox detection
   - Polymorphic behavior

3. **Communication Channels**
   - DNS tunneling
   - HTTPS exfiltration
   - Steganography
   - Tor network routing

⚠️ **Note**: These enhancements are for educational discussion only!

---

## References and Further Reading

### Books
1. "The Art of Intrusion" by Kevin Mitnick
2. "Penetration Testing" by Georgia Weidman
3. "Practical Malware Analysis" by Michael Sikorski

### Online Resources
1. OWASP Testing Guide
2. MITRE ATT&CK Framework
3. NIST Cybersecurity Framework
4. SANS Cyber Aces

### Related Technologies
- Python pynput documentation
- Cryptography module documentation
- Windows Registry reference
- HTTP protocol specifications

---

## Academic Integrity

This project is designed for educational purposes in cybersecurity courses. If you are submitting this as part of coursework:

1. Ensure you understand every component
2. Be able to explain the technical implementation
3. Discuss ethical implications
4. Cite this project appropriately
5. Follow your institution's academic integrity policies

---

## License and Disclaimer

### Educational Use License

This software is provided "AS IS" for educational purposes only. The authors and contributors:

- Make no warranties about functionality or safety
- Are not responsible for misuse or illegal activities
- Do not endorse unauthorized surveillance
- Encourage responsible and ethical use

### Disclaimer

**Using this software for unauthorized purposes is ILLEGAL and UNETHICAL.**

The creators of this educational project explicitly prohibit and condemn:
- Unauthorized computer access
- Privacy violations
- Data theft
- Surveillance without consent
- Any illegal activities

Users are solely responsible for compliance with all applicable laws.

---

## Contact and Support

### Educational Inquiries

For questions about the educational aspects of this project:
- Review the technical documentation
- Consult cybersecurity textbooks
- Speak with your instructor or mentor
- Join cybersecurity community forums

### Responsible Disclosure

If you discover vulnerabilities in this educational tool:
- Document the issue thoroughly
- Report responsibly
- Suggest improvements
- Contribute to education

---

## Acknowledgments

This educational project was developed to demonstrate:
- Cybersecurity attack techniques
- Defensive security measures
- Ethical considerations in security research
- Responsible disclosure practices

**Remember**: Knowledge is power. Use it responsibly and ethically!

---

## Version History

- **v1.0** (Initial Release)
  - Basic keystroke logging
  - Fernet encryption
  - Localhost exfiltration simulation
  - Registry persistence
  - Kill switch implementation
  - Comprehensive documentation

---

**Final Reminder**: This is an educational tool for cybersecurity professionals and students. Always use responsibly, legally, and ethically!
