from sqlalchemy import Column, Integer, String, DateTime
import datetime
from database import Base


class ClinicalData(Base):
    __tablename__ = "clinical_data"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    diagnosis = Column(String, nullable=False)

    # Three additional patient data columns
    patient_id = Column(String, nullable=False)
    blood_type = Column(String, nullable=False)
    treatment = Column(String, nullable=False)

    recorded_at = Column(
        DateTime,
        default=datetime.datetime.utcnow
    )

    def to_dict(self):
        """Return clinical record as a JSON-compatible dictionary."""
        return {
            "id": self.id,
            "patient_name": self.patient_name,
            "age": self.age,
            "diagnosis": self.diagnosis,
            "patient_id": self.patient_id,
            "blood_type": self.blood_type,
            "treatment": self.treatment,
            "recorded_at": self.recorded_at.isoformat()
        }
