
SELECT 
    DISTINCT list_id, list_name, display_name 
FROM {{ source('nyt_books', 'nyt_books') }}