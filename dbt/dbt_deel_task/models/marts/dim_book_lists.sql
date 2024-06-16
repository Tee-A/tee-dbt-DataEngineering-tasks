
SELECT 
{{ dbt_utils.generate_surrogate_key(['list_id']) }} as list_key,
*
FROM {{ ref('stg_book_lists') }}