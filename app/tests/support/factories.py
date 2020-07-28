import factory

from app.main import db
from app.main.models.session import Session
from app.main.models.project import Project
from app.main.models.raw_file import RawFile


class RawFileFactory(factory.alchemy.SQLAlchemyModelFactory):
	class Meta:
		model = RawFile
		sqlalchemy_session = db.session

	name = 'sample'
	extension = 'mzXML'
	location = '/tmp/projects/metabolomics-project-1/5e8ff9bf55ba3508199d22e984129be6_sample.mzXML'
	checksum = '5e8ff9bf55ba3508199d22e984129be6'

class ProjectFactory(factory.alchemy.SQLAlchemyModelFactory):
	class Meta:
		model = Project
		sqlalchemy_session = db.session

	name = 'Metabolomics Project 1'  
	description = 'Very good science based description'
	owner = 'test@example.com'
	collaborators = ['collab@ucal.ca']

	@factory.post_generation
	def raw_files(project, create, extracted, **kwargs):
		if not create:
			return

		if extracted:
			assert isinstance(extracted, int)

			db.session.add(project)
			db.session.commit()

			RawFileFactory.create_batch(size=extracted, project_id=project.id, **kwargs)

class SessionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Session
        sqlalchemy_session = db.session

    access_token = 'AAdzZWNyZXQxPJZyTIDvSKK9Yvc4uxbEGUMrOigCWk1TQ1YD-0oeAnRALisozvHVQFIh8116kTMp5RTvEsa2HGpoc6WPj9JW3zZoqdR0i620NHCVU53PAmMQF_6GAraQcdEYyEzfJDlpLLfSNtz9ynjHVVpgFMa8lxowgIejCdTDiUGNc-fLcVF_LCiKWzyRNRziB4a86vymobAshmB1QS1V2Sn9-I6yWRhN3g-oqZFtQXCkaY0ALTQm1E1UA54ZuUd-DDjguxGb8kDLapotL7SdYRoxm4h6zNLgj09IYcOseleZXPcAZnTy62ygtvKye3AZxKgLptpdrJh6-6bZ_eSNH7C0p0rsTFa1UlRBF0vHt3oHvmfIagRtDq9spfg0n6v17kIXp1mm9QdOKpOPeDax8oNECwbulSfg4Au58N4vcWmYwN0I0CR_AJoGr7N6IHnF3cgaT8Iq2tJ2vlofx1SXYdGVuGCX60E9lXNhucbxuOD0cIYLSbVrwxPMpQ_rlEmJ44gfM0H6jrmst9xw_gAJDU6Bu5oA9F7F0GKF6IdFQV8wZjoqYAyvW6AOQuToGPGt5u55D3TA943YEsbaSgLifmfW'
    tokenized_user = dict(
        name='First-Name',
        given_name='Given-Name',
        family_name='Family-Name',
        middle_name='Middle-Name',
        nickname='Nick-Name',
        email='test@example.com',
        locale='en',
        access_token='AAdzZWNyZXQxPJZyTIDvSKK9Yvc4uxbEGUMrOigCWk1TQ1YD-0oeAnRALisozvHVQFIh8116kTMp5RTvEsa2HGpoc6WPj9JW3zZoqdR0i620NHCVU53PAmMQF_6GAraQcdEYyEzfJDlpLLfSNtz9ynjHVVpgFMa8lxowgIejCdTDiUGNc-fLcVF_LCiKWzyRNRziB4a86vymobAshmB1QS1V2Sn9-I6yWRhN3g-oqZFtQXCkaY0ALTQm1E1UA54ZuUd-DDjguxGb8kDLapotL7SdYRoxm4h6zNLgj09IYcOseleZXPcAZnTy62ygtvKye3AZxKgLptpdrJh6-6bZ_eSNH7C0p0rsTFa1UlRBF0vHt3oHvmfIagRtDq9spfg0n6v17kIXp1mm9QdOKpOPeDax8oNECwbulSfg4Au58N4vcWmYwN0I0CR_AJoGr7N6IHnF3cgaT8Iq2tJ2vlofx1SXYdGVuGCX60E9lXNhucbxuOD0cIYLSbVrwxPMpQ_rlEmJ44gfM0H6jrmst9xw_gAJDU6Bu5oA9F7F0GKF6IdFQV8wZjoqYAyvW6AOQuToGPGt5u55D3TA943YEsbaSgLifmfW',
        id_token='eyJraWQiOiJkZWZhdWx0UlNBU2lnbiIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiNXJIZGMzZGlhNVBObXpxMEdLbktaZyIsInN1YiI6IktBWko2Tk0zNUs2NUVDSTU3VEZYNUJUSVFNNEpXMzRGIiwiYXVkIjoicmRiLWRldi10ZXN0LXN0YWdpbmciLCJhdXRoX3RpbWUiOjE1OTEwODgyNTgsImlzcyI6Imh0dHBzOlwvXC9pZHAubWl0LmMzLmNhIiwiZXhwIjoxNTkxMDkxODczLCJpYXQiOjE1OTEwODgyNzN9.U46VZ_tva152ndS73_jJ5M-NNOxeGErGIx9m6sKWbjtwQFMozI7fst2PD18HSWYiqGPYGW_Wap5w1nnUoh0h79LELhi5oww2mVma-swASJ7uKnrUawfN5ZD6NZiDby81jF5U_7jEVKFZ7jK5mvp5S5w8MCAOOlDVwc5JFdox-RXeCgFPac7-BWYsQ9CO_Zcv4NY6PaN3CofTALmAyeI8i4ZEUeSk-xt1VF0jX3V0Jv83acITYtPA7LjB9JIO64ghFKrUqXsQxD6uFeShtHvOJEQtO6TUM7RU8q2suO-znpfyXsbPdZzSeDKdOe0F-QT4p5bTIvBZmfK9B_7xt1Mgdg',
        refresh_token=None,
        token_type='bearer',
        expires_in=600,
        redirect_uri='http://localhost:4000/path/to/destination',
        code='AAdzZWNyZXQx18RH18UlCrmDnmRN9fRrUcqitGMzfpHqy4PL-7wDrfBkvnkajLeNdnOT4yr49O0wVB5Sekcej0AExfZcBC4M5BJZuzOZepJJ9IC2AiRDGJdYnTSeFTwWKok_ZOcgmOYD9K3254UfXNLffd2BUZ7H0RSGRfpxx7Ga1nMYnNIkH_uGj6H3S2J3BLCotKIwR8ArcGkBNWtum3LExSsJdXH36YV5vS61-E_JGg2CurGpt4RHF4zya6z1081WKL1MqTIombIxR07JSvGlnJMcfLsJaVuN70cCKWS0Wnohl2CB5xNLm9LzDrYWk047mgbYU4aDg5SHUqvP3TimOBwfnaX2S3MCLBPwb5JU49sEMV5JKF2vZ9RNPsWZSj5WgV0MtwBWplpSg5hcwdDxOLEfwVEIvMtpOxsTm_a8PMsrk1aN1Uw9v1rzdzlslwPSFQs_VOze-AAW3XKFUWtNetXLxFvkgOUSeMwks7a-pgCGumLpkOqNvZCjHC1s317-97BCc19lfhORapmFlDVn1O_a5c0gQ5M5beIyZYqqxoKaQgOryvqai0efZKxQnjd8b78YcOx0uTPuzA9df21Db3lhqRAmXys'
    )
