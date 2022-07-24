SELECT * FROM posts LEFT JOIN users ON posts.user_id = users.id 
ORDER BY posts.created_at DESC;

SELECT posts.*,users.username FROM posts LEFT JOIN users ON posts.user_id = users.id 
ORDER BY posts.created_at DESC;
