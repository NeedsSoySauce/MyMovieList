from datetime import datetime

from flask import Blueprint

utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


@utilities_blueprint.app_template_filter()
def dateformat(date: datetime):
    return date.strftime('%e %b %Y')
