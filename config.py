import os


class Config:

    BASE_DIR = os.path.abspath(
        os.path.dirname(__file__)
    )

    SECRET_KEY = "ai-rating-predictor-secret-key"

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///"
        + os.path.join(
            BASE_DIR,
            "instance",
            "prediction.db"
        )
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False