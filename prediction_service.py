# ==========================================
# IMPORT
# ==========================================

from extensions import db

from models.prediction import Prediction
from models.user import User

from sqlalchemy import func


class PredictionService:

    # ==========================================
    # SAVE PREDICTION
    # ==========================================

    @staticmethod
    def save_prediction(
        user_id,
        reviews,
        installs,
        price,
        size,
        rating,
        actual_rating=None
    ):
        """
        Lưu một kết quả dự đoán vào database.
        """

        prediction = Prediction(
            user_id=user_id,
            reviews=reviews,
            installs=installs,
            price=price,
            size=size,
            rating=rating,
            actual_rating=actual_rating
        )

        db.session.add(prediction)
        db.session.commit()

        return prediction

    # ==========================================
    # GET ONE PREDICTION
    # ==========================================

    @staticmethod
    def get_prediction(prediction_id):

        return Prediction.query.get(
            prediction_id
        )

    # ==========================================
    # RECENT PREDICTIONS
    # ==========================================

    @staticmethod
    def get_recent_predictions(
        user_id=None,
        limit=10
    ):
        """
        Lấy các dự đoán gần đây.
        Nếu truyền user_id thì chỉ lấy
        dữ liệu của user đó.
        """

        query = Prediction.query

        if user_id is not None:

            query = query.filter(
                Prediction.user_id == user_id
            )

        return (
            query
            .order_by(
                Prediction.id.desc()
            )
            .limit(limit)
            .all()
        )

    # ==========================================
    # TOTAL PREDICTIONS
    # ==========================================

    @staticmethod
    def get_total_predictions(
        user_id=None
    ):
        """
        Tổng số dự đoán.
        """

        query = Prediction.query

        if user_id is not None:

            query = query.filter(
                Prediction.user_id == user_id
            )

        return query.count()

    # ==========================================
    # AVERAGE RATING
    # ==========================================

    @staticmethod
    def get_average_rating(
        user_id=None
    ):
        """
        Tính rating trung bình.
        """

        query = db.session.query(
            func.avg(
                Prediction.rating
            )
        )

        if user_id is not None:

            query = query.filter(
                Prediction.user_id == user_id
            )

        average = query.scalar()

        if average is None:

            return 0

        return round(
            float(average),
            2
        )

    # ==========================================
    # ACCURACY
    # ==========================================

    @staticmethod
    def get_prediction_accuracy(
        user_id=None
    ):
        """
        Tính độ chính xác nếu có actual_rating.

        Accuracy ở đây được hiểu là tỷ lệ
        dự đoán có sai số <= 0.2.
        """

        query = Prediction.query.filter(
            Prediction.actual_rating.isnot(None)
        )

        if user_id is not None:

            query = query.filter(
                Prediction.user_id == user_id
            )

        predictions = query.all()

        if not predictions:

            return 0

        correct = 0

        for item in predictions:

            difference = abs(
                item.rating
                - item.actual_rating
            )

            if difference <= 0.2:

                correct += 1

        accuracy = (
            correct
            / len(predictions)
        ) * 100

        return round(
            accuracy,
            2
        )

    # ==========================================
    # RATING DISTRIBUTION
    # ==========================================

    @staticmethod
    def get_rating_distribution(
        user_id=None
    ):
        """
        Thống kê số lượng dự đoán
        theo rating.
        """

        query = db.session.query(
            Prediction.rating,
            func.count(
                Prediction.id
            )
        )

        if user_id is not None:

            query = query.filter(
                Prediction.user_id == user_id
            )

        return (
            query
            .group_by(
                Prediction.rating
            )
            .order_by(
                Prediction.rating
            )
            .all()
        )

    # ==========================================
    # TOP USERS
    # ==========================================

    @staticmethod
    def get_top_users(
        limit=5
    ):
        """
        Lấy những người dùng có
        nhiều dự đoán nhất.
        """

        return (
            db.session.query(
                User.username,
                func.count(
                    Prediction.id
                ).label("prediction_count")
            )
            .join(
                Prediction,
                User.id
                == Prediction.user_id
            )
            .group_by(
                User.id,
                User.username
            )
            .order_by(
                func.count(
                    Prediction.id
                ).desc()
            )
            .limit(limit)
            .all()
        )

    # ==========================================
    # PREDICTION TREND
    # ==========================================

    @staticmethod
    def get_prediction_trend(
        user_id=None,
        limit=20
    ):
        """
        Lấy dữ liệu dự đoán theo thời gian.
        """

        query = Prediction.query

        if user_id is not None:

            query = query.filter(
                Prediction.user_id == user_id
            )

        return (
            query
            .order_by(
                Prediction.created_at.asc()
            )
            .limit(limit)
            .all()
        )

    # ==========================================
    # DELETE ONE PREDICTION
    # ==========================================

    @staticmethod
    def delete_prediction(
        prediction_id,
        user_id=None
    ):
        """
        Xóa một prediction.

        Nếu truyền user_id:
        chỉ cho phép user đó xóa dữ liệu
        của chính mình.
        """

        query = Prediction.query.filter_by(
            id=prediction_id
        )

        if user_id is not None:

            query = query.filter(
                Prediction.user_id == user_id
            )

        prediction = query.first()

        if prediction is None:

            return False

        db.session.delete(
            prediction
        )

        db.session.commit()

        return True

    # ==========================================
    # CLEAR HISTORY
    # ==========================================

    @staticmethod
    def clear_history(
        user_id=None
    ):
        """
        Xóa lịch sử.

        Nếu user_id được truyền:
        chỉ xóa lịch sử của user đó.

        Nếu không truyền:
        xóa toàn bộ lịch sử.
        """

        query = Prediction.query

        if user_id is not None:

            query = query.filter(
                Prediction.user_id == user_id
            )

        deleted_count = query.delete(
            synchronize_session=False
        )

        db.session.commit()

        return deleted_count

    # ==========================================
    # SEARCH + PAGINATION
    # ==========================================

    @staticmethod
    def get_predictions_paginated(
        page=1,
        per_page=10,
        keyword="",
        rating="",
        user_id=None
    ):
        """
        Tìm kiếm + phân trang lịch sử dự đoán.
        """

        query = Prediction.query

        # --------------------------------------
        # FILTER USER
        # --------------------------------------

        if user_id is not None:

            query = query.filter(
                Prediction.user_id == user_id
            )

        # --------------------------------------
        # SEARCH USERNAME
        # --------------------------------------

        if keyword:

            query = (
                query
                .join(
                    User,
                    User.id
                    == Prediction.user_id
                )
                .filter(
                    User.username.ilike(
                        f"%{keyword}%"
                    )
                )
            )

        # --------------------------------------
        # FILTER RATING
        # --------------------------------------

        if rating:

            try:

                rating_value = float(
                    rating
                )

                query = query.filter(
                    Prediction.rating
                    >= rating_value
                )

            except ValueError:

                pass

        # --------------------------------------
        # PAGINATION
        # --------------------------------------

        return (
            query
            .order_by(
                Prediction.id.desc()
            )
            .paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
        )