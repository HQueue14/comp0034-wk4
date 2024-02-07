from flask import current_app as app, abort, jsonify
from sqlalchemy.exc import SQLAlchemyError
from paralympics import db
from paralympics.models import Region
from paralympics.schemas import RegionSchema

region_schema = RegionSchema()


@app.errorhandler(404)
def resource_not_found(e):
    """ Error handler for 404.

        Args:
            HTTP 404 error
        Returns:
            JSON response with the validation error message and the 404 status code
        """
    return jsonify(error=str(e)), 404


@app.get('/regions/<code>')
def get_region(code):
    """ Returns one region in JSON.

    Returns 404 if the region code is not found in the database.

    Args:
        code (str): The 3 digit NOC code of the region to be searched for
    Returns: 
        JSON for the region if found otherwise 404
    """
    # Try to find the region, if it is not found, catch the error and return 404
    try:
        region = db.session.execute(db.select(Region).filter_by(NOC=code)).scalar_one()
        result = region_schema.dump(region)
        return result
    except SQLAlchemyError as e:
        # See https://flask.palletsprojects.com/en/2.3.x/errorhandling/#returning-api-errors-as-json
        abort(404, description="Region not found.")