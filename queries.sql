-- Basic SELECT query
SELECT * FROM flipkart_data LIMIT 5;

-- Aggregation and grouping
SELECT Month, SUM("Total Revenue (USD Mn)") as Total_Revenue
FROM flipkart_data
GROUP BY Month
ORDER BY Total_Revenue DESC;

-- JOIN operation
SELECT f.Month, f."Total Revenue (USD Mn)" as Flipkart_Revenue, 
       a."Total Revenue (USD Mn)" as Amazon_Revenue
FROM flipkart_data f
JOIN amazon_data a ON f.Month = a.Month;

-- Subquery example
SELECT *
FROM flipkart_data
WHERE "Total Revenue (USD Mn)" > (SELECT AVG("Total Revenue (USD Mn)") FROM flipkart_data);

-- Window function
SELECT Month, "Total Revenue (USD Mn)",
       AVG("Total Revenue (USD Mn)") OVER (ORDER BY Month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as Moving_Average
FROM flipkart_data;

-- Complex query combining multiple operations
SELECT 
    f.Month, 
    f."Total Revenue (USD Mn)" as Flipkart_Revenue,
    a."Total Revenue (USD Mn)" as Amazon_Revenue,
    (f."Total Revenue (USD Mn)" - a."Total Revenue (USD Mn)") as Revenue_Difference,
    CASE 
        WHEN f."Total Revenue (USD Mn)" > a."Total Revenue (USD Mn)" THEN 'Flipkart'
        ELSE 'Amazon'
    END as Higher_Revenue
FROM flipkart_data f
JOIN amazon_data a ON f.Month = a.Month
WHERE f.Month IN (
    SELECT Month
    FROM flipkart_data
    GROUP BY strftime('%Y', Month)
    HAVING MAX("Total Revenue (USD Mn)")
)
ORDER BY f.Month;
