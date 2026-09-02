# catalog/views_api/sql_strings.py:1
# From the 'catalog/views_api/view_one_image.py:124'
# Hera one code to the variables the 'sqlite_json_object_acreate' & 'postres_json_build_object_acreate'
#   but are different databases. They are SQLite ('json_object()') and PostgreSQL ('json_build_object()')


sqlite_json_object_acreate = """
    SELECT img.id as id, json_object(
        'id', img.id,
        'title', img.title,
        'describe', img.describe,
        'label', img.label,
        'x', img.x,
        'y', img.y,
        'product', json_object(
            'id', pm.id,
            'name', pm.name,
            'product_sku', pm.product_sku,
            'price', pm.price,
            'product_discount', pm.product_discount,
            'describe_preview', pm.describe_preview,
            'description', pm.description,
            'discount_percent', pm.discount_percent,
            'stock_quantity', pm.stock_quantity,
            'attributes_additional', pm.attributes_additional,
            'created_at', pm.created_at,
            'updated_at', pm.updated_at,
            'is_active', pm.is_active,
            'brand', json_object(
                'id', b.id,
                'name', b.name,
                'description', b.description,
                'created_at', b.created_at,
                'updated_at', b.updated_at
            ),
            'category', json_object(
                'id', c.id,
                'name', c.name,
                'description', c.description,
                'created_at', c.created_at,
                'updated_at', c.updated_at
            ),
            'created_by_id', pm.created_by_id,
            'updated_by_id', pm.updated_by_id
        ),
        'image', json_object(
            'id', wi.id,
            'title', wi.title,
            'file', wi.file,
            'width', wi.width,
            'height', wi.height,
            'created_at', wi.created_at,
            'focal_point_x', wi.focal_point_x,
            'focal_point_y', wi.focal_point_y,
            'focal_point_width', wi.focal_point_width,
            'focal_point_height', wi.focal_point_height,
            'uploaded_by_user_id', wi.uploaded_by_user_id,
            'file_size', wi.file_size,
            'collection_id', wi.collection_id,
            'file_hash', wi.file_hash,
            'description', wi.description
        )) AS result
    FROM images img
    LEFT JOIN product_model pm
    ON img.product_id = pm.id
    LEFT JOIN brand b
    ON pm.brand_id = b.id
    LEFT JOIN category c
    ON pm.category_id = c.id
    LEFT JOIN wagtailimages_image wi
    ON img.image_id = wi.id
    WHERE {}
"""

postres_json_build_object_acreate = """
    SELECT img.id as id, json_build_object(
        'id', img.id,
        'title', img.title,
        'describe', img.describe,
        'label', img.label,
        'x', img.x,
        'y', img.y,
        'product', json_build_object(
            'id', pm.id,
            'name', pm.name,
            'product_sku', pm.product_sku,
            'price', pm.price,
            'product_discount', pm.product_discount,
            'describe_preview', pm.describe_preview,
            'description', pm.description,
            'discount_percent', pm.discount_percent,
            'stock_quantity', pm.stock_quantity,
            'attributes_additional', pm.attributes_additional,
            'created_at', pm.created_at,
            'updated_at', pm.updated_at,
            'is_active', pm.is_active,
            'brand', json_build_object(
                'id', b.id,
                'name', b.name,
                'description', b.description,
                'created_at', b.created_at,
                'updated_at', b.updated_at
            ),
            'category', json_build_object(
                'id', c.id,
                'name', c.name,
                'description', c.description,
                'created_at', c.created_at,
                'updated_at', c.updated_at
            ),
            'created_by_id', pm.created_by_id,
            'updated_by_id', pm.updated_by_id
        ),
        'image', json_build_object(
            'id', wi.id,
            'title', wi.title,
            'file', wi.file,
            'width', wi.width,
            'height', wi.height,
            'created_at', wi.created_at,
            'focal_point_x', wi.focal_point_x,
            'focal_point_y', wi.focal_point_y,
            'focal_point_width', wi.focal_point_width,
            'focal_point_height', wi.focal_point_height,
            'uploaded_by_user_id', wi.uploaded_by_user_id,
            'file_size', wi.file_size,
            'collection_id', wi.collection_id,
            'file_hash', wi.file_hash,
            'description', wi.description
        )) AS result
    FROM images img
    LEFT JOIN product_model pm
    ON img.product_id = pm.id
    LEFT JOIN brand b
    ON pm.brand_id = b.id
    LEFT JOIN category c
    ON pm.category_id = c.id
    LEFT JOIN wagtailimages_image wi
    ON img.image_id = wi.id
    WHERE {}
"""
