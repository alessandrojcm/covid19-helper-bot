from requests import Response

from app.models import APIService, Config


class EndlessMedicalAPI(APIService):
    base_url: str
    # Exact passphrase to send needed to accept tos as per the docs
    tos_passphrase: str = """I have read, understood and I accept and agree to comply with the Terms of Use of EndlessMedicalAPI and Endless Medical services. The Terms of Use are available on endlessmedical.com"""

    def __init__(self, config: Config):
        super().__init__(config.ENDLESS_MEDICAL_API_URL)

    def analyse(self, session_id: str):
        return self.get("/Analyze", {"SessionID": session_id}).json()

    def add_feature(self, session_id: str, feature_name: str, feature_value: int):
        res = self.post(
            "/UpdateFeature",
            {"SessionID": session_id, "name": feature_name, "value": feature_value},
        )

        return True if res.status_code == 200 else False

    def get_session_token(self) -> str:
        """
            Needed to start the api session
        """
        res = self.get("/InitSession").json()

        return res["SessionID"]

    def accept_tos(self, api_session_id: str):
        """
            Calling this endpoint is required in order to add features to the API
        """
        res: Response = self.post(
            "/AcceptTermsOfUse",
            params={"SessionID": api_session_id, "passphrase": self.tos_passphrase},
        )

        return True if res.status_code == 200 else False
