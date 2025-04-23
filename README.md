# 🚗 Vehicle Insurance Premium Prediction - End-to-End MLOps Project

This project demonstrates a **complete MLOps pipeline** for predicting vehicle insurance premiums using advanced tools and technologies like **MongoDB Atlas**, **AWS S3**, **EC2**, **ECR**, **Docker**, **GitHub Actions**, and a robust Python-based backend. It showcases real-world automation, orchestration, and deployment techniques with a focus on scalability and reproducibility.

---
https://github.com/user-attachments/assets/9bc29bba-ae21-41d9-8048-ec5ebcb05265
## 📌 Project Highlights

- ✅ Modular Python Codebase with custom `setup.py` and `pyproject.toml`
- ✅ MongoDB Atlas for cloud-based data storage
- ✅ Custom logging, exception handling, and configuration management
- ✅ End-to-End ML Pipeline:
  - Data Ingestion
  - Data Validation
  - Data Transformation
  - Model Training
  - Model Evaluation
  - Model Pushing
- ✅ Cloud Deployment using:
  - Docker
  - AWS ECR & EC2
  - GitHub Actions (CI/CD)
- ✅ Web App hosted via Flask on EC2 instance

---

## ⚙️ Project Setup

### 1. 📁 Initial Template and Environment Setup
```bash
python template.py  # To generate project structure
conda create -n vehicle python=3.10 -y
conda activate vehicle
pip install -r requirements.txt
pip list  # Verify packages
```
Edit `setup.py` and `pyproject.toml` to use local modules. (More details in `crashcourse.txt`)

---

## 🌐 MongoDB Atlas Setup
1. Sign up at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create Cluster → Setup DB user + Network Access (0.0.0.0/0)
3. Copy the connection string and set `MONGODB_URL` in your environment.
4. Upload dataset to MongoDB using `mongoDB_demo.ipynb`.

---

## 📁 Notebooks, Logging & Exception Handling

- 🧠 EDA and Feature Engineering in Jupyter notebooks
- 📟 Custom logging module for all logs
- ❗ Custom exception module for debugging

---

## 🔄 Data Ingestion to Model Trainer Pipeline

- Define MongoDB config: `configuration.mongo_db_connections.py`
- Setup ingestion logic: `data_access/`, `components/`, `entity/`, `pipeline/`
- Add schema in `config/schema.yaml` for validation
- Add transformers and trainer logic in:
  - `components.data_validation.py`
  - `components.data_transformation.py`
  - `components.model_trainer.py`
  - `entity/estimator.py`

---

## ☁️ AWS Integration

### IAM + AWS CLI
```bash
export AWS_ACCESS_KEY_ID="xxx"
export AWS_SECRET_ACCESS_KEY="xxx"
```

### AWS S3 Setup
- S3 Bucket: `my-model-mlopsproj`
- Key: `model-registry`

Configure S3 interaction in:
- `configuration/aws_connection.py`
- `aws_storage/`
- `entity/s3_estimator.py`

---

## ✅ Model Evaluation & Pushing

- Evaluate and push model to S3 via `model_evaluation.py` and `model_pusher.py`

---

## 🧪 Prediction Pipeline + Flask App

- `app.py`: Main web app
- Routes:
  - `/` - Prediction UI
  - `/training` - Trigger model training
- `templates/` and `static/` added for frontend

---

## 🚀 CI/CD with GitHub Actions + AWS

### Docker Setup
- Create `Dockerfile` and `.dockerignore`

### GitHub Actions
- Setup `.github/workflows/aws.yaml` for CI/CD
- Secrets:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_REGION`
  - `ECR_REPO`

### AWS Resources
- 🐳 **ECR** for storing Docker images
- 💻 **EC2 Ubuntu (t2.medium)** to deploy app

### EC2 Setup
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
```

### Connect GitHub Self-Hosted Runner
- Settings > Actions > Runners > Add Linux Runner
- Follow setup commands on EC2 terminal

---

## 🌍 Final Deployment

- CI/CD auto-triggers on `push to main`
- Activate EC2 port 5080 via Inbound Rules
- Access your app: `http://<EC2-Public-IP>:5080`

---

## 🛠 Tools & Technologies

| Category       | Tools/Services                                    |
|----------------|---------------------------------------------------|
| Programming    | Python 3.10                                       |
| MLOps          | DVC, MLflow, GitHub Actions, Docker               |
| Data Storage   | MongoDB Atlas, AWS S3                             |
| Deployment     | AWS EC2, ECR, IAM                                 |
| Web Framework  | Flask                                             |
| Cloud Platform | Amazon Web Services                               |
| Workflow       | CI/CD via GitHub Actions & Self-hosted Runner     |

---

## 💡 Future Improvements

- Add monitoring with Prometheus + Grafana
- Improve UI with ReactJS or Streamlit
- Integrate model explainability (SHAP)

---

## 🙌 Let's Connect

If you liked the project or have any suggestions, feel free to reach out!

