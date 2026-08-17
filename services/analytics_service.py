from extensions import db
from models.prediction import Prediction
from sqlalchemy import func


class AnalyticsService:

    @staticmethod
    def rating_distribution():

        result = db.session.query(
            Prediction.rating,
            func.count(Prediction.id)
        ).group_by(
            Prediction.rating
        ).all()

        return result

    @staticmethod
    def top_users(limit=5):

        result = db.session.query(
            Prediction.username,
            func.count(Prediction.id)
        ).group_by(
            Prediction.username
        ).order_by(
            func.count(Prediction.id).desc()
        ).limit(limit).all()

        return result