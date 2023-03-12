SELECT m.first_name, m.last_name, SUM(mt.total_price) AS total_spending
FROM member m
JOIN member_transaction mt ON m.membership_id = mt.membership_id
GROUP BY m.first_name, m.last_name
ORDER BY total_spending DESC
LIMIT 10;
