from extensions import db
from models.user import User


def create_default_users():

    default_users = [
        {
            "username": "admin",
            "password": "admin123",
            "role": "Admin"
        },
        {
            "username": "dev",
            "password": "dev123",
            "role": "Developer"
        },
        {
            "username": "user",
            "password": "123456",
            "role": "User"
        }
    ]

    for data in default_users:

        existing_user = User.query.filter_by(
            username=data["username"]
        ).first()

        if existing_user:
            continue

        user = User(
            username=data["username"],
            role=data["role"]
        )

        user.set_password(
            data["password"]
        )

        db.session.add(user)

    db.session.commit()