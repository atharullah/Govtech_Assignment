SELECT i.item_name, COUNT(mt.item_id) AS total_bought
FROM item i
JOIN member_transaction mt ON i.item_id = mt.item_id
GROUP BY i.item_name
ORDER BY total_bought DESC
LIMIT 3;
