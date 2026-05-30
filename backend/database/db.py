import json
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")


def _column_exists(cursor: sqlite3.Cursor, table: str, column: str) -> bool:
    cursor.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cursor.fetchall())


def _add_column_if_missing(
    cursor: sqlite3.Cursor, table: str, column: str, definition: str
) -> None:
    if _column_exists(cursor, table, column):
        return
    cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS content_task (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            tags TEXT,
            platforms TEXT,
            author TEXT,
            use_ai INTEGER,
            llm_provider TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    _add_column_if_missing(cursor, "content_task", "author", "TEXT")
    _add_column_if_missing(cursor, "content_task", "use_ai", "INTEGER")
    _add_column_if_missing(cursor, "content_task", "llm_provider", "TEXT")

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS media_file (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            file_name TEXT NOT NULL,
            file_url TEXT NOT NULL,
            file_type TEXT NOT NULL,
            file_size INTEGER,
            created_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS platform_content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            platform TEXT NOT NULL,
            title TEXT,
            content TEXT,
            summary TEXT,
            description TEXT,
            tags TEXT,
            media_files TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS publish_record (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            platform TEXT NOT NULL,
            final_title TEXT,
            final_content TEXT,
            status TEXT NOT NULL,
            message TEXT,
            publish_time TEXT NOT NULL
        )
        """
    )

    _add_column_if_missing(cursor, "publish_record", "message", "TEXT")
    _add_column_if_missing(cursor, "publish_record", "publish_id", "TEXT")

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            account TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            token TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS platform_account (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            platform TEXT NOT NULL,
            account_name TEXT,
            auth_type TEXT,
            access_token TEXT,
            login_status TEXT,
            token_expire_time TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ai_setting (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            provider TEXT,
            settings TEXT,
            updated_at TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def create_task(
    title: str,
    content: str,
    tags: list,
    platforms: list,
    author: str | None = None,
    use_ai: bool = False,
    llm_provider: str | None = None,
) -> int:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO content_task (
            title, content, tags, platforms, author, use_ai, llm_provider, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """,
        (
            title,
            content,
            json.dumps(tags, ensure_ascii=False),
            json.dumps(platforms, ensure_ascii=False),
            author,
            1 if use_ai else 0,
            llm_provider,
        ),
    )
    connection.commit()
    task_id = cursor.lastrowid
    connection.close()
    return int(task_id)


def create_publish_record(
    task_id: int,
    platform: str,
    final_title: str,
    final_content: str,
    status: str,
    message: str,
    publish_time: str,
    publish_id: str | None = None,
) -> None:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO publish_record (
            task_id, platform, final_title, final_content, status, message, publish_time, publish_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (task_id, platform, final_title, final_content, status, message, publish_time, publish_id),
    )
    connection.commit()
    connection.close()


def create_media_file(
    task_id: int,
    file_name: str,
    file_url: str,
    file_type: str,
    file_size: int | None,
) -> None:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO media_file (
            task_id, file_name, file_url, file_type, file_size, created_at
        )
        VALUES (?, ?, ?, ?, ?, datetime('now'))
        """,
        (task_id, file_name, file_url, file_type, file_size),
    )
    connection.commit()
    connection.close()


def create_platform_content(task_id: int, platform: str, payload: dict) -> None:
    connection = get_connection()
    cursor = connection.cursor()

    tags = json.dumps(payload.get("tags", []), ensure_ascii=False)
    media_files = {
        "images": payload.get("images", []),
        "videos": payload.get("videos", []),
        "cover": payload.get("cover"),
    }
    if payload.get("video") and not media_files["videos"]:
        media_files["videos"] = [payload.get("video")]

    cursor.execute(
        """
        INSERT INTO platform_content (
            task_id,
            platform,
            title,
            content,
            summary,
            description,
            tags,
            media_files,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """,
        (
            task_id,
            platform,
            payload.get("title"),
            payload.get("content"),
            payload.get("summary"),
            payload.get("description"),
            tags,
            json.dumps(media_files, ensure_ascii=False),
        ),
    )
    connection.commit()
    connection.close()


def list_platform_contents(task_id: int) -> dict:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT platform, title, content, summary, description, tags, media_files
        FROM platform_content
        WHERE task_id = ?
        """,
        (task_id,),
    )

    rows = cursor.fetchall()
    connection.close()

    results = {}
    for row in rows:
        tags = json.loads(row["tags"]) if row["tags"] else []
        media_files = json.loads(row["media_files"]) if row["media_files"] else {}
        content = {
            "platform": row["platform"],
            "title": row["title"],
            "content": row["content"],
            "summary": row["summary"],
            "description": row["description"],
            "tags": tags,
            "images": media_files.get("images", []),
            "videos": media_files.get("videos", []),
            "cover": media_files.get("cover"),
        }

        if content["videos"]:
            content["video"] = content["videos"][0]

        results[row["platform"]] = content

    return results


def list_records(limit: int = 50) -> list:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, platform, final_title, status, message, publish_time, publish_id
        FROM publish_record
        ORDER BY publish_time DESC
        LIMIT ?
        """,
        (limit,),
    )

    rows = cursor.fetchall()
    connection.close()

    records = []
    for row in rows:
        records.append(
            {
                "id": row["id"],
                "platform": row["platform"],
                "title": row["final_title"],
                "status": row["status"],
                "message": row["message"],
                "publish_time": row["publish_time"],
                "publish_id": row["publish_id"] or f"mock_{row['platform']}_{row['id']}",
            }
        )

    return records


def get_record_detail(record_id: int) -> dict | None:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            r.id,
            r.task_id,
            r.platform,
            r.final_title,
            r.final_content,
            r.status,
            r.message,
            r.publish_time,
            r.publish_id,
            t.title AS task_title,
            t.content AS source_content,
            t.tags AS source_tags,
            t.platforms AS task_platforms
        FROM publish_record r
        LEFT JOIN content_task t ON t.id = r.task_id
        WHERE r.id = ?
        """,
        (record_id,),
    )
    row = cursor.fetchone()
    if not row:
        connection.close()
        return None

    cursor.execute(
        """
        SELECT platform, title, content, summary, description, tags, media_files
        FROM platform_content
        WHERE task_id = ?
        """,
        (row["task_id"],),
    )
    content_rows = cursor.fetchall()
    connection.close()

    platform_contents = []
    for content_row in content_rows:
        media_files = json.loads(content_row["media_files"]) if content_row["media_files"] else {}
        platform_contents.append(
            {
                "platform": content_row["platform"],
                "title": content_row["title"],
                "content": content_row["content"],
                "summary": content_row["summary"],
                "description": content_row["description"],
                "tags": json.loads(content_row["tags"]) if content_row["tags"] else [],
                "images": media_files.get("images", []),
                "videos": media_files.get("videos", []),
                "cover": media_files.get("cover"),
                "status": row["status"],
                "publish_id": row["publish_id"] or f"mock_{content_row['platform']}_{row['id']}",
            }
        )

    if not platform_contents:
        platform_contents.append(
            {
                "platform": row["platform"],
                "title": row["final_title"],
                "content": row["final_content"],
                "tags": json.loads(row["source_tags"]) if row["source_tags"] else [],
                "images": [],
                "videos": [],
                "cover": None,
                "status": row["status"],
                "publish_id": row["publish_id"] or f"mock_{row['platform']}_{row['id']}",
            }
        )

    return {
        "id": row["id"],
        "task_id": row["task_id"],
        "task_title": row["task_title"] or row["final_title"],
        "source_content": row["source_content"],
        "publish_time": row["publish_time"],
        "publish_mode": "mock",
        "status": row["status"],
        "message": row["message"],
        "publish_id": row["publish_id"] or f"mock_{row['platform']}_{row['id']}",
        "platforms": json.loads(row["task_platforms"]) if row["task_platforms"] else [row["platform"]],
        "platform_contents": platform_contents,
    }


