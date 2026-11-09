import json
import logging
from pathlib import Path

from flask import Flask, request, jsonify, g
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base
from models import ClinicalData
from schemas import ClinicalDataCreate

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Create the SQLite database table
Base.metadata.create_all(bind=engine)

# Create the JSON Lines file location
DATA_FILE = Path("data/clinical_data.jsonl")
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)


def append_to_file(record: dict):
    """Append a clinical record to the JSON Lines file."""
    with DATA_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")


@app.before_request
def create_session():
    """Create a database session for each request."""
    g.db = SessionLocal()


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Close the database session after the request."""
    db: Session = getattr(g, "db", None)
    if db is not None:
        db.close()


@app.route("/clinical/", methods=["POST"])
def create_record():
    """Validate and save a clinical record to both storage files."""
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415

    try:
        payload = request.get_json()
        clinical_data = ClinicalDataCreate.model_validate(payload)
    except ValidationError as exc:
        return jsonify({"error": exc.errors(include_context=False)}), 400
    except Exception:
        return jsonify({"error": "Invalid JSON request"}), 400

    db: Session = g.db

    try:
        db_item = ClinicalData(
            patient_name=clinical_data.patient_name,
            age=clinical_data.age,
            diagnosis=clinical_data.diagnosis,
            patient_id=clinical_data.patient_id,
            blood_type=clinical_data.blood_type,
            treatment=clinical_data.treatment
        )

        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        record = db_item.to_dict()
        append_to_file(record)

        app.logger.info("Created clinical record %s", db_item.id)
        return jsonify(record), 201

    except (SQLAlchemyError, OSError):
        db.rollback()
        app.logger.exception("Failed to save clinical record")
        return jsonify({"error": "Unable to save clinical record"}), 500


@app.route("/clinical/", methods=["GET"])
def read_records():
    """Retrieve all clinical records from SQLite."""
    try:
        records = g.db.query(ClinicalData).all()
        return jsonify([record.to_dict() for record in records]), 200
    except SQLAlchemyError:
        app.logger.exception("Failed to retrieve records")
        return jsonify({"error": "Unable to retrieve records"}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
