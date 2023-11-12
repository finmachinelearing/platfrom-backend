SCOREBOARD_SQL = (
    'SELECT MAX(answer.score) as score, answer.user_id FROM answer '
    'WHERE answer.task_id = %(task_id)s AND answer.score is not NULL AND answer.is_active = True '
    'GROUP BY answer.user_id ORDER BY score DESC;'
)
