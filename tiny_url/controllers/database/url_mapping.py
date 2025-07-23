import os

from fastapi import status
from pydantic import AwareDatetime

from tiny_url.interfaces.database import get_database_connection
from tiny_url.models.exceptions import TinyUrlBaseException
from tiny_url.models.url import SlugUrl


class UrlMappingController:
    @staticmethod
    def create_database():
        """
        Runs the script stored un init_table.sql (here to create the table)
        """
        env_file_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "sql", "init_table.sql")

        with open(env_file_path, "rb") as f:
            sql_script = f.read()

        with get_database_connection() as cursor:
            cursor.execute(query=sql_script)

    @staticmethod
    def insert_record(source_url: str, slug_url: str, end_validity_date: AwareDatetime = None) -> SlugUrl:
        """
        Inserts the record in the url_mapping table

        Args:
            source_url (str): Source URL getting shortened
            slug_url (str): Shrort version of the long url
            end_validity_date (Optional, AwareDatetime): Validity end date for the short url

        Returns:
            SlugUrl: model containing the record data
        """
        insert_query = """
        INSERT INTO url_mapping (source_url, slug_url, end_validity_date)
        VALUES (%s, %s, %s)
        RETURNING id, source_url, slug_url, end_validity_date;
        """

        with get_database_connection() as cursor:
            cursor.execute(insert_query, (source_url, slug_url, end_validity_date))

            ins = cursor.fetchone()

            slug_url = SlugUrl(
                id=ins[0],
                source_url=ins[1],
                slug_url=ins[2],
                end_validity_date=ins[3]
            )

        return slug_url

    @staticmethod
    def get_long_url_by_slug_url(slug_url: str) -> (str, AwareDatetime):
        """
        Based on a short url, returns the associated long url and its end validity date

        Args:
            slug_url (str): short url

        Raises:
            TinyUrlBaseException: if no short url is found

        Returns:
            str: long version of the url
            AwareDatetime | None: short link end validity date
        """
        query = """
        SELECT id, source_url, end_validity_date
        FROM url_mapping
        WHERE slug_url = %s;
        """
        with get_database_connection() as cursor:
            cursor.execute(query, (slug_url,))
            result = cursor.fetchone()
            if result is None:
                raise TinyUrlBaseException(message="No slug url found", status_code=status.HTTP_404_NOT_FOUND)
            else:
                long_url = result[1]
                url_mapping_id = result[0]
                end_validity_date = result[2]

        UrlMappingController.update_clic_counter(url_mapping_id=url_mapping_id)

        return long_url, end_validity_date

    @staticmethod
    def update_clic_counter(url_mapping_id: int) -> None:
        """
        Updates the clic counter for a given short url (based on its ID)

        Args:
            url_mapping_id (int): record ID
        """
        update_query = """
        UPDATE url_mapping
        SET clic_count = clic_count + 1
        WHERE id = %s
        RETURNING clic_count;
        """

        with get_database_connection() as cursor:
            cursor.execute(update_query, (url_mapping_id,))
