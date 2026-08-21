from flask import Flask

from config import Config
from extensions import db

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.predict import predict_bp
from routes.admin import admin_bp
from routes.developer import developer_bp
from routes.history import history_bp
from routes.analytics import analytics_bp
from routes.profile import profile_bp


# ==========================================
# CREATE APP
# ==========================================

app = Flask(__name__)

app.config.from_object(Config)

# ==========================================
# DATABASE
# ==========================================

db.init_app(app)

with app.app_context():
    db.create_all()


# ==========================================
# REGISTER BLUEPRINT
# ==========================================

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(predict_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(developer_bp)
app.register_blueprint(history_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(profile_bp)


# ==========================================
# PRINT ROUTES
# ==========================================

print("\n==========================================")
print("        DANH SÁCH ROUTE CỦA HỆ THỐNG")
print("==========================================")

for rule in app.url_map.iter_rules():
    print(
        f"{rule.endpoint:35} "
        f"{rule.methods} "
        f"{rule}"
    )

print("==========================================\n")


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000,
        use_reloader=False
    )