def list_materials(limit: int = 200) -> list:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, task_id, file_name, file_url, file_type, file_size, created_at
        FROM media_file
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cursor.fetchall()
    connection.close()

    return [
        {
            "id": row["id"],
            "task_id": row["task_id"],
            "name": row["file_name"],
            "url": row["file_url"],
            "type": row["file_type"],
            "size": row["file_size"] or 0,
            "created_at": row["created_at"],
            "usage_count": 1 if row["task_id"] else 0,
        }
        for row in rows
    ]


def create_user(username: str, account: str, password: str, token: str) -> dict:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO user (username, account, password, token, created_at)
        VALUES (?, ?, ?, ?, datetime('now'))
        """,
        (username, account, password, token),
    )
    connection.commit()
    user_id = cursor.lastrowid
    connection.close()
    return {"id": user_id, "username": username, "account": account, "token": token}


def find_user_by_account(account: str) -> dict | None:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, username, account, password, token
        FROM user
        WHERE account = ?
        """,
        (account,),
    )
    row = cursor.fetchone()
    connection.close()
    if not row:
        return None
    return dict(row)


def find_user_by_token(token: str) -> dict | None:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, username, account, token
        FROM user
        WHERE token = ?
        """,
        (token,),
    )
    row = cursor.fetchone()
    connection.close()
    if not row:
        return None
    return dict(row)


def upsert_platform_account(
    platform: str,
    account_name: str,
    auth_type: str = "mock",
    token: str = "",
    status: str = "logged_in",
) -> dict:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO platform_account (
            platform, account_name, auth_type, access_token, login_status,
            token_expire_time, created_at
        )
        VALUES (?, ?, ?, ?, ?, '2026-12-31', datetime('now'))
        """,
        (platform, account_name, auth_type, token, status),
    )
    connection.commit()
    account_id = cursor.lastrowid
    connection.close()
    return {
        "id": account_id,
        "platform": platform,
        "account_name": account_name,
        "auth_type": auth_type,
        "access_token": token,
        "login_status": status,
        "token_expire_time": "2026-12-31",
    }


def list_platform_accounts() -> list:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT platform, account_name, auth_type, access_token, login_status, token_expire_time
        FROM platform_account
        ORDER BY id DESC
        """
    )
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]


def get_ai_setting() -> dict:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT provider, settings, updated_at
        FROM ai_setting
        ORDER BY id DESC
        LIMIT 1
        """
    )
    row = cursor.fetchone()
    connection.close()
    if not row:
        return {}
    settings = json.loads(row["settings"]) if row["settings"] else {}
    settings["provider"] = row["provider"]
    settings["updated_at"] = row["updated_at"]
    return settings


def save_ai_setting(provider: str, settings: dict) -> dict:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO ai_setting (provider, settings, updated_at)
        VALUES (?, ?, datetime('now'))
        """,
        (provider, json.dumps(settings, ensure_ascii=False)),
    )
    connection.commit()
    connection.close()
    return get_ai_setting()
