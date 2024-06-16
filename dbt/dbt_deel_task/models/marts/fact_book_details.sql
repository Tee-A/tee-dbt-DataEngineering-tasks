
SELECT 
{{ dbt_utils.generate_surrogate_key(['published_date', 'list_id', 'book_id']) }} as fact_key,
{{ dbt_utils.generate_surrogate_key(['list_id']) }} as list_key,
{{ dbt_utils.generate_surrogate_key(['book_id', 'title']) }} as book_key,
CAST(CONCAT(LEFT(CAST(published_date As TEXT), 4), SUBSTR(CAST(published_date As TEXT), 6, 2), SUBSTR(CAST(published_date As TEXT), 9, 2)) As INTEGER) As published_date_key,
CAST(published_date as DATE) as published_date,
age_group, price, primary_isbn10,
rank, publisher, updated_date, weeks_on_list
FROM {{ ref('stg_book_details') }}