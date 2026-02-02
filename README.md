
## 🛠️ Tech Stack

### Backend
- **Python 3.12** - Core programming language
- **Flask 3.0** - Web framework
- **scikit-learn 1.4** - Machine learning library
- **pandas 2.2** - Data manipulation
- **TextBlob 0.17** - Natural language processing

### ML Model
- **Algorithm**: Random Forest Regressor
- **Features**: 11 engineered features
- **Training Data**: 64 LinkedIn posts
- **Accuracy**: R² Score 0.717 on training data

### DevOps
- **Docker & Docker Compose** - Containerization
- **Nginx** - Reverse proxy & load balancer
- **GitHub Actions** - CI/CD pipeline
- **Prometheus** - Monitoring
- **Grafana** - Visualization
- **Terraform** - Infrastructure as Code (optional)
- **Ansible** - Configuration management (optional)

### Infrastructure
- **AWS EC2** - Hosting
- **Ubuntu 22.04** - Operating system

## 📦 Prerequisites

### Local Development
- Python 3.12+
- pip (Python package manager)
- Git

### Docker Deployment
- Docker 20.10+
- Docker Compose 2.0+

### Production Deployment
- AWS EC2 instance (t2.medium or higher recommended)
- Ubuntu 20.04/22.04
- Domain name (optional, for SSL)

## 🚀 Installation

### Method 1: Local Development

**Step 1: Clone the Repository**
```bash
git clone https://github.com/saadkhan024/linkedin-post-predictor.git
cd linkedin-post-predictor

Step 2: Create Virtual Environment
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

Step 3: Install Dependencies

bash
pip install --upgrade pip
pip install -r requirements.txt

Step 4: Download Required Data

Setup Kaggle API:

bash
# Install Kaggle CLI
pip install kaggle

# Create .kaggle directory
mkdir -p ~/.kaggle

# Add your kaggle.json (get from kaggle.com/settings)
# Download from: Kaggle → Settings → API → Create New Token
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

Download dataset:

bash
mkdir -p data
kaggle datasets download -d olagokeblissman/linkedin-post-analytics-data-creator-insights
unzip linkedin-post-analytics-data-creator-insights.zip -d data/
rm linkedin-post-analytics-data-creator-insights.zip

Step 5: Prepare Data and Train Model

bash
# Convert Excel to CSV
python3 << EOF
import pandas as pd
df = pd.read_excel('data/LinkedIn_Post_Analytics_Data.xlsx', sheet_name='Sheet1')
df.to_csv('data/linkedin_posts.csv', index=False)
print("✅ CSV created")
EOF

# Test feature engineering
python3 src/feature_engineering.py

# Train the ML model
python3 src/model_training.py

Step 6: Run the Application

bash
python3 app.py
Access at: http://localhost:5000

Method 2: Docker Deployment
Step 1: Clone Repository
git clone https://github.com/saadkhan024/linkedin-post-predictor.git
cd linkedin-post-predictor

Step 2: Build and Run with Docker Compose

bash
# Build and start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
Step 3: Access Services

Application: http://localhost:5000

Prometheus: http://localhost:9090

Grafana: http://localhost:3000 (admin/admin)

Method 3: Production Deployment on AWS EC2
Step 1: Launch EC2 Instance

AMI: Ubuntu 22.04 LTS

Instance Type: t2.medium (minimum)

Security Group: Allow ports 22, 80, 443, 5000

Step 2: Connect and Setup

bash
# SSH into EC2
ssh -i your-key.pem ubuntu@YOUR_EC2_IP

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io docker-compose git

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu

# Re-login to apply group changes
exit
# SSH back in
Step 3: Deploy Application

bash
# Clone repository
cd /home/ubuntu
git clone https://github.com/saadkhan024/linkedin-post-predictor.git
cd linkedin-post-predictor

# Start services
docker-compose up -d

# Check status
docker-compose ps
Step 4: Configure Nginx (Optional)

bash
# Install Nginx
sudo apt install nginx -y

# Copy Nginx config
sudo cp nginx/nginx.conf /etc/nginx/sites-available/linkedin-predictor
sudo ln -s /etc/nginx/sites-available/linkedin-predictor /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Test and restart
sudo nginx -t
sudo systemctl restart nginx
Access at: http://YOUR_EC2_IP

📖 Usage
Web Interface
1. Analyze Post Text (Recommended)

Navigate to "📝 Analyze Post Text" tab

Paste your LinkedIn post

Click "Analyze My Post"

Get instant score (0-100) and recommendations

2. Predict by Metrics

Navigate to "📊 Predict by Metrics" tab

Select post type (Text, Image, Video, Link, Reel)

Enter expected impressions, reach, clicks

Click "Predict Performance" or "Compare All Types"

CLI Tool
bash
# Activate virtual environment
source venv/bin/activate

# Run CLI predictor
python3 predict_cli.py

# Follow interactive prompts
API Usage
Analyze Text

bash
curl -X POST http://localhost:5000/predict-text \
  -H "Content-Type: application/json" \
  -d '{
    "post_text": "🚀 Just deployed my first CI/CD pipeline!\n\nHere is what I learned:\n1. Automation saves time\n2. Testing is crucial\n\nThoughts? 👇\n\n#DevOps #CICD"
  }'
Predict by Metrics

bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "post_type": "Video",
    "month": "February",
    "impressions": 5000,
    "reach": 6000,
    "clicks": 400
  }'
Compare Post Types

bash
curl -X POST http://localhost:5000/compare \
  -H "Content-Type: application/json" \
  -d '{
    "month": "February",
    "impressions": 5000,
    "reach": 6000,
    "clicks": 400
  }'
Health Check

bash
curl http://localhost:5000/health
