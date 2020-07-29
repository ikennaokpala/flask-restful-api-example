import unittest
import json
import factory
from freezegun import freeze_time

from app.tests.base_test_case import BaseTestCase
from app.main.models.project import Project
from app.tests.support.factories import SessionFactory
from app.tests.support.factories import ProjectFactory


class TestProjectBase(BaseTestCase):
    def setUp(self):
        super(TestProjectBase, self).setUp()
        self.current_session = SessionFactory.create()
        self.owner = self.current_session.tokenized_user['email']
        self.expected = {'slug': 'metabolomics-project-1'}
        self.headers = {'Authorization': 'Bearer ' + self.current_session.access_token}
        self.params = {'name': 'Metabolomics Project 1',
                    'description': 'Very good science based description', 'collaborators': ['collab@ucal.ca']}

class TestCreateProject(TestProjectBase):
    @freeze_time('2020-06-02 09:57:54') # After an hour and 1 second
    def test_when_user_access_token_is_expired(self):
        with self.client as rdbclient:
            response = rdbclient.post('/v1/projects', headers=self.headers, json=self.params)

            self.assertEqual(response.status_code, 401)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn\'t understand how to supply the credentials required.')
    
    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_does_not_exist(self):
        headers = { 'Authorization': 'Bearer access_token_does_not_exist' }

        with self.client as rdbclient:
            response = rdbclient.post('/v1/projects', headers=headers, json=self.params)

            self.assertEqual(response.status_code, 401)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn\'t understand how to supply the credentials required.')

    def test_when_authorize_bearer_with_no_access_token_in_header(self):
        headers = { 'Authorization': 'Bearer ' }
        with self.client as rdbclient:
            response = rdbclient.post('/v1/projects', headers=headers, json=self.params)

            self.assertEqual(response.status_code, 401)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn\'t understand how to supply the credentials required.')

    def test_when_authorize_bearer_is_set_empty_in_header(self):
        headers = { 'Authorization': '' }
        with self.client as rdbclient:
            response = rdbclient.post('/v1/projects', headers=headers, json=self.params)

            self.assertEqual(response.status_code, 401)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn\'t understand how to supply the credentials required.')

    def test_when_x_access_token_is_set_empty_in_header(self):
        headers = { 'X-ACCESS-TOKEN': '' }

        with self.client as rdbclient:
            response = rdbclient.post('/v1/projects', headers=headers, json=self.params)

            self.assertEqual(response.status_code, 401)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn\'t understand how to supply the credentials required.')
    
    @freeze_time('2020-06-02 08:57:53')
    def test_when_authorize_bearer_or_x_access_token_isnt_set_in_header(self):
        with self.client as rdbclient:
            response = rdbclient.post('/v1/projects', headers={}, json=self.params)

            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The browser (or proxy) sent a request that this server could not understand.')

    @freeze_time('2020-06-02 08:57:53')
    def test_when_authorize_bearer_isnt_set_but_x_access_token_is_set_in_header(self):
        headers = { 'X-ACCESS-TOKEN': self.current_session.access_token }

        with self.client as rdbclient:
            response = rdbclient.post('/v1/projects', headers=headers, json=self.params)

            self.assertEqual(response.status_code, 201)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome == self.expected)

            results = Project.query.filter_by(slug=outcome['slug'])
            outcome = results.first()
            self.assertTrue(outcome.name == self.params['name'])
            self.assertTrue(outcome.description == self.params['description'])
            self.assertTrue(outcome.collaborators == ['collab@ucal.ca'])
            self.assertTrue(outcome.slug == self.expected['slug'])
            self.assertTrue(outcome.owner == self.owner)
            self.assertTrue(results.count() == 1)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_a_params_are_exempted(self):
        with self.client as rdbclient:
            response = rdbclient.post('/v1/projects', headers=self.headers, json={})

            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The browser (or proxy) sent a request that this server could not understand.')

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_a_description_is_exempted(self):
        with self.client as rdbclient:
            response = rdbclient.post('/v1/projects', headers=self.headers, json={ 'name': 'Metabolomics Project 1' })

            self.assertEqual(response.status_code, 201)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome == self.expected)
            results = Project.query.filter_by(slug=outcome['slug'])
            outcome = results.first()
            self.assertTrue(outcome.name == self.params['name'])
            self.assertTrue(outcome.description == None)
            self.assertTrue(outcome.collaborators == [])
            self.assertTrue(outcome.slug == self.expected['slug'])
            self.assertTrue(outcome.owner == self.owner)
            self.assertTrue(results.count() == 1)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_a_collaborators_is_exempted(self):
        with self.client as rdbclient:
            params = { 'name': 'Metabolomics Project 1', 'description': 'desc' }
            response = rdbclient.post('/v1/projects', headers=self.headers, json=params)

            self.assertEqual(response.status_code, 201)
            self.assertTrue(response.content_type == 'application/json')
            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome == self.expected)
            results = Project.query.filter_by(slug=outcome['slug'])
            outcome = results.first()
            self.assertTrue(outcome.name == self.params['name'])
            self.assertTrue(outcome.description == 'desc')
            self.assertTrue(outcome.collaborators == [])
            self.assertTrue(outcome.slug == self.expected['slug'])
            self.assertTrue(outcome.owner == self.owner)
            self.assertTrue(results.count() == 1)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_a_name_are_exempted(self):
        with self.client as rdbclient:
            response = rdbclient.post('/v1/projects', headers=self.headers, json={ 'description': '' })

            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The browser (or proxy) sent a request that this server could not understand.')

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_with_params_provided(self):
        with self.client as rdbclient:
            response = rdbclient.post('/v1/projects/', headers=self.headers, json=self.params)

            self.assertEqual(response.status_code, 201)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome == self.expected)

            results = Project.query.filter_by(slug=outcome['slug'])
            outcome = results.first()
            self.assertTrue(outcome.name == self.params['name'])
            self.assertTrue(outcome.description == self.params['description'])
            self.assertTrue(outcome.slug == self.expected['slug'])
            self.assertTrue(outcome.owner == self.owner)
            self.assertTrue(results.count() == 1)

