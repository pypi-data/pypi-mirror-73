import requests


class Peedeeff():
    ENDPOINT = 'http://localhost:3000/development/pdf'
    @staticmethod
    def get_pdf(**kwargs):
        return requests.post(Peedeeff.ENDPOINT, json=kwargs)
