Here are the complete steps to deploy a **Flask + ML model app** on **Google Compute Engine (GCE)** using a full virtual machine (Ubuntu), along with all necessary configuration like Python, Flask, ports, NLTK, etc.

---

# 🚀 Deploy Flask App on Google Compute Engine (VM) — Step-by-Step

---

## ✅ Prerequisites

* Google Cloud account
* Project with **Billing Enabled**
* GCP SDK installed (optional but useful)

---

## 🧱 1. Create a Compute Engine VM

1. Go to [https://console.cloud.google.com/compute](https://console.cloud.google.com/compute)
2. Click **"Create Instance"**
3. Fill the fields:

   * **Name**: `flask-vm`
   * **Region**: choose your preferred region
   * **Machine type**: `e2-micro` (free tier)
   * **Boot disk**: Ubuntu 22.04 LTS
   * **Firewall**: ✅ Allow HTTP & ✅ HTTPS traffic
4. Click **"Create"**

---

## 🔑 2. Connect to the VM via SSH

In the GCP console, click **"SSH"** to open a terminal.

You are now inside your virtual Ubuntu machine.

---

## 🧰 3. Set Up Python Environment

### Update packages:

```bash
sudo apt update && sudo apt upgrade -y
```

### Install Python and pip:

```bash
sudo apt install python3-pip python3-venv -y
```

### Install Git and unzip (optional):

```bash
sudo apt install git unzip -y
```

---

## 🐍 4. Set Up Your Flask App

### Upload your files from local system:

On your local terminal:

```bash
scp -r /path/to/your/flask_app username@EXTERNAL_IP:~
```

Or use **FileZilla** or **WinSCP** for GUI-based file transfers.

---

## 📦 5. Install Flask and Dependencies

### Create and activate virtual environment:

```bash
cd ~/flask_app
python3 -m venv venv
source venv/bin/activate
```

### Install requirements:

```bash
pip install -r requirements.txt
```

If you use NLTK, also install:

```python
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
```

> You can also create a `setup_nltk.py` and run it.

---

## 🔥 6. Run Flask App (With Gunicorn)

Edit your `app.py` to:

```python
app.run(host="0.0.0.0", port=8080)
```

Then run with:

```bash
gunicorn --bind 0.0.0.0:8080 app:app
```

> If not using Gunicorn, use:

```bash
python app.py
```

---

## 🌍 7. Open Firewall Port (If Needed)

GCP only allows ports 80/443 by default.

### Open custom port (e.g., 8080):

```bash
gcloud compute firewall-rules create allow-custom-port \
  --allow tcp:8080 \
  --target-tags flask-vm \
  --description="Allow port 8080" \
  --direction=INGRESS
```

### OR update instance network tags and add rule via UI.

---

## 🌐 8. Access Your App

Visit:

```
http://<EXTERNAL_IP>:8080
```

> Use `gcloud compute instances list` or view the VM's external IP in the console.

---

## ♻️ Optional: Use Systemd for Auto-Start

Create a service file:

```bash
sudo nano /etc/systemd/system/flaskapp.service
```

```ini
[Unit]
Description=Gunicorn instance to serve flaskapp
After=network.target

[Service]
User=your_username
Group=www-data
WorkingDirectory=/home/your_username/flask_app
Environment="PATH=/home/your_username/flask_app/venv/bin"
ExecStart=/home/your_username/flask_app/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8080 app:app

[Install]
WantedBy=multi-user.target
```

Enable it:

```bash
sudo systemctl daemon-reexec
sudo systemctl enable flaskapp
sudo systemctl start flaskapp
```

---

## 🧼 9. (Optional) Point Domain + SSL

Use NGINX + Let's Encrypt to route traffic from domain.com to port 8080 securely.

---

## ✅ Summary: Pros & Cons of GCE

| ✅ Pros                           | ❌ Cons                                  |
| -------------------------------- | --------------------------------------- |
| Full control (like local system) | You manage uptime, ports, etc.          |
| Install anything manually        | Manual scaling, no autoscaling          |
| Ideal for experimentation        | More maintenance vs Cloud Run/AppEngine |

---

Would you like a GitHub-ready `README.md` version of these steps too?

===











Here’s a clean and production-ready `README.md` file with step-by-step instructions for deploying your **Flask + ML app** using **Google Compute Engine (VM)**:

---

```markdown
# 🚀 Deploy Flask + ML App on Google Compute Engine (VM)

This guide walks you through deploying a Flask application with ML models (e.g., `.pkl`, NLTK) on a **Google Compute Engine VM (Ubuntu)**.

---

## 📁 Project Structure

```

flask\_app/
│
├── app.py
├── model.pkl
├── vectorizer.pkl
├── requirements.txt
├── setup\_nltk.py         # optional (for downloading NLTK data)
└── templates/
└── index.html

````

---

## ✅ Prerequisites

- Google Cloud account
- Billing enabled
- Google Cloud project
- Internet connection 😄

---

## 🧱 Step 1: Create Compute Engine VM

1. Visit: https://console.cloud.google.com/compute
2. Click **Create Instance**
3. Settings:
   - **Name**: `flask-vm`
   - **Region**: Choose nearest region
   - **Machine type**: `e2-micro` (free tier)
   - **Boot disk**: Ubuntu 22.04 LTS
   - **Firewall**: ✅ Allow HTTP & HTTPS
4. Click **Create**

---

## 🔐 Step 2: Connect to VM

Click the **SSH** button from the VM instance dashboard.

---

## 📦 Step 3: Install Python & Flask

Run the following in the SSH terminal:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv unzip -y
````

---

## 📁 Step 4: Upload Your App

**Option 1: SCP (Terminal)**

```bash
scp -r flask_app/ username@<EXTERNAL_IP>:~
```

**Option 2: FileZilla / WinSCP (GUI Tool)**

Upload `flask_app/` to `/home/<user>/`

---

## 🐍 Step 5: Set Up Virtual Environment

```bash
cd ~/flask_app
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

If you're using NLTK:

```python
# setup_nltk.py
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
```

Then run:

```bash
python setup_nltk.py
```

---

## 🚦 Step 6: Modify `app.py`

Ensure your Flask app has:

```python
app.run(host="0.0.0.0", port=8080)
```

---

## 🔥 Step 7: Run Flask App

**Option 1: Development (not recommended for production)**

```bash
python app.py
```

**Option 2: Production with Gunicorn**

```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:8080 app:app
```

---

## 🌍 Step 8: (Optional) Open Firewall Port

If not using port 80/443:

```bash
gcloud compute firewall-rules create allow-8080 \
  --allow tcp:8080 \
  --target-tags flask-vm \
  --description="Allow Flask app port"
```

---

## 🌐 Step 9: Access Your App

```text
http://<EXTERNAL_VM_IP>:8080
```

---

## ♻️ Optional: Auto-Start on Boot with systemd

```bash
sudo nano /etc/systemd/system/flaskapp.service
```

Paste the following:

```ini
[Unit]
Description=Flask App with Gunicorn
After=network.target

[Service]
User=<your-username>
Group=www-data
WorkingDirectory=/home/<your-username>/flask_app
Environment="PATH=/home/<your-username>/flask_app/venv/bin"
ExecStart=/home/<your-username>/flask_app/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8080 app:app

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reexec
sudo systemctl enable flaskapp
sudo systemctl start flaskapp
```

---

## ✅ Deployment Done!

You’ve successfully deployed your Flask + ML model app using a **GCE virtual machine**.

---

## ⚖️ Pros vs Cons of GCE

| ✅ Pros                           | ❌ Cons                            |
| -------------------------------- | --------------------------------- |
| Full control like local setup    | Manual security/ports setup       |
| Easily upload files via SSH/SFTP | No autoscaling                    |
| Works with Python, NLTK, OpenCV  | Less suited for high-traffic apps |

---

## 📌 Alternatives

* **Cloud Run** (Serverless, container-based)
* **App Engine** (Easy deployment, scalable)
* **Cloud Functions** (Lambda-like functions)

---

## 📬 Need Help?

Raise an issue or contact me at \[[your-email@example.com](mailto:your-email@example.com)]

---

```

Let me know if you'd also like similar guides for **Cloud Run**, **App Engine**, or **Dockerizing this app**!
```
