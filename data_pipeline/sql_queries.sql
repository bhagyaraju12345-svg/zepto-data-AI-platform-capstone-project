<<<<<<< HEAD
-- Q1_SELECT_WHERE
SELECT
            title,
            price_gbp,
            rating,
            in_stock
        FROM books
        WHERE price_gbp > 40
        ORDER BY price_gbp DESC

-- Q2_ORDER_BY_LIMIT
SELECT
            title,
            price_gbp,
            rating
        FROM books
        ORDER BY price_gbp DESC
        LIMIT 10

-- Q3_DISTINCT
SELECT DISTINCT
            rating
        FROM books
        ORDER BY rating

-- Q4_BETWEEN
SELECT
            title,
            price_gbp,
            price_inr
        FROM books
        WHERE price_gbp BETWEEN 20 AND 40
        ORDER BY price_gbp

-- Q5_JOIN
SELECT
            b.title,
            c.category_name,
            b.price_gbp,
            b.price_inr,
            b.rating,
            b.in_stock
        FROM books AS b
        INNER JOIN categories AS c
            ON b.category_id = c.category_id
        ORDER BY
            b.rating DESC,
            c.category_name,
            b.title
        LIMIT 10

=======
-- Q1_SELECT_WHERE
SELECT
            title,
            price_gbp,
            rating,
            in_stock
        FROM books
        WHERE price_gbp > 40
        ORDER BY price_gbp DESC

-- Q2_ORDER_BY_LIMIT
SELECT
            title,
            price_gbp,
            rating
        FROM books
        ORDER BY price_gbp DESC
        LIMIT 10

-- Q3_DISTINCT
SELECT DISTINCT
            rating
        FROM books
        ORDER BY rating

-- Q4_BETWEEN
SELECT
            title,
            price_gbp,
            price_inr
        FROM books
        WHERE price_gbp BETWEEN 20 AND 40
        ORDER BY price_gbp

-- Q5_JOIN
SELECT
            b.title,
            c.category_name,
            b.price_gbp,
            b.price_inr,
            b.rating,
            b.in_stock
        FROM books AS b
        INNER JOIN categories AS c
            ON b.category_id = c.category_id
        ORDER BY
            b.rating DESC,
            c.category_name,
            b.title
        LIMIT 10

>>>>>>> 08113b3fb69eb4f5b7a46eb0e6de961e744a2ee7
