import factory

from flask import current_app

from app.main import db
from app.main.models.session import Session
from app.main.models.project import Project
from app.main.models.data_type import DataType
from app.main.models.mzxml_file import MZXmlFile
from app.main.models.metadata_shipment_file import MetadataShipmentFile


class MZXmlFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = MZXmlFile
        sqlalchemy_session = db.session

    name = 'sample'
    extension = 'mzXML'
    location = '/tmp/projects/metabolomics-project-1/5e8ff9bf55ba3508199d22e984129be6_sample.mzXML'
    checksum = '5e8ff9bf55ba3508199d22e984129be6'


class MetadataShipmentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = MetadataShipmentFile
        sqlalchemy_session = db.session

    name = 'sample'
    extension = 'xlsx'
    content = {
        'columns': current_app.config.get('METADATA_SHIPMENTS_FILE_COLUMNS'),
        'rows': {
            '2019-05-07 00:00:00': [
                {
                    'LSARP_SA009': [
                        ['A,1', 'SA', 'QC01'],
                        ['D,6', 'MRSA', 'QC02'],
                        ['A,2', 'SA', 'BI_16_3052'],
                        ['A,3', 'SA', 'BI_16_3054'],
                        ['A,4', 'SA', 'BI_16_3055'],
                        ['A,5', 'SA', 'BI_16_3060'],
                    ],
                    'LSARP_SA010': [
                        ['A,1', 'SA', 'QC01'],
                        ['D,6', 'MRSA', 'QC02'],
                        ['A,2', 'SA', 'BI_16_3490'],
                        ['A,3', 'SA', 'BI_16_3499'],
                        ['A,4', 'SA', 'BI_16_3503'],
                        ['A,5', 'SA', 'BI_16_3520'],
                        ['A,6', 'SA2', 'BI_16_3532'],
                        ['A,7', 'SA', 'BI_16_3555'],
                        ['A,8', 'SA', 'BI_16_3558'],
                        ['A,9', 'MRSA', 'BI_17_0002'],
                        ['A,10', 'SA', 'BI_17_0004'],
                        ['B,1', 'SA', 'BI_17_0006'],
                    ],
                    'LSARP_SA011': [
                        ['A,1', 'SA', 'SA_QC01'],
                        ['D,6', 'MRSA', 'SA_QC02'],
                        ['A,2', 'SA', 'BI_17_0470'],
                        ['A,3', 'SA', 'BI_17_0482'],
                        ['A,4', 'MRSA', 'BI_17_0487'],
                        ['A,5', 'SA', 'BI_17_0499'],
                        ['A,6', 'MRSA', 'BI_17_0508'],
                        ['A,7', 'SA', 'BI_17_0511'],
                        ['A,8', 'SA', 'BI_17_0512'],
                        ['A,9', 'SA', 'BI_17_0513'],
                        ['A,10', 'MRSA', 'BI_17_0516'],
                        ['H,10', 'SA', 'BI_17_0918'],
                    ],
                    'LSARP_SA012': [
                        ['A,1', 'SA', 'SA_QC01'],
                        ['D,6', 'MRSA', 'SA_QC02'],
                        ['A,2', 'SA', 'BI_17_0919'],
                        ['A,3', 'SA', 'BI_17_0926'],
                        ['A,4', 'SA', 'BI_17_0937'],
                        ['A,5', 'SA', 'BI_17_0938'],
                        ['A,6', 'MRSA', 'BI_17_0942'],
                        ['A,7', 'MRSA', 'BI_17_0950'],
                        ['A,8', 'SA', 'BI_17_0973'],
                        ['A,9', 'SA', 'BI_17_0979'],
                        ['A,10', 'SA', 'BI_17_0980'],
                        ['B,1', 'SA', 'BI_17_0982'],
                    ],
                }
            ]
        },
    }


class DataTypeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = DataType
        sqlalchemy_session = db.session

    name = factory.Sequence(lambda n: 'Metabolomics DataType Factory {}'.format(n + 1))
    description = 'A particular kind of data item, as defined by the file formats (mzXML, xlsx) and values it can take in.'
    data_formats = ['mzXML', 'xlsx', 'csv']


class ProjectFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Project
        sqlalchemy_session = db.session

    name = factory.Sequence(lambda n: 'Metabolomics Project {}'.format(n + 1))
    description = 'Very good science based description'
    owner = 'test@example.com'
    collaborators = [
        'collab@ucal.ca',
        'kaylan.horne@westgrid.ca',
        'dev@westgrid.ca',
        'ikenna.okpala@westgrid.ca',
        'swacker@ucalgary.ca',
        'patrick.mann@westgrid.ca',
        'snoskov@ucalgary.ca',
        'ian.lewis2@ucalgary.ca',
        'ian.percel@ucalgary.ca',
        'fridman@ucalgary.ca',
    ]

    @factory.post_generation
    def data_types(project, create, size, **kwargs):
        if not create:
            return

        if size:
            assert isinstance(size, int)

            db.session.add(project)
            db.session.commit()

            DataTypeFactory.create_batch(size=size, project_id=project.id, **kwargs)


class DataTypeWithProjectFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = DataType
        sqlalchemy_session = db.session

    name = factory.Sequence(lambda n: 'Metabolomics DataType Factory {}'.format(n + 1))
    description = 'A particular kind of data item, as defined by the file formats (mzXML, xlsx) and values it can take in.'

    @classmethod
    def _create(_cls, _data_type_model_class, *_args, **_kwargs):
        return ProjectFactory.create(data_types=1).data_types[0]

    @factory.post_generation
    def mzxmls(data_type, create, size, **kwargs):
        if not create:
            return

        if size:
            assert isinstance(size, int)

            db.session.add(data_type)
            db.session.commit()

            MZXmlFactory.create_batch(size=size, data_type_id=data_type.id, **kwargs)

    @factory.post_generation
    def metadata_shipments(data_type, create, size, **kwargs):
        if not create:
            return

        if size:
            assert isinstance(size, int)

            db.session.add(data_type)
            db.session.commit()

            MetadataShipmentFactory.create_batch(
                size=size, data_type_id=data_type.id, **kwargs
            )


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
        code='AAdzZWNyZXQx18RH18UlCrmDnmRN9fRrUcqitGMzfpHqy4PL-7wDrfBkvnkajLeNdnOT4yr49O0wVB5Sekcej0AExfZcBC4M5BJZuzOZepJJ9IC2AiRDGJdYnTSeFTwWKok_ZOcgmOYD9K3254UfXNLffd2BUZ7H0RSGRfpxx7Ga1nMYnNIkH_uGj6H3S2J3BLCotKIwR8ArcGkBNWtum3LExSsJdXH36YV5vS61-E_JGg2CurGpt4RHF4zya6z1081WKL1MqTIombIxR07JSvGlnJMcfLsJaVuN70cCKWS0Wnohl2CB5xNLm9LzDrYWk047mgbYU4aDg5SHUqvP3TimOBwfnaX2S3MCLBPwb5JU49sEMV5JKF2vZ9RNPsWZSj5WgV0MtwBWplpSg5hcwdDxOLEfwVEIvMtpOxsTm_a8PMsrk1aN1Uw9v1rzdzlslwPSFQs_VOze-AAW3XKFUWtNetXLxFvkgOUSeMwks7a-pgCGumLpkOqNvZCjHC1s317-97BCc19lfhORapmFlDVn1O_a5c0gQ5M5beIyZYqqxoKaQgOryvqai0efZKxQnjd8b78YcOx0uTPuzA9df21Db3lhqRAmXys',
    )
