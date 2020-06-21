"""Plan related tasks"""
from celery.utils.log import get_task_logger
from sqlalchemy import or_, not_

from src.celery_app import celery
from src.models.base import db
from src.models.cycles import BillingCycle
from src.models.versions import Versions
from src.models.utils import get_object_or_404

log = get_task_logger(__name__)


def get_actual_versions_as_list(subscription_id, versions_query):
    """Get actual versions by subscription_id as list
    :param billing_cycle: billing_cycle object
    :param subscription_id: subscription_id
    :param versions_query: base_query to get actual versions
    :return: List of actual Versions
    """
    versions = versions_query.filter_by({"subscription_id": subscription_id}).all()

    return versions or []


def get_actual_versions_as_dict(versions_query):
    """Get actual versions as dict
    :param versions_query: base_query to get actual versions
    :return: Dict of actual Versions
    """
    versions = versions_query.all()
    if not versions:
        return {}

    result = {}
    for version in versions:
        if version.plan_id not in result:
            result[version.plan_id] = []
        result[version.plan_id].append(version.subscription_id)

    return result


@celery.task()
def query_subscription_plans(billing_cycle_id: int, subscription_id: int = None):
    """This function takes ids of BillingCycle and Subscription"""

    billing_cycle = get_object_or_404(BillingCycle, billing_cycle_id)
    base_versions_query = db.session.query(Versions).filter(
        not_(or_(Versions.effective_date_start >= billing_cycle.end_date,
                 Versions.effective_date_end <= billing_cycle.start_date))
    )

    if subscription_id:
        return get_actual_versions_as_list(subscription_id, base_versions_query)

    return get_actual_versions_as_dict(base_versions_query)
