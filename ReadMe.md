# 🧩 OVPN Patcher

A simple Python utility to automate VPN configuration tasks such as extracting `.ovpn` files, resolving hostnames to IPs, and injecting credentials — making VPN setup seamless for automation or self-hosted environments.

---

## 🚀 Features

- Extracts `.ovpn` configs from ZIP archives  
- Resolves VPN hostnames to IP addresses  
- Injects credentials automatically into config files  
- Ideal for Gluetun or custom VPN automation setups  

---

## 🛠️ Requirements

- **Python 3.8+**
- Internet access (for hostname resolution)
- FastVPN [ZIP archive](https://vpn.ncapi.io/groupedServerList.zip) (or similar `.ovpn` bundle)

---

## ⚙️ Installation

1. **Clone this repository**

   ```bash
   git clone https://github.com/InsafNilam/ovpn-patcher.git
   cd ovpn-patcher
````

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the environment (Windows PowerShell)**

   ```bash
   .\venv\Scripts\Activate.ps1
   ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

Once dependencies are installed, run:

```bash
python main.py
```

The script will:

* Extract all `.ovpn` files from the given ZIP
* Replace domain names with IPs
* Add credentials and save the patched configs

---

## 📁 Output

The processed `.ovpn` files will be saved under an output directory (e.g., `/patched`).

---

## 🧠 Example Use Case

Perfect for automating VPN configurations with:

* **Gluetun Docker containers**
* **Custom torrent setups**
* **Self-hosted media streaming systems**

---

## 🔗 Repository

GitHub: [https://github.com/InsafNilam/ovpn-patcher](https://github.com/InsafNilam/ovpn-patcher)

---

## 📜 License

This project is licensed under the **MIT License** – feel free to use and modify it.

---

**Made with ⚙️ by [Insaf Nilam](https://github.com/InsafNilam)**
