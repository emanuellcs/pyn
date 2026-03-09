from flask import Blueprint, render_template
from app.infrastructure.persistence.password_metrics import PasswordMetrics
from app.extensions import db

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/", methods=["GET"])
def index():
    # Fetch recent generations/analyses (limit to last 50 for performance)
    recent_metrics = (
        PasswordMetrics.query.order_by(PasswordMetrics.created_at.desc())
        .limit(50)
        .all()
    )

    # Calculate some basic stats
    total_generated = PasswordMetrics.query.count()
    avg_entropy = db.session.query(db.func.avg(PasswordMetrics.entropy)).scalar() or 0
    avg_score = db.session.query(db.func.avg(PasswordMetrics.score)).scalar() or 0

    # Count passwords by score
    score_distribution = {
        0: PasswordMetrics.query.filter_by(score=0).count(),
        1: PasswordMetrics.query.filter_by(score=1).count(),
        2: PasswordMetrics.query.filter_by(score=2).count(),
        3: PasswordMetrics.query.filter_by(score=3).count(),
        4: PasswordMetrics.query.filter_by(score=4).count(),
    }

    return render_template(
        "dashboard/index.html",
        recent_metrics=recent_metrics,
        total_generated=total_generated,
        avg_entropy=round(avg_entropy, 2),
        avg_score=round(avg_score, 1),
        score_distribution=score_distribution,
    )
