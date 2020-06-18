import unittest

from app.main import db
from app.main.models.project import Project
from app.tests.base_test_case import BaseTestCase
from app.tests.support.factories import ProjectFactory

class TestSlugifyingProject(BaseTestCase):
    def setUp(self):
        super(TestSlugifyingProject, self).setUp()
        self.project = ProjectFactory.create()

    def test_when_new_project_is_created(self):
        self.project = ProjectFactory.create(name='New Project')

        outcome = Project.query.order_by(Project.id.desc()).first()
        self.assertEqual(outcome.slug, 'new-project')

    def test_when_new_project_is_created_with_the_same_name_with_an_existing_project(self):
        ProjectFactory.create(name='Project Name Already Taken')
        self.project = ProjectFactory.create(name='Project Name Already Taken')

        outcome = Project.query.order_by(Project.id.desc()).first()
        self.assertEqual(outcome.slug, 'project-name-already-taken-1')

    def test_when_new_project_is_created_with_the_same_name_with_an_existing_projects(self):
        ProjectFactory.create(name='Project Name Already Taken')
        ProjectFactory.create(name='Project Name Already Taken')
        self.project = ProjectFactory.create(name='Project Name Already Taken')

        outcome = Project.query.order_by(Project.id.desc()).first()
        self.assertEqual(outcome.slug, 'project-name-already-taken-2')

    def test_when_existing_project_name_is_updated(self):
        project = Project.query.first()
        project.name = 'Updated Project Name'

        db.session.flush()
        db.session.commit()

        outcome = Project.query.order_by(Project.id.desc()).first()
        self.assertEqual(outcome.name, 'Updated Project Name')
        self.assertEqual(outcome.slug, 'updated-project-name')

    def test_when_existing_project_name_is_updated_with_the_same_name_with_an_existing_project(self):
        ProjectFactory.create(name='Project Name Already Taken')
        self.project = ProjectFactory.create(name='Another Project Name')

        project = Project.query.order_by(Project.id.desc()).first()
        project.name = 'Project Name Already Taken'

        db.session.flush()
        db.session.commit()

        outcome = Project.query.order_by(Project.id.desc()).first()
        self.assertEqual(outcome.name, 'Project Name Already Taken')
        self.assertEqual(outcome.slug, 'project-name-already-taken-1')

    def test_when_existing_project_name_is_updated_with_the_same_name_with_an_existing_projects(self):
        ProjectFactory.create(name='Project Name Already Taken')
        ProjectFactory.create(name='Project Name Already Taken')
        self.project = ProjectFactory.create(name='Another Project Name')

        project = Project.query.order_by(Project.id.desc()).first()
        project.name = 'Project Name Already Taken'

        db.session.flush()
        db.session.commit()

        outcome = Project.query.order_by(Project.id.desc()).first()
        self.assertEqual(outcome.name, 'Project Name Already Taken')
        self.assertEqual(outcome.slug, 'project-name-already-taken-2')
