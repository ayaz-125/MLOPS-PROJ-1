# Vehicle Data Processing and Model Training Pipeline

## Project Overview
This project involves setting up a complete pipeline for data ingestion, validation, transformation, model training, evaluation, and deployment using MongoDB, AWS, and CI/CD with Docker and GitHub Actions. The following steps provide a structured workflow for the implementation.

---

## 1. Project Setup

### Step 1: Create Project Template
Run the following command to generate the project template:
```bash
python template.py
```

### Step 2: Configure `setup.py` and `pyproject.toml`
Modify these files to import local packages.
More details are available in `crashcourse.txt`.

### Step 3: Setup Virtual Environment
```bash
conda create -n vehicle python=3.10 -y
conda activate vehicle
pip install -r requirements.txt
```

### Step 4: Verify Installed Packages
```bash
pip list
```

---

## 2. MongoDB Setup

### Step 5: Create MongoDB Atlas Account and Cluster
- Sign up for MongoDB Atlas.
- Create a new project and cluster (M0 free tier).
- Set up a database user and password.
- Add `0.0.0.0/0` to Network Access.
- Retrieve the connection string (`mongodb+srv://<username>:<password>@cluster.mongodb.net/`).

### Step 6: Connect MongoDB to Jupyter Notebook
- Create a `notebook` directory.
- Add a dataset to this directory.
- Use `mongoDB_demo.ipynb` to upload data.
- Verify data in MongoDB Atlas under the Database Collections section.

---

## 3. Logging and Exception Handling

### Step 7: Implement Logging and Exception Handling
- Create `logger.py` and `exception.py`.
- Test the setup using `demo.py`.

---

## 4. Data Pipeline Setup

### Step 8: Data Ingestion
- Define MongoDB connection functions in `configuration.mongo_db_connections.py`.
- Fetch and transform data using `data_access/proj1_data.py`.
- Implement `DataIngestionConfig` and `DataIngestionArtifact` classes.
- Run `demo.py` after setting up the MongoDB connection.

```bash
export MONGODB_URL="mongodb+srv://<username>:<password>@cluster.mongodb.net/"
```

### Step 9: Data Validation, Transformation, and Model Training
- Define dataset schema in `config.schema.yaml`.
- Implement validation, transformation, and model training similar to data ingestion.
- Update `estimator.py` for model training.

---

## 5. AWS and S3 Configuration

### Step 10: AWS Setup
- Sign in to AWS and create an IAM user (`firstproj`).
- Attach `AdministratorAccess` policy.
- Generate access keys and set environment variables:
```bash
export AWS_ACCESS_KEY_ID="<your-access-key>"
export AWS_SECRET_ACCESS_KEY="<your-secret-key>"
```
- Create an S3 bucket (`my-model-mlopsproj`).

### Step 11: Implement AWS Connection
- Configure `src.configuration.aws_connection.py` to interact with S3.
- Implement `s3_estimator.py` for managing model storage.

---

## 6. CI/CD Pipeline with Docker and GitHub Actions

### Step 12: Setup Docker and CI/CD
- Create `Dockerfile` and `.dockerignore`.
- Set up GitHub Actions workflow in `.github/workflows/aws.yaml`.
- Create an ECR repository (`vehicleproj`).
- Create an EC2 Ubuntu instance (`vehicledata-machine`).
- Install Docker in EC2:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```
- Configure EC2 as a GitHub self-hosted runner.
- Add GitHub Secrets:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_DEFAULT_REGION`
  - `ECR_REPO`

### Step 13: Deploy Application on EC2
- Allow inbound traffic on port `5080` in EC2 Security Groups.
- Access the app using `http://<EC2-Public-IP>:5080`.

---

## 7. Model Deployment

### Step 14: Model Evaluation and Deployment
- Implement model evaluation logic.
- Deploy trained models via `Model Pusher`.
- Enable model training via `/training` API endpoint.

---

## Summary
This project establishes a complete MLOps pipeline integrating MongoDB, AWS, Docker, and GitHub Actions for automated model training and deployment. The CI/CD workflow ensures seamless integration and delivery.

For any issues, refer to individual module documentation or raise an issue in the repository.