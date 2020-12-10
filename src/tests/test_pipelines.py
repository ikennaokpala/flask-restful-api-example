import re
import json
import factory
import xml.etree.ElementTree as ET

from flask import jsonify, current_app
from freezegun import freeze_time
from unittest.mock import patch
from dataclasses import asdict

from src.tests.base_test_case import BaseTestCase
from src.tests.support.factories import SessionFactory
from src.tests.support.factories import MaxQuantFactory
from src.tests.support.factories import PipelineFactory
from src.tests.support.factories import DataTypeWithProjectFactory
from src.main.models.pipeline import Pipeline


class TestPipelineBase(BaseTestCase):
    def setUp(self):
        super(TestPipelineBase, self).setUp()
        self.pipeline = PipelineFactory.create()
        self.prototype = MaxQuantFactory.create()
        self.data_type = DataTypeWithProjectFactory.create(
            mzxmls=2, metadata_shipments=1
        )
        self.project = self.data_type.project
        self.current_session = SessionFactory.create()
        self.headers = {'Authorization': 'Bearer ' + self.current_session.access_token}
        self.params = {
            'name': 'QC Pipeline',
            'description': 'Some science based description for this pipeline',
            'data_type': self.data_type.slug,
            'prototype': self.prototype.slug,
        }


class TestCreatePipeline(TestPipelineBase):
    @freeze_time('2020-06-02 08:57:53')
    def test_when_data_type_does_not_exist(self):
        self.params = {
            'name': 'QC Pipeline',
            'description': 'Some science based description for this pipeline',
            'data_type': 'none-existing-project',
            'prototype': self.prototype.slug,
        }
        with self.client as rdbclient:
            response = rdbclient.post(
                '/v1/pipelines', headers=self.headers, json=self.params,
            )

            self.assertEqual(response.status_code, 404)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_prototype_does_not_exist(self):
        self.params = {
            'name': 'QC Pipeline',
            'description': 'Some science based description for this pipeline',
            'data_type': self.data_type.slug,
            'prototype': 'none-existing-prototype',
        }
        with self.client as rdbclient:
            response = rdbclient.post(
                '/v1/pipelines', headers=self.headers, json=self.params,
            )

            self.assertEqual(response.status_code, 404)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_pipeline_name_is_not_supplied(self):
        self.params = {
            'description': 'Some science based description for this pipeline',
            'data_type': self.project.slug,
            'prototype': self.prototype.slug,
        }
        with self.client as rdbclient:
            response = rdbclient.post(
                '/v1/pipelines', headers=self.headers, json=self.params,
            )

            self.assertEqual(response.status_code, 400)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_pipeline_name_is_empty(self):
        self.params = {
            'name': '',
            'description': 'Some science based description for this pipeline',
            'data_type': self.data_type.slug,
            'prototype': self.prototype.slug,
        }
        with self.client as rdbclient:
            response = rdbclient.post(
                '/v1/pipelines', headers=self.headers, json=self.params,
            )

            self.assertEqual(response.status_code, 400)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_all_params_are_supplied(self):
        with self.client as rdbclient:
            response = rdbclient.post(
                '/v1/pipelines', headers=self.headers, json=self.params,
            )

            self.assertEqual(response.status_code, 201)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())

            self.assertTrue(
                re.match(
                    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
                    outcome['id'],
                )
            )
            self.assertTrue(outcome['name'] == self.params['name'])
            self.assertTrue(outcome['description'] == self.params['description'])
            self.assertTrue(outcome['project']['name'] == self.project.name)
            self.assertTrue(
                outcome['project']['description'] == self.project.description
            )
            self.assertTrue(outcome['project']['slug'] == self.project.slug)
            self.assertTrue(
                outcome['project']['data_type']['name'] == self.data_type.name
            )
            self.assertTrue(
                outcome['project']['data_type']['description']
                == self.data_type.description
            )
            self.assertTrue(
                outcome['project']['data_type']['slug'] == self.data_type.slug
            )
            self.assertTrue(outcome['prototype']['name'] == self.prototype.name)
            self.assertTrue(outcome['prototype']['type'] == self.prototype.type)
            self.assertTrue(outcome['prototype']['slug'] == self.prototype.slug)

            document = ET.fromstring(outcome['prototype']['content'])

            self.assertEqual(
                document.findall('./fastaFiles/FastaFileInfo[1]/fastaFilePath')[0].text,
                self.prototype.content['fasta_file']['path'],
            )
            for i in range(len(self.data_type.mzxml_files)):
                self.assertEqual(
                    document.findall('./filePaths/string')[i].text,
                    self.data_type.mzxml_files[0].location,
                )


