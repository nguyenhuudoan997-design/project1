# ==========================================
# IMPORT
# ==========================================

from datetime import datetime

from extensions import db

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


# ==========================================
# USER MODEL
# ==========================================

class User(db.Model):

    __tablename__ = "users"


    # ======================================
    # ID
    # ======================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    # ======================================
    # USERNAME
    # ======================================

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )


    # ======================================
    # PASSWORD
    # ======================================

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )


    # ======================================
    # ROLE
    # ======================================

    role = db.Column(
        db.String(30),
        nullable=False,
        default="User"
    )


    # ======================================
    # CREATED AT
    # ======================================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    # ======================================
    # RELATIONSHIP
    # ======================================

    predictions = db.relationship(
        "Prediction",
        back_populates="user",
        cascade="all, delete-orphan"
    )


    # ======================================
    # SET PASSWORD
    # ======================================

    def set_password(
        self,
        password
    ):

        self.password_hash = (
            generate_password_hash(
                password
            )
        )


    # ======================================
    # CHECK PASSWORD
    # ======================================

    def check_password(
        self,
        password
    ):

        return check_password_hash(
            self.password_hash,
            password
        )


    # ======================================
    # REPRESENTATION
    # ======================================

    def __repr__(self):

        return (
            f"<User "
            f"id={self.id} "
            f"username={self.username} "
            f"role={self.role}>"
        )