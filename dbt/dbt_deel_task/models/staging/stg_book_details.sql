
SELECT 
    list_id, CAST(published_date AS DATE) as published_date, primary_isbn13 as book_id, title, created_date, age_group, price, primary_isbn10, description,
    rank, publisher, updated_date, weeks_on_list
FROM {{ source('nyt_books', 'nyt_books') }}