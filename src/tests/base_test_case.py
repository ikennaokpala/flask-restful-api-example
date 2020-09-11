import vcr

from flask_testing import TestCase

from src.main import db
from manage import app

from src.main.environment import environments


class BaseTestCase(TestCase):
    """ Base Tests """

    OIDC_USER_AUTHORIZATION_CODE = 'AAdzZWNyZXQx18RH18UlCrmDnmRN9fRrUcqitGMzfpHqy4PL-7wDrfBkvnkajLeNdnOT4yr49O0wVB5Sekcej0AExfZcBC4M5BJZuzOZepJJ9IC2AiRDGJdYnTSeFTwWKok_ZOcgmOYD9K3254UfXNLffd2BUZ7H0RSGRfpxx7Ga1nMYnNIkH_uGj6H3S2J3BLCotKIwR8ArcGkBNWtum3LExSsJdXH36YV5vS61-E_JGg2CurGpt4RHF4zya6z1081WKL1MqTIombIxR07JSvGlnJMcfLsJaVuN70cCKWS0Wnohl2CB5xNLm9LzDrYWk047mgbYU4aDg5SHUqvP3TimOBwfnaX2S3MCLBPwb5JU49sEMV5JKF2vZ9RNPsWZSj5WgV0MtwBWplpSg5hcwdDxOLEfwVEIvMtpOxsTm_a8PMsrk1aN1Uw9v1rzdzlslwPSFQs_VOze-AAW3XKFUWtNetXLxFvkgOUSeMwks7a-pgCGumLpkOqNvZCjHC1s317-97BCc19lfhORapmFlDVn1O_a5c0gQ5M5beIyZYqqxoKaQgOryvqai0efZKxQnjd8b78YcOx0uTPuzA9df21Db3lhqRAmXys'
    OIDC_USER_ACCESS_TOKEN = 'AAdzZWNyZXQxPJZyTIDvSKK9Yvc4uxbEGUMrOigCWk1TQ1YD-0oeAnRALisozvHVQFIh8116kTMp5RTvEsa2HGpoc6WPj9JW3zZoqdR0i620NHCVU53PAmMQF_6GAraQcdEYyEzfJDlpLLfSNtz9ynjHVVpgFMa8lxowgIejCdTDiUGNc-fLcVF_LCiKWzyRNRziB4a86vymobAshmB1QS1V2Sn9-I6yWRhN3g-oqZFtQXCkaY0ALTQm1E1UA54ZuUd-DDjguxGb8kDLapotL7SdYRoxm4h6zNLgj09IYcOseleZXPcAZnTy62ygtvKye3AZxKgLptpdrJh6-6bZ_eSNH7C0p0rsTFa1UlRBF0vHt3oHvmfIagRtDq9spfg0n6v17kIXp1mm9QdOKpOPeDax8oNECwbulSfg4Au58N4vcWmYwN0I0CR_AJoGr7N6IHnF3cgaT8Iq2tJ2vlofx1SXYdGVuGCX60E9lXNhucbxuOD0cIYLSbVrwxPMpQ_rlEmJ44gfM0H6jrmst9xw_gAJDU6Bu5oA9F7F0GKF6IdFQV8wZjoqYAyvW6AOQuToGPGt5u55D3TA943YEsbaSgLifmfW'
    OIDC_USER_ID_TOKEN = 'eyJraWQiOiJkZWZhdWx0UlNBU2lnbiIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiNXJIZGMzZGlhNVBObXpxMEdLbktaZyIsInN1YiI6IktBWko2Tk0zNUs2NUVDSTU3VEZYNUJUSVFNNEpXMzRGIiwiYXVkIjoicmRiLWRldi10ZXN0LXN0YWdpbmciLCJhdXRoX3RpbWUiOjE1OTEwODgyNTgsImlzcyI6Imh0dHBzOlwvXC9pZHAubWl0LmMzLmNhIiwiZXhwIjoxNTkxMDkxODczLCJpYXQiOjE1OTEwODgyNzN9.U46VZ_tva152ndS73_jJ5M-NNOxeGErGIx9m6sKWbjtwQFMozI7fst2PD18HSWYiqGPYGW_Wap5w1nnUoh0h79LELhi5oww2mVma-swASJ7uKnrUawfN5ZD6NZiDby81jF5U_7jEVKFZ7jK5mvp5S5w8MCAOOlDVwc5JFdox-RXeCgFPac7-BWYsQ9CO_Zcv4NY6PaN3CofTALmAyeI8i4ZEUeSk-xt1VF0jX3V0Jv83acITYtPA7LjB9JIO64ghFKrUqXsQxD6uFeShtHvOJEQtO6TUM7RU8q2suO-znpfyXsbPdZzSeDKdOe0F-QT4p5bTIvBZmfK9B_7xt1Mgdg'
    OIDC_REDIRECT_URI = 'http://localhost:4000/admin/auth/callback'

    def __init__(self, *args, **kwargs):
        super(BaseTestCase, self).__init__(*args, **kwargs)
        self.vcr = vcr.VCR(
            serializer='yaml',
            cassette_library_dir='src/tests/support/cassettes',
            record_mode='once',
            match_on=['uri', 'method'],
        )

    def create_app(self):
        app.config.from_object(environments['test'])
        return app

    def setUp(self):
        self.create_app()
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
