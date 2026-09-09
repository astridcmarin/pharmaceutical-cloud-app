# Neurology Pharmaceutical Data Explorer

A cloud-based web application for exploring structured neurology medication and condition data, built with Python, Flask, Docker, and Google Cloud.

The application allows users to search across medication names, brands, neurological conditions, drug classes, formulations, administration routes, adverse effects, warnings, off-label uses, and condition symptoms.

## Project Overview

This project demonstrates the development and deployment of a containerized pharmaceutical data application using Google Cloud.

The application integrates two structured datasets:

- 46 neurology medications
- 9 neurological conditions

Medication records are dynamically associated with condition-level information such as disease summaries and common symptoms.

The application retrieves its datasets from a private Google Cloud Storage bucket and serves searchable results through a Flask web interface deployed on Google Cloud Run.

## Features

- Search by generic or brand name
- Search by neurological condition
- Search by drug class
- Search by formulation or administration route
- Search by adverse effect or warning
- Search by condition symptoms
- Display FDA-approved use information
- Display evidence-reviewed off-label use information
- Display condition summaries and common symptoms
- Display source information and verification dates
- Educational-use disclaimer

## Architecture

```text
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
  ├── neurology_medications.csv
  └── neurology_conditions.csv
```

The Flask application loads both datasets from Cloud Storage and associates medication records with their corresponding neurological condition before processing searches.

## Google Cloud Services

### Cloud Run

Hosts the containerized Flask application and provides the application's HTTPS endpoint.

### Cloud Storage

Stores the medication and condition datasets separately from the application container.

### IAM

Controls access between Cloud Run and Cloud Storage.

The Cloud Run service uses a dedicated service account with:

`roles/storage.objectViewer`

This grants read-only access to objects in the application's Cloud Storage bucket.

### Cloud Build

Builds the application container during source deployment.

### Artifact Registry

Stores the container image used by Cloud Run.

## Technologies

- Python
- Flask
- Gunicorn
- HTML
- CSS
- Docker
- Google Cloud Run
- Google Cloud Storage
- Google Cloud IAM
- Google Cloud Build
- Artifact Registry
- Git
- GitHub

## Data Architecture

### Medication Dataset

`neurology_medications.csv`

Contains structured fields for:

- Generic name
- Brand name
- Condition
- Approved use
- Drug class
- Formulations
- Routes
- Common adverse effects
- Warnings
- Off-label uses
- Source summary
- Last verified date

### Condition Dataset

`neurology_conditions.csv`

Contains:

- Condition
- Summary
- Common symptoms
- Source summary
- Last verified date

The application joins condition information to medication records using the `condition` field.

## Security

The datasets are stored in a private Cloud Storage bucket.

The Cloud Run application uses a dedicated service account rather than the project's default Compute Engine service account.

The service account has read-only `roles/storage.objectViewer` access at the application bucket level, supporting the principle of least privilege.

No service account keys, credentials, or access tokens are stored in the repository.

## Local Development

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the application:

```bash
python3 app/app.py
```

The application runs locally on:

```text
http://127.0.0.1:8080
```

## Deployment

The application is deployed to Google Cloud Run from source.

Cloud Run retrieves the datasets from the private Cloud Storage bucket using the application's dedicated service account.

## Educational Disclaimer

This project is intended for educational and portfolio purposes.

The pharmaceutical and clinical information presented by the application is not intended for clinical decision-making, diagnosis, treatment, prescribing, or medical advice.

Source information and verification dates are maintained within the datasets to document the provenance of the information used by the application.

## Project Goals

This project was developed to practice and demonstrate:

- Python application development
- Working with structured CSV data
- Multi-dataset integration
- Flask web development
- Containerization
- Cloud application deployment
- Cloud Storage integration
- IAM and service-account configuration
- Principle-of-least-privilege access
- Git and GitHub version control
- Troubleshooting across local and cloud environments