import vcr

from flask_testing import TestCase

from app.main import db
from manage import app

from app.main.environment import environments

class BaseTestCase(TestCase):
    """ Base Tests """

    OIDC_USER_AUTHORIZATION_CODE = 'AAdzZWNyZXQxaVhnUjsd01ppfTsPu_364mJToVblojMC9tNtT3u9UrcgugtDLjttcZ4EeHGTxlSvN-EB5klzG-xuugi3FVDhnHDAWLJDs9BmH3j2SFcAVWY54Hgnb-emuFgoaQ3yZH43e-UFI8KtqdFIVS-4t0xIdEFkNI71mo7fI1zPOCZhJ_ADCGonYZ4cXarj7rr3qrBUKvgUTDQl_5HSutB07OISfwlFgfGS4X03QYIcvdiyFV4KfHar9OCR7gJZmYhUwcdT4781Y7yBhP55t4GqonSRSChQkkrd522JbTsj2oQ6eyI-I3MsJhYeAC3YTw-fRi_fjhlKSQbKgpRd__AdmOAVuqixuFJXtCsU6kRpmhCzGq-8oSn2XtpG0EmxN1F-COLkynVBzihCEjrzUTigeFA_eDc4r5kZEyoAu8N0PeDO7bGm1agj6r4cfgh8fv69SioNa0Z6j92rWBqie4TNwA-96PnQB6GDdSwCFzlvWf0LvElY56ayBw_tho5YUkYnVZBv23G8pHBzG_DbA7Cr2xq1xQc7lmXnJjPSC18'
    OIDC_USER_ACCESS_TOKEN = 'AAdzZWNyZXQxcQEIz8PEJJF9w7UGptR7Jgzzm3_VIqO5emnGhn7xvedt-A_ldZ-sKnEqFQWXAorX2LljwHrKfGqzZe_Uvp3kqAv5oromTsW9Fbll-cAz1PCYWKE6q43kpuM7jr7a3WOqGt5vxV1ihvN463sF0t3XyC64NWJtDWFVrcHM8mosjArdI1-tVjFXWlEcXzcrvh9entDpkQPrnCucyf4muGa5yvskMJgq5fSsiMLqTvnLvNgVg5qo4XJdiVvIhIiNV8_aTgECiu64_8WTZ3JSyb3Qfmy66Cyt_RbsqeGeoz8E_5Wip48K8Oe-KzPPo1ssk3aAUNw5ZSDDKEsZ-KQapCRwaZYnpKjoHKA6IXCBXZbJjBjEDXiI7XDqJzd7ntr9peScT0aVxVXqtujKW0yR95CH4qyENtEn-swUBiIWVi2dWw4c1t0xrUJdhbUIic15IEOS66LCPKU5ArrxkATbK9OYUNxxlXW3fMNmIzdUs3HmeRgl_hqk4C-gSP8gAj8tTNbF5HrHl0TGjCYipywEHPOfS4UOZ23l'
    OIDC_USER_ID_TOKEN = 'eyJraWQiOiJkZWZhdWx0UlNBU2lnbiIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiamRYVTJTS01RX1lub1JqYmJqOFFPdyIsInN1YiI6IktBWko2Tk0zNUs2NUVDSTU3VEZYNUJUSVFNNEpXMzRGIiwiYXVkIjoibXktY2MtZGV2LXRlc3Qtc3RhZ2luZyIsImF1dGhfdGltZSI6MTU4OTA0Mzg0OCwiaXNzIjoiaHR0cHM6XC9cL2lkcC5taXQuYzMuY2EiLCJleHAiOjE1ODkwNDc0NTIsImlhdCI6MTU4OTA0Mzg1Mn0.TYOzuFCzjVmssYIUJ0YHJiTDtNoEIG_Lj_Qe4J-70fo4c7oY4Lzgami9G1RlErlEFJZdYVPmtYd-9BYrVK1dx3L4aq5C9QvMH-0uIRwvbTZ7ymuLRnjfa3WlxBeKmfs0MPGvXdLdGtPQb4R34LeeubO4NZg2L6pNSLZyjMyUzUly-yP5rV2On286UZxMu1pLxVGpl-KS_tHiSGfoKRsoy7R3tH8-1pYRn2_-V2ydaO4HIwOl9l6WG1wudHD2PQFWuxI0hDP3SqpgT2htzhJ4PmkxSNAzbLqrSg4SIk0cxQmWJhskMTaoxYMBr22tmJz9jctpPJ0blVBif0wYeZ_LpA'
    OIDC_REDIRECT_URI = 'http://localhost:4000/auth/callback'

    def __init__(self, *args, **kwargs):
        super(BaseTestCase, self).__init__(*args, **kwargs)
        self.vcr = vcr.VCR(
            serializer='yaml',
            cassette_library_dir='app/tests/support/cassettes',
            record_mode='once',
            match_on=['uri', 'method'],
        )

    def create_app(self):
        app.config.from_object(environments['test'])
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