class TestProjects(TestProjectBase):
    def setUp(self):
        super(TestProjects, self).setUp()

    @freeze_time('2020-06-02 08:57:53')
    def test_fetch_all_owned_and_collaboarating_projects(self):
        ProjectFactory.create(collaborators=[self.owner], owner='another@email.com')
        ProjectFactory.create(owner='another@email.com')
        ProjectFactory.create(collaborators=['another@email.com'], owner='another@email.com')
        self.projects = ProjectFactory.create_batch(size=2, owner=self.owner)

        with self.client as rdbclient:
            response = rdbclient.get('/v1/projects', headers=self.headers)

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(len(outcome) == 3)
            self.assertTrue(outcome[0]['slug'] == self.projects[1].slug)

class TestFetchAProject(TestProjectBase):
    def setUp(self):
        super(TestFetchAProject, self).setUp()

    @freeze_time('2020-06-02 08:57:53')
    def test_fetch_a_project(self):
        self.another_project = ProjectFactory.create(owner='another@anotherexample.com')

        with self.client as rdbclient:
            response = rdbclient.get('/v1/projects/metabolomics-project-1', headers=self.headers)

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.expected.update(self.params)
            self.expected.update({ 'owner':'another@anotherexample.com', 'mzxml_files': [] })
            outcome.pop('id')
            self.assertTrue(outcome == self.expected)

class TestUpdateAProject(TestProjectBase):
    def setUp(self):
        super(TestUpdateAProject, self).setUp()

    @freeze_time('2020-06-02 08:57:53')
    def test_update_a_project(self):
        self.another_project = ProjectFactory.create(owner='another@anotherexample.com')
        self.params = { 'name': 'Updated name', 'description': 'Updated desccription', 'collaborators': ['update@ucal.ca'] }

        with self.client as rdbclient:
            response = rdbclient.put('/v1/projects/metabolomics-project-1', headers=self.headers, json=self.params)

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome == { 'slug': 'updated-name' })

            outcome = Project.query.filter_by(slug=outcome['slug']).first()

            self.assertTrue(outcome.name == self.params['name'])
            self.assertTrue(outcome.description == self.params['description'])
            self.assertTrue(outcome.collaborators == self.params['collaborators'])

class TestDeleteAProject(TestProjectBase):
    def setUp(self):
        super(TestDeleteAProject, self).setUp()

    @freeze_time('2020-06-02 08:57:53')
    def test_delete_a_project(self):
        self.another_project = ProjectFactory.create(owner='another@anotherexample.com')
        with self.client as rdbclient:
            response = rdbclient.delete('/v1/projects/metabolomics-project-1', headers=self.headers)

            self.assertEqual(response.status_code, 204)
            self.assertTrue(response.content_type == 'application/json')

            outcome = response.data.decode()
            self.assertTrue(outcome == '')

            outcome = Project.query.filter_by(slug='metabolomics-project-1').first()
            self.assertTrue(outcome == None)

if __name__ == '__main__':
    unittest.main()
