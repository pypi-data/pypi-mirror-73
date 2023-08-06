from collections import namedtuple
import os
import base64
import json
import logging
from datetime import datetime


import requests
from requests.exceptions import RequestException
import jwt


class AppStoreConnectException(Exception):
    pass


logger = logging.getLogger()
Bundle = namedtuple("Bundle", "prov_name prov_data cert_name cert_data bundle_id")


class AppStoreConnect:
    def __init__(self) -> None:
        self.key_id = os.environ["APPLE_KEY_ID"]
        self.issuer_id = os.environ["APPLE_ISSUER_ID"]
        self.private_key = base64.b64decode(os.environ["APPLE_KEYDATA"])
        self.headers = {
            'alg': 'ES256',
            'kid': self.key_id,
            'typ': 'JWT'
        }
        self.base_url = 'https://api.appstoreconnect.apple.com/v1'

    def _prep_headers(self):
        payload = {
            'iss': self.issuer_id,
            'exp': int(datetime.now().strftime("%s")) + 60 * 5,
            'aud': 'appstoreconnect-v1'
        }
        token = jwt.encode(payload, self.private_key, algorithm='ES256', headers=self.headers)
        return {'Authorization': 'Bearer %s' % token.decode('utf-8')}

    def add_device(self, udid, name):
        url = '{}/devices'.format(self.base_url)
        data = {
            'data': {
                'type': 'devices',
                'attributes': {
                    'name': name,
                    'udid': udid,
                    'platform': 'IOS'
                }
            }
        }
        req = requests.post(url, headers=self._prep_headers(), json=data)
        if req.status_code != 201:
            raise AppStoreConnectException(req.status_code)

    def list_devices(self):
        url = '{}/devices'.format(self.base_url)
        req = requests.get(url, headers=self._prep_headers())
        print(req.status_code)
        print(req.json())

    def get_first_distr_certificate(self) -> dict:
        url = f'{self.base_url}/certificates'
        params = {"filter[certificateType]": "IOS_DISTRIBUTION"}
        resp = requests.get(url, headers=self._prep_headers(), params=params)
        if resp.status_code == 200:
            return resp.json()['data'][0]

    def _get_profiles(self, type):
        url = f'{self.base_url}/profiles'
        params = {
            "filter[profileState]": "ACTIVE",
        }
        if type == 'adhoc':
            params.update({"filter[profileType]": "IOS_APP_ADHOC"})
        resp = requests.get(url, headers=self._prep_headers(), params=params)
        if resp.status_code == 200:
            return resp.json()['data']
        logger.error(resp)
        raise AppStoreConnectException

    def get_device_info(self, dev_id):
        url = '{}/devices/{}'.format(self.base_url, dev_id)
        req = requests.get(url, headers=self._prep_headers())
        print(req.text)

    def apps(self):
        url = '{}/apps'.format(self.base_url)
        print(url)
        print(self._prep_headers())
        try:
            req = requests.get(url, headers=self._prep_headers())
            if req.status_code != 200:

                raise AppStoreConnectException
        except RequestException as e:
            raise AppStoreConnectException(e)

    def get_bundle(self, bundle_id, type) -> Bundle:
        # грязный код:)
        profiles = self._get_profiles(type)
        for profile in profiles:
            # get bundle id info
            resp = requests.get(profile['relationships']['bundleId']['links']['related'], headers=self._prep_headers())
            if resp.json()['data']['attributes']['identifier'] == bundle_id:
                resp = requests.get(profile['relationships']['certificates']['links']['related'], headers=self._prep_headers())
                bundle = Bundle(
                    cert_name=resp.json()['data'][0]['attributes']['name'],
                    cert_data=base64.b64decode(resp.json()['data'][0]['attributes']['certificateContent']),
                    prov_name=profile['attributes']['name'],
                    prov_data=base64.b64decode(profile['attributes']['profileContent']),
                    bundle_id=bundle_id
                )
        if bundle:
            return bundle


if __name__ == '__main__':
    conn = AppStoreConnect()
    bundle = conn.get_bundle("io.neurohive.bncstage", "adhoc")
    with open('cert.pem', 'wb') as fp:
        fp.write(bundle.cert_data)
    with open('provis.pem', 'wb') as fp:
        fp.write(bundle.prov_data)
