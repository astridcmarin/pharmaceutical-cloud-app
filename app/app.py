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
    blob = bucket.blob("pharmaceutical_data.csv")

    csv_text = blob.download_as_text()

    drugs = []
    reader = csv.DictReader(io.StringIO(csv_text))

    for drug in reader:
        drugs.append(drug)

    return drugs


def search_drugs(drugs, search_term):
    results = []

    search_term = search_term.strip().lower()

    for drug in drugs:
        if (
            search_term in drug["generic_name"].lower()
            or search_term in drug["brand_name"].lower()
            or search_term in drug["disease"].lower()
            or search_term in drug["drug_class"].lower()
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
            results = search_drugs(drugs, search_term)

    return render_template(
        "index.html",
        results=results,
        search_term=search_term,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)