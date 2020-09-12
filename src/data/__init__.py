from flask import current_app as app

from src.tests.support.factories import DataTypeWithProjectFactory


class Seed:
    @classmethod
    def run(_klazz):
        for _ in range(app.config['SEED_DATA_COUNT']):
            DataTypeWithProjectFactory.create(mzxmls=2, metadata_shipments=2)
