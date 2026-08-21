from datetime import datetime

from extensions import db


class Prediction(db.Model):

    __tablename__ = "predictions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ==========================================
    # USER ID
    # ==========================================

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # ==========================================
    # INPUT FEATURES
    # ==========================================

    reviews = db.Column(
        db.Float,
        nullable=False
    )

    installs = db.Column(
        db.Float,
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    size = db.Column(
        db.Float,
        nullable=False
    )

    # ==========================================
    # PREDICTED RATING
    # ==========================================

    rating = db.Column(
        db.Float,
        nullable=False
    )

    # ==========================================
    # ACTUAL RATING
    # ==========================================

    actual_rating = db.Column(
        db.Float,
        nullable=True
    )

    # ==========================================
    # CREATED TIME
    # ==========================================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # ==========================================
    # RELATIONSHIP
    # ==========================================

    user = db.relationship(
        "User",
        back_populates="predictions"
    )

    # ==========================================
    # HELPER PROPERTY
    # ==========================================

    @property
    def username(self):

        if self.user:

            return self.user.username

        return "Unknown"

    # ==========================================
    # REPRESENTATION
    # ==========================================

    def __repr__(self):

        return (
            f"<Prediction "
            f"id={self.id} "
            f"user_id={self.user_id} "
            f"rating={self.rating}>"
        )