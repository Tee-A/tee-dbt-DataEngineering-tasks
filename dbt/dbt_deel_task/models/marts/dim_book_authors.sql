
SELECT 
{{ dbt_utils.generate_surrogate_key(['book_id', 'title']) }} as book_key,
*
FROM {{ ref('stg_book_authors') }}