class TestFetchAPipeline(TestPipelineBase):
    def setUp(self):
        super(TestFetchAPipeline, self).setUp()

    @freeze_time('2020-06-02 08:57:53')
    def test_fetch_a_pipeline(self):
        id = str(self.pipeline.id)
        self.expected = jsonify(asdict(self.pipeline))

        with self.client as rdbclient:
            response = rdbclient.get('/v1/pipelines/' + id, headers=self.headers)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())

            self.assertTrue(
                re.match(
                    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
                    outcome['id'],
                )
            )
            self.assertTrue(outcome['name'] == self.pipeline.name)
            self.assertTrue(outcome['description'] == self.pipeline.description)
            self.assertTrue(
                outcome['project']['name'] == self.pipeline.data_type.project.name
            )
            self.assertTrue(
                outcome['project']['description']
                == self.pipeline.data_type.project.description
            )
            self.assertTrue(
                outcome['project']['slug'] == self.pipeline.data_type.project.slug
            )
            self.assertTrue(
                outcome['project']['data_type']['name'] == self.pipeline.data_type.name
            )
            self.assertTrue(
                outcome['project']['data_type']['description']
                == self.pipeline.data_type.description
            )
            self.assertTrue(
                outcome['project']['data_type']['slug'] == self.pipeline.data_type.slug
            )
            self.assertTrue(
                outcome['prototype']['name'] == self.pipeline.prototype.name
            )
            self.assertTrue(
                outcome['prototype']['type'] == self.pipeline.prototype.type
            )
            self.assertTrue(
                outcome['prototype']['slug'] == self.pipeline.prototype.slug
            )

            document = ET.fromstring(outcome['prototype']['content'])

            self.assertEqual(
                document.findall('./fastaFiles/FastaFileInfo[1]/fastaFilePath')[0].text,
                self.pipeline.prototype.content['fasta_file']['path'],
            )
            assert len(self.pipeline.data_type.mzxml_files) > 0
            for i in range(len(self.pipeline.data_type.mzxml_files)):
                self.assertEqual(
                    document.findall('./filePaths/string')[i].text,
                    self.data_type.mzxml_files[0].location,
                )


class TestUpdateAPipeline(TestPipelineBase):
    def setUp(self):
        super(TestUpdateAPipeline, self).setUp()

    @freeze_time('2020-06-02 08:57:53')
    def test_update_a_pipeline(self):
        id = str(self.pipeline.id)
        data_type_slug = DataTypeWithProjectFactory.create().slug
        prototype_slug = MaxQuantFactory.create().slug

        self.params = {
            'name': 'Updated Name',
            'description': 'Updated description',
            'data_type': data_type_slug,
            'prototype': prototype_slug,
        }

        with self.client as rdbclient:
            response = rdbclient.put(
                '/v1/pipelines/' + id, headers=self.headers, json=self.params,
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())

            self.assertEqual(outcome['id'], id)
            self.assertEqual(outcome['name'], self.params['name'])
            self.assertEqual(outcome['description'], self.params['description'])
            self.assertEqual(outcome['data_type_slug'], data_type_slug)
            self.assertEqual(outcome['prototype_slug'], prototype_slug)


