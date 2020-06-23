"""Plan related tasks"""
from celery.utils.log import get_task_logger
from sqlalchemy import or_, not_

from src.celery_app import celery
from src.models.base import db
from src.models.cycles import BillingCycle
from src.models.versions import Versions
from src.models.utils import get_object_or_404

log = get_task_logger(__name__)


def get_actual_subscriptions(versions):
    """Get actual subscriptions from versions
    Args:
        versions: (list) list of versions

    Returns:
        Dict with actual subscriptions
    """
    actual_subscriptions = {}
    for version in versions:
        if version.subscription_id not in actual_subscriptions \
                or actual_subscriptions[version.subscription_id].creation_date <= version.creation_date:
            actual_subscriptions[version.subscription_id] = version
    return actual_subscriptions.values()


def get_actual_versions_as_list(subscription_id, versions_query):
    """ Get actual versions by subscription_id as list

    Args:
        subscription_id: (int) Subscription identifier
        versions_query: base_query to get actual versions

    Returns:
        List of actual Versions
    """
    versions = versions_query.filter_by(subscription_id=subscription_id).all()
    actual_subscriptions = get_actual_subscriptions(versions)

    # QUESTION: From the task I don't understand what is plan size,
    # is it plan_id or plan.mb_available or some another column,
    # so I decide to use mb_available, because it's closest solution to be true
    return [(
        version.plan.mb_available,
        version.effective_date_start,
        version.effective_date_end
    ) for version in actual_subscriptions] or []


def get_actual_versions_as_dict(versions_query):
    """Get actual versions as dict

    Args:
        versions_query: base_query to get actual versions

    Returns:
        Dict of actual Versions
    """
    versions = versions_query.all()
    if not versions:
        return {}
    actual_subscriptions = get_actual_subscriptions(versions)
    result = {}
    for version in actual_subscriptions:
        if version.plan.mb_available not in result:
            result[version.plan.mb_available] = []
        result[version.plan.mb_available].append(version.subscription_id)

    return result


@celery.task()
def query_subscription_plans(billing_cycle_id: int, subscription_id: int = None):
    """ Get plans and related Subscription

    Args:
        billing_cycle_id: (int) Billing cycle identifier
        subscription_id: (int) Subscription identifier(optional)

    Returns:
        List or Dict with Versions as a value depends on parameters
    """

    billing_cycle = get_object_or_404(BillingCycle, billing_cycle_id)
    if not billing_cycle:
        raise Exception("There is no billing cycle with id: {}".format(billing_cycle_id))
    base_versions_query = db.session.query(Versions).filter(
        not_(or_(Versions.effective_date_start >= billing_cycle.end_date,
                 Versions.effective_date_end <= billing_cycle.start_date))
    )

    if subscription_id:
        return get_actual_versions_as_list(subscription_id, base_versions_query)

    return get_actual_versions_as_dict(base_versions_query)
