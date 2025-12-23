from src.db.database import Database


def get_brand_settings_id_by_brand_id(brand_id=None, cursor=None):
    """
    Fetch active brand_settings.id for a given brand_id
    """
    try:
        query = """
            SELECT id
            FROM brand_settings
            WHERE inactive_settings = 0
              AND brand_id = %(brand_id)s
            LIMIT 1
        """
        params = {"brand_id": brand_id}

        result = Database.fetchone(cursor=cursor, query=query, params=params)
        return result["id"] if result else None

    except Exception as e:
        raise e


def get_microservice_details_by_module_id(module_id=None, cursor=None):
    """
    Fetch active microservice row by module_id
    """
    try:
        query = """
            SELECT *
            FROM microservice
            WHERE module_id = %(module_id)s
              AND inactive = 0
            LIMIT 1
        """
        params = {"module_id": module_id}

        return Database.fetchone(cursor=cursor, query=query, params=params)

    except Exception as e:
        raise e


def get_service_resources(brand_id=None, resource_type=None, cursor=None):
    """
    Fetch service_resources with latest Deployment model per resource_id
    """
    try:
        query = """
            SELECT
                sr.*,
                rm.model_name
            FROM service_resources sr
            JOIN (
                SELECT rm1.resource_id, rm1.model_name
                FROM resource_model rm1
                JOIN (
                    SELECT resource_id, MAX(updated_time) AS max_updated
                    FROM resource_model
                    WHERE model_type = 'Deployment'
                      AND inactive = 0
                    GROUP BY resource_id
                ) latest
                  ON rm1.resource_id = latest.resource_id
                 AND rm1.updated_time = latest.max_updated
            ) rm
              ON sr.id = rm.resource_id
            WHERE sr.brand_id = %(brand_id)s
              AND sr.resource_type = %(resource_type)s
              AND sr.inactive = 0
        """
        params = {
            "brand_id": brand_id,
            "resource_type": resource_type
        }

        return Database.fetch(cursor=cursor, query=query, params=params)

    except Exception as e:
        raise e


def get_account_id_by_story_id(story_id=None, cursor=None):
    """
    Fetch account_id mapped to a story_id
    """
    try:
        query = """
            SELECT account_id
            FROM storyAccountMapping
            WHERE story_id = %(story_id)s
            LIMIT 1
        """
        params = {"story_id": story_id}

        return Database.fetchone(cursor=cursor, query=query, params=params)

    except Exception as e:
        raise e


def get_brand_settings_details_by_brand_id(brand_id=None, cursor=None):
    """
    Fetch brand_settings details by brand_id
    """
    try:
        query = """
            SELECT brand_settings.id as brand_settings_id, brand.bucket as bucket
            FROM brand_settings
            JOIN brand ON brand_settings.brand_id = brand.id
            WHERE 
                brand_settings.inactive_settings = 0
                AND brand.inactive = 0
                AND brand.id = %(brand_id)s            
            LIMIT 1
        """
        params = {"brand_id": brand_id}
        return Database.fetchone(cursor=cursor, query=query, params=params)
    except Exception as e:
        raise e
