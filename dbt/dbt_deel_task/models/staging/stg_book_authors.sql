
SELECT 
    DISTINCT primary_isbn13 as book_id, title, author, 
    REPLACE(contributor, 'by ', '') as contributor, contributor_note
FROM {{ source('nyt_books', 'nyt_books') }}