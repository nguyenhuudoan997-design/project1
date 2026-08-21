# ============================================================
# SERVICES / PREDICTION SERVICE
# AI Rating Predictor
# ============================================================

from sqlalchemy import func

from extensions import db
from models.prediction import Prediction
from models.user import User


# ============================================================
# PREDICTION SERVICE
# ============================================================

class PredictionService:

    # ========================================================
    # SAVE PREDICTION
    # ========================================================

    @staticmethod
    def save_prediction(
        user_id,
        reviews,
        installs,
        price,
        size,
        rating
    ):
        """
        Lưu một kết quả dự đoán vào database.
        """

        prediction = Prediction(
            user_id=user_id,
            reviews=float(reviews),
            installs=float(installs),
            price=float(price),
            size=float(size),
            rating=float(rating)
        )

        db.session.add(prediction)
        db.session.commit()

        return prediction

    # ========================================================
    # GET TOTAL PREDICTIONS
    # ========================================================

    @staticmethod
    def get_total_predictions(user_id=None):
        """
        Lấy tổng số lượt dự đoán.

        user_id=None:
            Lấy toàn bộ hệ thống.

        user_id=<id>:
            Chỉ lấy dự đoán của user đó.
        """

        query = Prediction.query

        if user_id is not None:
            query = query.filter(
                Prediction.user_id == user_id
            )

        return query.count()

    # ========================================================
    # GET AVERAGE RATING
    # ========================================================

    @staticmethod
    def get_average_rating(user_id=None):
        """
        Lấy Rating trung bình.

        user_id=None:
            Toàn bộ hệ thống.

        user_id=<id>:
            Chỉ tính của user đó.
        """

        query = db.session.query(
            func.avg(Prediction.rating)
        )

        if user_id is not None:
            query = query.filter(
                Prediction.user_id == user_id
            )

        result = query.scalar()

        if result is None:
            return 0.0

        return round(float(result), 2)

    # ========================================================
    # GET PREDICTION ACCURACY
    # ========================================================

    @staticmethod
    def get_prediction_accuracy(user_id=None):
        """
        Tính độ chính xác dự đoán dựa trên actual_rating.

        Accuracy được tính khi database có actual_rating.

        Công thức:

            Accuracy =
            (1 - MAE / 5) * 100

        Nếu chưa có actual_rating:
            trả về 0.0
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
            return 0.0

        total_error = 0.0

        for prediction in predictions:

            predicted = float(
                prediction.rating
            )

            actual = float(
                prediction.actual_rating
            )

            total_error += abs(
                predicted - actual
            )

        mae = (
            total_error /
            len(predictions)
        )

        accuracy = (
            1 - (mae / 5)
        ) * 100

        accuracy = max(
            0.0,
            min(
                100.0,
                accuracy
            )
        )

        return round(
            accuracy,
            2
        )

    # ========================================================
    # GET PAGINATED PREDICTIONS
    # ========================================================

    @staticmethod
    def get_predictions_paginated(
        page=1,
        per_page=10,
        keyword="",
        rating="",
        user_id=None
    ):
        """
        Lấy lịch sử dự đoán có phân trang.

        user_id=None:
            Admin xem toàn bộ lịch sử.

        user_id=<id>:
            User chỉ xem lịch sử của mình.

        keyword:
            Tìm theo username.

        rating:
            Lọc Rating >= giá trị.
        """

        query = Prediction.query

        # ----------------------------------------------------
        # FILTER USER
        # ----------------------------------------------------

        if user_id is not None:

            query = query.filter(
                Prediction.user_id == user_id
            )

        # ----------------------------------------------------
        # SEARCH USERNAME
        # ----------------------------------------------------

        if keyword:

            query = (
                query
                .join(Prediction.user)
                .filter(
                    User.username.ilike(
                        f"%{keyword}%"
                    )
                )
            )

        # ----------------------------------------------------
        # FILTER RATING
        # ----------------------------------------------------

        if rating:

            try:

                rating_value = float(
                    rating
                )

                query = query.filter(
                    Prediction.rating >=
                    rating_value
                )

            except (
                TypeError,
                ValueError
            ):

                pass

        # ----------------------------------------------------
        # ORDER
        # ----------------------------------------------------

        query = query.order_by(
            Prediction.created_at.desc()
        )

        # ----------------------------------------------------
        # PAGINATION
        # ----------------------------------------------------

        return query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    # ========================================================
    # GET ONE PREDICTION
    # ========================================================

    @staticmethod
    def get_prediction_by_id(
        prediction_id,
        user_id=None
    ):
        """
        Lấy một prediction theo ID.

        Nếu user_id được truyền vào,
        chỉ cho phép lấy prediction của user đó.
        """

        query = Prediction.query.filter(
            Prediction.id == prediction_id
        )

        if user_id is not None:

            query = query.filter(
                Prediction.user_id == user_id
            )

        return query.first()

    # ========================================================
    # DELETE ONE PREDICTION
    # ========================================================

    @staticmethod
    def delete_prediction(
        prediction_id,
        user_id=None
    ):
        """
        Xóa một prediction.

        user_id=None:
            Cho phép Admin xóa prediction.

        user_id=<id>:
            Chỉ xóa prediction thuộc user đó.
        """

        query = Prediction.query.filter(
            Prediction.id == prediction_id
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

    # ========================================================
    # CLEAR HISTORY
    # ========================================================

    @staticmethod
    def clear_history(
        user_id=None
    ):
        """
        Xóa toàn bộ lịch sử.

        user_id=None:
            Xóa toàn bộ prediction của hệ thống.
            Chỉ nên gọi từ Admin.

        user_id=<id>:
            Xóa toàn bộ prediction của user đó.
        """

        query = Prediction.query

        if user_id is not None:

            query = query.filter(
                Prediction.user_id == user_id
            )

        predictions = query.all()

        deleted_count = len(
            predictions
        )

        for prediction in predictions:

            db.session.delete(
                prediction
            )

        db.session.commit()

        return deleted_count

    # ========================================================
    # GET RATING DISTRIBUTION
    # ========================================================

    @staticmethod
    def get_rating_distribution(
        user_id=None
    ):
        """
        Lấy phân bố Rating.

        Trả về dạng:

            [
                (rating, count),
                ...
            ]

        user_id=None:
            Toàn bộ hệ thống.

        user_id=<id>:
            Chỉ user đó.
        """

        query = (
            db.session.query(
                Prediction.rating,
                func.count(
                    Prediction.id
                )
            )
        )

        if user_id is not None:

            query = query.filter(
                Prediction.user_id == user_id
            )

        query = (
            query
            .group_by(
                Prediction.rating
            )
            .order_by(
                Prediction.rating.asc()
            )
        )

        return query.all()

    # ========================================================
    # GET RATING SUMMARY
    # ========================================================

    @staticmethod
    def get_rating_summary(
        user_id=None
    ):
        """
        Lấy thống kê Rating tổng quan.
        """

        query = Prediction.query

        if user_id is not None:

            query = query.filter(
                Prediction.user_id == user_id
            )

        ratings = [
            float(item.rating)
            for item in query.all()
        ]

        if not ratings:

            return {
                "min": 0.0,
                "max": 0.0,
                "average": 0.0
            }

        return {
            "min": round(
                min(ratings),
                2
            ),
            "max": round(
                max(ratings),
                2
            ),
            "average": round(
                sum(ratings) /
                len(ratings),
                2
            )
        }

    # ========================================================
    # GET TOP USERS
    # ========================================================

    @staticmethod
    def get_top_users(
        limit=5
    ):
        """
        Lấy những user có nhiều lượt dự đoán nhất.

        Chỉ sử dụng cho Dashboard/Admin.
        """

        results = (
            db.session.query(
                User.id,
                User.username,
                func.count(
                    Prediction.id
                ).label(
                    "prediction_count"
                )
            )
            .outerjoin(
                Prediction,
                User.id ==
                Prediction.user_id
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

        return results

    # ========================================================
    # GET PREDICTION TREND
    # ========================================================

    @staticmethod
    def get_prediction_trend(
        user_id=None,
        limit=10
    ):
        """
        Lấy các prediction gần đây để
        hiển thị biểu đồ xu hướng.

        Trả về các object Prediction.
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

    # ========================================================
    # GET RECENT PREDICTIONS
    # ========================================================

    @staticmethod
    def get_recent_predictions(
        user_id=None,
        limit=10
    ):
        """
        Lấy các dự đoán gần nhất.
        """

        query = Prediction.query

        if user_id is not None:

            query = query.filter(
                Prediction.user_id == user_id
            )

        return (
            query
            .order_by(
                Prediction.created_at.desc()
            )
            .limit(limit)
            .all()
        )

    # ========================================================
    # GET USER STATISTICS
    # ========================================================

    @staticmethod
    def get_user_statistics(
        user_id
    ):
        """
        Lấy thống kê riêng của một user.
        """

        return {
            "total_predictions":
                PredictionService
                .get_total_predictions(
                    user_id=user_id
                ),

            "average_rating":
                PredictionService
                .get_average_rating(
                    user_id=user_id
                ),

            "accuracy":
                PredictionService
                .get_prediction_accuracy(
                    user_id=user_id
                ),

            "rating_distribution":
                PredictionService
                .get_rating_distribution(
                    user_id=user_id
                )
        }

    # ========================================================
    # GET SYSTEM STATISTICS
    # ========================================================

    @staticmethod
    def get_system_statistics():
        """
        Lấy thống kê tổng quan cho Admin.
        """

        return {
            "total_users":
                User.query.count(),

            "total_predictions":
                PredictionService
                .get_total_predictions(),

            "average_rating":
                PredictionService
                .get_average_rating(),

            "accuracy":
                PredictionService
                .get_prediction_accuracy(),

            "total_admins":
                User.query.filter_by(
                    role="Admin"
                ).count(),

            "total_developers":
                User.query.filter_by(
                    role="Developer"
                ).count(),

            "total_normal_users":
                User.query.filter_by(
                    role="User"
                ).count()
        }