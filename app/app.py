import csv
import io
import os

from flask import Flask, render_template, request
from google.cloud import storage

app = Flask(__name__)


def load_drugs():
    bucket_name = os.environ.get(
        "BUCKET_NAME",
        "pharma-data-explorer-am-data"
    )

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob("neurology_medications.csv")

    csv_text = blob.download_as_text()

    drugs = []
    reader = csv.DictReader(io.StringIO(csv_text))

    for drug in reader:
        drugs.append(drug)

    return drugs

def load_conditions():

    bucket_name = os.environ.get(
        "BUCKET_NAME",
        "pharma-data-explorer-am-data"
    )

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob("neurology_conditions.csv")

    csv_text = blob.download_as_text()

    conditions = []
    reader = csv.DictReader(io.StringIO(csv_text))

    for condition in reader:
        conditions.append(condition)

    return conditions

def enrich_drugs_with_conditions(drugs, conditions):

    condition_lookup = {}

    for condition in conditions:
        condition_name = condition["condition"].strip().lower()
        condition_lookup[condition_name] = condition

    for drug in drugs:
        condition_name = drug["condition"].strip().lower()
        condition_info = condition_lookup.get(condition_name)

        if condition_info:
            drug["condition_summary"] = condition_info["summary"]
            drug["common_symptoms"] = condition_info["common_symptoms"]
        else:
            drug["condition_summary"] = ""
            drug["common_symptoms"] = ""

    return drugs

def search_drugs(drugs, search_term):
    results = []

    search_term = search_term.strip().lower()

    for drug in drugs:
        if (
            search_term in drug["generic_name"].lower()
            or search_term in drug["brand_name"].lower()
            or search_term in drug["condition"].lower()
            or search_term in drug["approved_use"].lower()
            or search_term in drug["drug_class"].lower()
            or search_term in drug["formulations"].lower()
            or search_term in drug["routes"].lower()
            or search_term in drug["common_adverse_effects"].lower()
            or search_term in drug["warnings"].lower()
            or search_term in drug["off_label_uses"].lower()
            or search_term in drug["condition_summary"].lower()
            or search_term in drug["common_symptoms"].lower()
        ):
            results.append(drug)

    return results


@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    search_term = ""

    if request.method == "POST":
        search_term = request.form.get("search_term", "").strip()

        if search_term:
            drugs = load_drugs()
            conditions = load_conditions()
            drugs = enrich_drugs_with_conditions(drugs, conditions)
            results = search_drugs(drugs, search_term)

    return render_template(
        "index.html",
        results=results,
        search_term=search_term,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)