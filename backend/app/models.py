from datetime import datetime
from .extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # "USER" or "ADMIN"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    profile = db.relationship("UserProfile", backref="user", uselist=False, cascade="all, delete-orphan")
    saved_schemes = db.relationship("SavedScheme", backref="user", cascade="all, delete-orphan")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email, "role": self.role}


class UserProfile(db.Model):
    __tablename__ = "user_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)

    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))       # male / female / other
    state = db.Column(db.String(60))
    income = db.Column(db.Integer)          # annual family income in rupees
    occupation = db.Column(db.String(30))   # student / farmer / employed / self-employed / unemployed

    def to_dict(self):
        return {
            "age": self.age,
            "gender": self.gender,
            "state": self.state,
            "income": self.income,
            "occupation": self.occupation,
        }


class Scheme(db.Model):
    __tablename__ = "schemes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    department = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(60), nullable=False)
    benefit = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)

    min_age = db.Column(db.Integer, nullable=True)
    max_age = db.Column(db.Integer, nullable=True)
    max_income = db.Column(db.Integer, nullable=True)

    state = db.Column(db.String(60), default="All India", nullable=False)
    occupation = db.Column(db.String(30), default="any", nullable=False)
    gender = db.Column(db.String(20), default="any", nullable=False)
    senior_only = db.Column(db.Boolean, default=False, nullable=False)

    documents = db.Column(db.Text)  # stored as comma-separated values
    deadline = db.Column(db.String(120), default="Open year-round")
    apply_link = db.Column(db.String(500))

    def documents_list(self):
        return [d.strip() for d in (self.documents or "").split(",") if d.strip()]

    def set_documents_list(self, docs):
        self.documents = ", ".join(d.strip() for d in docs if d and d.strip())

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "category": self.category,
            "benefit": self.benefit,
            "description": self.description,
            "minAge": self.min_age,
            "maxAge": self.max_age,
            "maxIncome": self.max_income,
            "state": self.state,
            "occupation": self.occupation,
            "gender": self.gender,
            "seniorOnly": self.senior_only,
            "documents": self.documents_list(),
            "deadline": self.deadline,
            "applyLink": self.apply_link,
        }


class SavedScheme(db.Model):
    __tablename__ = "saved_schemes"
    __table_args__ = (db.UniqueConstraint("user_id", "scheme_id", name="uq_user_scheme"),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    scheme_id = db.Column(db.Integer, db.ForeignKey("schemes.id"), nullable=False)

    scheme = db.relationship("Scheme")
