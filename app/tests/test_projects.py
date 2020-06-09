import unittest
import json
import factory
from freezegun import freeze_time

from app.tests.base_test_case import BaseTestCase
from app.main.models.project import Project
from app.tests.support.factories import SessionFactory
from app.tests.support.factories import ProjectFactory

class TestCreateProject(BaseTestCase):
    def setUp(self):
        super(TestCreateProject, self).setUp()
        self.current_session = SessionFactory.create()
        self.email = self.current_session.tokenized_user['email']
        self.expected = { 'slug': 'metabolomics-project-1' }
        self.headers = { 'Authorization': 'Bearer ' + self.current_session.access_token }
        self.params = { 'name': 'Metabolomics Project 1', 'description': 'Very good science based description' }

    @freeze_time('2020-06-02 09:57:54') # After an hour and 1 second
    def test_when_user_access_token_is_expired(self):
        with self.client as rdbclient:
            response = rdbclient.post('/v1/projects', headers=self.headers, json=self.params)

            self.assertEqual(response.status_code, 401)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn\'t understand how to supply the credentials required.')

    def test_when_user_access_token_does_not_exist(self):
        headers = { 'Authorization': 'Bearer access_token_does_not_exist' }

        with self.client as rdbclient:
            response = rdbclient.post('/v1/projects', headers=headers, json=self.params)

            self.assertEqual(response.status_code, 401)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn\'t understand how to supply the credentials required.')

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_a_name_and_description_are_exempted(self):
        with self.client as rdbclient:
            response = rdbclient.post('/v1/projects', headers=self.headers, json={})

            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The browser (or proxy) sent a request that this server could not understand.')

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_a_description_are_exempted(self):
        with self.client as rdbclient:
            response = rdbclient.post('/v1/projects', headers=self.headers, json={ 'name': '' })

            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The browser (or proxy) sent a request that this server could not understand.')

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_a_name_are_exempted(self):
        with self.client as rdbclient:
            response = rdbclient.post('/v1/projects', headers=self.headers, json={ 'description': '' })

            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The browser (or proxy) sent a request that this server could not understand.')

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_with_a_name_and_description_provided(self):
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
            self.assertTrue(outcome.email == self.email)
            self.assertTrue(results.count() == 1)

class TestProjects(TestCreateProject):
    def setUp(self):
        super(TestProjects, self).setUp()

    @freeze_time('2020-06-02 08:57:53')
    def test_fetch_all_projects(self):
        self.projects = ProjectFactory.create_batch(size=2, email=self.email)

        with self.client as rdbclient:
            response = rdbclient.get('/v1/projects', headers=self.headers)

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(len(outcome) == 2)

class TestFetchAProject(TestCreateProject):
    def setUp(self):
        super(TestFetchAProject, self).setUp()

    @freeze_time('2020-06-02 08:57:53')
    def test_fetch_a_project(self):
        self.another_project = ProjectFactory.create(email='another@anotherexample.com')

        with self.client as rdbclient:
            response = rdbclient.get('/v1/projects/metabolomics-project-1', headers=self.headers)

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.expected.update(self.params)
            self.expected.update({ 'email':'another@anotherexample.com' })
            self.assertTrue(outcome == self.expected)

class TestUpdateAProject(TestCreateProject):
    def setUp(self):
        super(TestUpdateAProject, self).setUp()

    @freeze_time('2020-06-02 08:57:53')
    def test_update_a_project(self):
        self.another_project = ProjectFactory.create(email='another@anotherexample.com')
        self.params = { 'name': 'Updated name', 'description': 'Updated desccription' }

        with self.client as rdbclient:
            response = rdbclient.put('/v1/projects/metabolomics-project-1', headers=self.headers, json=self.params)

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome == { 'slug': 'metabolomics-project-1' })

            outcome = Project.query.filter_by(slug=outcome['slug']).first()

            self.assertTrue(outcome.name == self.params['name'])
            self.assertTrue(outcome.description == self.params['description'])

class TestDeleteAProject(TestCreateProject):
    def setUp(self):
        super(TestDeleteAProject, self).setUp()

    @freeze_time('2020-06-02 08:57:53')
    def test_delete_a_project(self):
        self.another_project = ProjectFactory.create(email='another@anotherexample.com')
        with self.client as rdbclient:
            response = rdbclient.delete('/v1/projects/metabolomics-project-1', headers=self.headers)

            self.assertEqual(response.status_code, 204)
            self.assertTrue(response.content_type == 'application/json')

            outcome = response.data.decode()
            self.assertTrue(outcome == '')

            outcome = Project.query.filter_by(slug='metabolomics-project-1').first()
            self.assertTrue(outcome == None)
