SCOREBOARD_SQL = (
    'SELECT score, user_id, "user".surname AS surname FROM "user" '
    'JOIN (SELECT MAX(answer.score) AS score, answer.user_id FROM answer '
    'WHERE answer.task_id = %(task_id)s AND answer.score IS NOT NULL AND answer.is_active = TRUE '
    'GROUP BY answer.user_id ORDER BY score DESC) scores ON "user".id = scores.user_id'
)

DISTINCT_TASKS_SQL = (
    'SELECT DISTINCT answer.task_id FROM answer WHERE answer.user_id = %(user_id)s'
)
