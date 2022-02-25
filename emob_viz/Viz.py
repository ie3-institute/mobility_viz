import logging

from emob_viz.Source import Source

source = Source.with_defaults("postgres", "postgres", "postgres1234!")
try:
    connection = source.get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM novagent.poi LIMIT 5;")
    data = cursor.fetchall()

    for row in data:
        print(row)

    # Don't forget to close the connection!
    connection.close()
except Exception as e:
    logging.error("Unable to connect to database.", e)
