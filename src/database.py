import sqlite3
import json
import structlog
import os

logger = structlog.get_logger()


def setup_database():
    try:
        db_path = "papers.db"
        logger.info(f"Attempting to connect to database at {os.path.abspath(db_path)}")

        with sqlite3.connect(db_path) as conn:
            # Set up DB
            sql = """CREATE TABLE IF NOT EXISTS papers (
                  uid INTEGER PRIMARY KEY AUTOINCREMENT,
                  id varchar NOT NULL UNIQUE,
                  uri varchar NOT NULL,
                  title varchar NOT NULL,
                  authors TEXT,
                  abstract TEXT,
                  categories TEXT,
                  published varchar
                );"""

            # Create a cursor
            cur = conn.cursor()

            # execute the CREATE TABLE statement
            logger.info("Executing CREATE TABLE statement")
            cur.execute(sql)

            # Verify table was created
            cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='papers';"
            )
            if cur.fetchone():
                logger.info("Table 'papers' created or already exists")
            else:
                logger.error("Failed to create table 'papers'")

            # commit the changes
            conn.commit()

            return True

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        print(f"Database error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")
        return False


class DB:
    def store_metadata(self, paper):
        try:
            with sqlite3.connect("papers.db") as conn:
                sql = """INSERT INTO papers(id, title, uri, authors, abstract, categories, published) 
                VALUES (?,?,?,?,?,?,?)
                ON CONFLICT(id) DO NOTHING
                """

                # Create  a cursor
                cur = conn.cursor()

                # execute the INSERT statement
                cur.execute(
                    sql,
                    (
                        paper["id"],
                        paper["title"],
                        paper["resource_uri"],
                        json.dumps(paper["authors"]),
                        paper["abstract"],
                        json.dumps(paper["categories"]),
                        paper["published"],
                    ),
                )

                # Check if a row was inserted
                if conn.total_changes > 0:
                    logger.info(f"Stored {paper['id']}")
                else:
                    # No rows were affected, meaning there was a conflict
                    logger.info(f"Skipped duplicate paper with ID: {paper['id']}")

                # commit the changes
                conn.commit()

        except sqlite3.Error as e:
            logger.error(e)

def search_papers(self, paper):
        try:
            with sqlite3.connect("papers.db") as conn:
                sql = """SELECT id FROM papers WHERE id IN ()"""

                # Create  a cursor
                cur = conn.cursor()

                # execute the INSERT statement
                cur.execute(sql)

                # Check if a row was inserted
                if conn.total_changes > 0:
                    logger.info(f"Stored {paper['id']}")
                else:
                    # No rows were affected, meaning there was a conflict
                    logger.info(f"Skipped duplicate paper with ID: {paper['id']}")

                # commit the changes
                conn.commit()

        except sqlite3.Error as e:
            logger.error(e)
