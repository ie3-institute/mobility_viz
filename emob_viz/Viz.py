import logging

from emob_viz.Source import Source

source = Source.with_defaults("postgres", "postgres", "postgres1234!")
try:
    connection = source.get_connection()
except Exception as e:
    logging.error("Unable to connect to database.", e)
