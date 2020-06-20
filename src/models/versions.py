from src.models.base import db


class Versions(db.Model):
    """Model to represent versions table for subscriptions"""
    __tablename__ = "versions"

    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey("subscriptions.id"), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey("plans.id"), nullable=False)

    effective_date_start = db.Column(db.TIMESTAMP(timezone=True))
    effective_date_end = db.Column(db.TIMESTAMP(timezone=True))
    creation_date = db.Column(db.TIMESTAMP(timezone=True))

    subscription = db.relationship(
        "Subscription", foreign_keys=[subscription_id], lazy="select", back_populates="versions"
    )
    plan = db.relationship("Plan", foreign_keys=[plan_id], lazy="select")

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}: {self.id}, "
            f"effective_date_start: {self.effective_date_start}, effective_date_end: {self.effective_date_end}>, "
            f"<subscription: {self.subscription_id}>, "
            f"<plan: {self.plan_id}>"
        )