class TestDeleteAPipeline(TestPipelineBase):
    def setUp(self):
        super(TestDeleteAPipeline, self).setUp()

    @freeze_time('2020-06-02 08:57:53')
    def test_delete_a_pipeline(self):
        id = str(self.pipeline.id)

        with self.client as rdbclient:
            response = rdbclient.delete('/v1/pipelines/' + id, headers=self.headers)

            self.assertEqual(response.status_code, 204)
            self.assertEqual(response.content_type, 'application/json')

            outcome = response.data.decode()
            self.assertEqual(outcome, '')

            outcome = Pipeline.query.filter_by(id=id).first()
            self.assertEqual(outcome, None)


class TestPipelines(TestPipelineBase):
    def setUp(self):
        super(TestPipelines, self).setUp()

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_all_pipelines_without_page_and_per_page_and_direction(self):
        self.pipelines = PipelineFactory.create_batch(size=2)

        with self.client as rdbclient:
            response = rdbclient.get('/v1/pipelines', headers=self.headers)

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            pipelines = outcome['pipelines']

            self.assertTrue(outcome['page'] == 1)
            self.assertTrue(outcome['per_page'] == 2)
            self.assertTrue(outcome['total'] == 3)

            self.assertTrue(len(pipelines) == 2)
            self.assertEqual(pipelines[0]['id'], str(self.pipelines[1].id))

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_pipelines_with_page_1_and_per_page_with_direction_desc(self):
        self.pipelines = PipelineFactory.create_batch(size=2)

        with self.client as rdbclient:
            response = rdbclient.get(
                '/v1/pipelines?page=1&per_page=2&direction=desc', headers=self.headers,
            )

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            pipelines = outcome['pipelines']

            self.assertTrue(outcome['page'] == 1)
            self.assertTrue(outcome['per_page'] == 2)
            self.assertTrue(outcome['total'] == 3)
            self.assertTrue(len(pipelines) == 2)
            self.assertEqual(pipelines[0]['id'], str(self.pipelines[1].id))

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_pipelines_with_page_1_and_per_page_with_direction_asc(self):
        self.pipelines = PipelineFactory.create_batch(size=2)

        with self.client as rdbclient:
            response = rdbclient.get(
                '/v1/pipelines?page=1&per_page=2&direction=asc', headers=self.headers,
            )

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            pipelines = outcome['pipelines']

            self.assertTrue(outcome['page'] == 1)
            self.assertTrue(outcome['per_page'] == 2)
            self.assertTrue(outcome['total'] == 3)
            self.assertTrue(len(pipelines) == 2)
            self.assertTrue(
                re.match(
                    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
                    pipelines[0]['id'],
                )
            )
            self.assertEqual(pipelines[0]['id'], str(self.pipeline.id))

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_pipelines_with_page_2_nd_per_page_with_direction_desc(self):
        self.pipelines = PipelineFactory.create_batch(size=2)

        with self.client as rdbclient:
            response = rdbclient.get(
                '/v1/pipelines?page=2&per_page=2&direction=desc', headers=self.headers,
            )

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            pipelines = outcome['pipelines']

            self.assertTrue(outcome['page'] == 2)
            self.assertTrue(outcome['per_page'] == 2)
            self.assertTrue(outcome['total'] == 3)
            self.assertTrue(len(pipelines) == 1)
            self.assertTrue(
                re.match(
                    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
                    pipelines[0]['id'],
                )
            )
            self.assertEqual(pipelines[0]['id'], str(self.pipeline.id))

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_pipelines_with_page_2_and_per_page_with_direction_asc(self):
        self.pipelines = PipelineFactory.create_batch(size=2)

        with self.client as rdbclient:
            response = rdbclient.get(
                '/v1/pipelines?page=2&per_page=2&direction=asc', headers=self.headers,
            )

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            pipelines = outcome['pipelines']

            self.assertTrue(outcome['page'] == 2)
            self.assertTrue(outcome['per_page'] == 2)
            self.assertTrue(outcome['total'] == 3)
            self.assertTrue(len(pipelines) == 1)
            self.assertEqual(pipelines[0]['id'], str(self.pipelines[1].id))


if __name__ == '__main__':
    unittest.main()
