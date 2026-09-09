# Pharmaceutical Data Explorer

A cloud-based pharmaceutical data search application built with Python, Flask, Docker, and Google Cloud.

The application allows users to search structured pharmaceutical data by generic name, brand name, disease, or drug class.

## Project Overview

This project was created to practice building and deploying a containerized application using Google Cloud services.

The application reads pharmaceutical data from a private Cloud Storage bucket and serves search results through a Flask web interface deployed on Cloud Run.

## Architecture

User
↓
Cloud Run
↓
Flask / Gunicorn
↓
Dedicated Service Account
↓
IAM
↓
Private Cloud Storage
↓
pharmaceutical_data.csv

## Google Cloud Services

### Cloud Run
Hosts the containerized Flask application and provides the HTTPS endpoint.

### Cloud Storage
Stores the pharmaceutical dataset separately from the application container.

### IAM
Controls access between Cloud Run and Cloud Storage.

The Cloud Run service uses a dedicated service account with:

`roles/storage.objectViewer`

This provides read-only access to objects in the application's Cloud Storage bucket.

### Cloud Build
Builds the application container during source deployment.

### Artifact Registry
Stores the container image used by Cloud Run.

## Technologies

- Python
- Flask
- Gunicorn
- Docker
- Google Cloud Run
- Google Cloud Storage
- Google Cloud IAM
- Google Cloud Build
- Artifact Registry
- Git
- GitHub

## Security

The pharmaceutical dataset is stored in a private Cloud Storage bucket.

The Cloud Run application uses a dedicated service account rather than the project's default Compute Engine service account.

The service account is granted only `roles/storage.objectViewer` on the application bucket, following the principle of least privilege.

No service account keys or application credentials are stored in the repository.

## Data

The dataset used in this project is a small educational pharmaceutical dataset created for cloud-development practice.

It is not intended to function as a validated clinical or drug-information database.

## Local Development

Install dependencies:

```bash
python3 -m pip install -r requirements.txt