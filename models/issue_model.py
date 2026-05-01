from connection import db_connector


def create_issue(title, summary, category_id):
    conn = db_connector()
    cursor = conn.cursor()

    query = """
        INSERT INTO issues (title, summary, category_id)
        VALUES (%s, %s, %s)
    """

    cursor.execute(query, (title, summary, category_id))
    conn.commit()

    issue_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return issue_id


def get_all_issues(category=None, sort=None):
    con = db_connector()
    cursor = con.cursor(dictionary=True)

    query = """
        SELECT issues.*, categories.name AS category_name
        FROM issues
        JOIN categories ON issues.category_id = categories.id
    """

    params = []

    # Filter by category
    if category:
        query += " WHERE categories.name = %s"
        params.append(category)

    # Sorting
    if sort == "latest":
        query += " ORDER BY issues.created_at DESC"
    else:
        query += " ORDER BY issues.id DESC"  # default fallback

    cursor.execute(query, params)
    results = cursor.fetchall()

    cursor.close()
    con.close()

    return results


def get_issue_by_id(issue_id):
    con = db_connector()
    cursor = con.cursor(dictionary=True)

    query = """
        SELECT issues.*, categories.name AS category_name
        FROM issues
        JOIN categories ON issues.category_id = categories.id
        WHERE issues.id = %s
    """

    cursor.execute(query, (issue_id,))
    result = cursor.fetchone()

    cursor.close()
    con.close()

    return result
