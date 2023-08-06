"""
Interface with the Lex API.
Based on reverse engineered data collated in early 2020.

Throw bug reports at alexandria@inventati.org
"""

from typing import NoReturn
import requests
from lexapi import lextypes


class LexAPI():
    """Lex API interface class"""
    IdentityToolkitURL = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/"  # noqa
    LexPersonalsURL = "https://us-central1-personals-personals.cloudfunctions.net/"  # noqa
    SecureTokenURL = "https://securetoken.googleapis.com/v1/token"

    LexFirebaseKey = "AIzaSyCnKtpgV7NFp_nnVRK_UZZn4eEk8xrg4R4"

    # It's exceedingly difficult to find any information on X-Goog-Spatula.
    # The authflow _requires_ it to work. It seems to be base64-encoded
    # protobuf with some info about the app and very likely the device or
    # certificate information. I have some notes on the observed requirements
    # gathered from a couple of observations but there are a fair bunch of
    # unknowns still. I really hope that putting this here doesn't disclose
    # any crypto secrets!

    IdentityToolkitHeadData = {
        'Content-Type':   'application/x-protobuf',
        'X-Goog-Spatula': 'CiwKDHVzLnBlcnNvbmFscxocMzU1eFZ3YTZzbXZ3Wm4rVH'
                          'JnekpqT21KOHlvPRIgvrfcb9eTNKiDMBtydVhumqMYABmL'
                          'I4BXyS/iZEj2zUoY94bilIqB0OQxIM2g8YOy4IjGHipZAF'
                          '5qgJxXh8oIIlZBJwIx52UqKjiVYHdIBODVIFAlXyNs0VIl'
                          '9juRH0z0ZNb8ekaiaHbf5I7K9fMhyacHTZxvPQnfY2ZxWH'
                          'ozQpmYWXqZROLpZfM662Al71I='
    }
    IdentityToolkitQueryData = {'alt': 'proto', 'key': LexFirebaseKey}

    def __init__(self):
        self.tokens = {}
        self.user_data = {}

    def user_id(self) -> str:
        "Return the cached user_id"
        return self.user_data['id']

    def save_tokens(self) -> dict:
        """
        Return the tokens we have. This allows you to serialize this to a file,
        so you don't have to ask the user to log in every single time, and can
        just run

            ...
            lex.load_tokens(tokens_dict)
            lex.refresh_tokens()
            lex.get_user()
            ...

        on app start.

        """
        return self.tokens

    def load_tokens(self, tokens: dict = None) -> NoReturn:
        """
        Return the tokens we have. This allows you to serialize this to a file,
        so you don't have to ask the user to log in every single time, and can
        just run

            ...
            lex.load_tokens(tokens_dict)
            lex.refresh_tokens()
            lex.get_user()
            ...

        on app start.

        """
        if tokens:
            self.tokens = tokens

    def send_verification_code(self, phone_number: str) -> NoReturn:
        """
        Request an account verification code to be sent to the given phone

        This is the first step of the authentication handshake.
        """
        url   = self.IdentityToolkitURL + 'sendVerificationCode'
        head  = self.IdentityToolkitHeadData
        query = self.IdentityToolkitQueryData
        body = lextypes.SendVerificationCodeRequest(phone_number).dumps()

        r = requests.post(url, params=query, data=body, headers=head)
        if r.status_code == 200:
            # requests doesn't actually document .content
            # it's MUCH easier than using read()
            # See requests/requests/models.py line 854

            data = lextypes.SendVerificationCodeResponse.loads(r.content)
            self.tokens['IdentityKitSessionInfo'] = data.session_info

        r.raise_for_status()

    def verify_phone_number(self, verify_code: str) -> NoReturn:
        """
        Authenticate using the phone number and authentication code sent to it

        This is the second and last step of the authentication handshake.
        """
        if not verify_code:
            raise ValueError("verify_code must be provided.")

        url   = self.IdentityToolkitURL + 'verifyPhoneNumber'
        head  = self.IdentityToolkitHeadData
        query = self.IdentityToolkitQueryData
        body  = lextypes.VerifyPhoneNumberRequest(
            session_info=self.tokens['IdentityKitSessionInfo'],
            verify_code=verify_code
        ).dumps()

        r = requests.post(url, params=query, data=body, headers=head)
        if r.status_code == 200:
            data = lextypes.VerifyPhoneNumberResponse.loads(r.content)
            self.user_data['id'] = data.user_id
            self.tokens['refresh_token'] = data.refresh_token
            self.tokens['id_token'] = data.id_token

        r.raise_for_status()

    def refresh_tokens(self) -> NoReturn:
        """
        Refresh the authentication tokens we have.
        If you've stored the authentication tokens to a file, you should run
        get_user() afterwards, so you can obtain the filters for the feed data.
        """
        url   = self.SecureTokenURL
        head  = self.IdentityToolkitHeadData
        query = self.IdentityToolkitQueryData
        body  = lextypes.RefreshTokenRequest(
            grant_type='refresh_token',
            refresh_token=self.tokens['refresh_token']
        ).dumps()

        r = requests.post(url, params=query, data=body, headers=head)
        if r.status_code == 200:
            data = lextypes.RefreshTokenResponse.loads(r.content)
            self.tokens['id_token'] = data.id_token
            self.user_data['id'] = data.user_id

        r.raise_for_status()

    def get_user(self, user_id: str = None) -> dict:
        """
        Return a dict containing the user's account data.
        This data is also stored internally so the get_feed function can
        default on the latitude, longitude, maxAge, distance, and query filters

        Defaults to the user_id returned via verify_phone_number
        """
        user_id = user_id or self.user_id()

        url   = self.LexPersonalsURL + 'getUser'
        head  = {'authorization': 'Bearer ' + self.tokens['id_token']}
        query = {'id': user_id}

        r = requests.get(url, params=query, headers=head)
        if r.status_code == 200:
            account = r.json()
            self.user_data['latitude']  = account['location']['latitude']
            self.user_data['longitude'] = account['location']['longitude']
            self.user_data['max_age']   = account['settings']['savedFilters']['ageMax'] # noqa
            self.user_data['distance']  = account['settings']['savedFilters']['distanceInMeters'] # noqa
            self.user_data['keywords']  = account['settings']['savedFilters']['searchQuery'] # noqa
            return account

        r.raise_for_status()
        return None

    def get_feed(self, filters: dict = None) -> list: # noqa
        """
        Return a list containing the posting feed for the current user,
        filtered by the filters dict. The filters dict looks like:

        {
            'latitude': int,
            'longitude': int,
            'max_age': int,
            'distance': int,
            'keywords': "keyworda, keywordb, ..."
        }

        Any or all of those keys can be missing from the dict, it's also
        acceptable to pass no argument. If get_user has been previously called,
        we default to the values set in the current user's profile, otherwise,
        integer arguments default to 0, and string arguments default to the
        empty string.
        """
        if not filters:
            filters = {}

        latitude  = filters.get('latitude',  self.user_data['latitude'])
        longitude = filters.get('longitude', self.user_data['longitude'])
        max_age   = filters.get('max_age',   self.user_data['max_age'])
        distance  = filters.get('distance',  self.user_data['distance'])
        keywords  = filters.get('keywords',  self.user_data['keywords'])

        url   = self.LexPersonalsURL + 'getFeed'
        head  = {'authorization': 'Bearer ' + self.tokens['id_token']}
        query = {
            'maxAge': max_age,
            'latitude': latitude,
            'longitude': longitude,
            'distance': distance,
            'query': keywords
        }

        r = requests.get(url, params=query, headers=head)
        if r.status_code == 200:
            self.user_data['feed'] = r.json()
            return r.json()

        r.raise_for_status()
        return None

    def get_likes_feed(self, user_id: str = None) -> list:
        """
        Return a list containing the user's likes feed

        user_id defaults to the user currently logged in
        """
        user_id = user_id or self.user_id()

        url   = self.LexPersonalsURL + 'getLikesFeed'
        head  = {'authorization': 'Bearer ' + self.tokens['id_token']}
        query = {'userId': user_id}

        r = requests.get(url, params=query, headers=head)
        if r.status_code == 200:
            return r.json()

        r.raise_for_status()
        return None

    def get_user_likes(self, user_id: str = None) -> list:
        """
        Return a list containing user ids for people who have liked the
        user's posts.

        user_id defaults to the user currently logged in
        """
        user_id = user_id or self.user_id()

        url   =  self.LexPersonalsURL + 'getLikesFeed'
        head  = {'authorization': 'Bearer ' + self.tokens['id_token']}
        query = {'userId': user_id}

        r = requests.get(url, params=query, headers=head)
        if r.status_code == 200:
            return r.json()

        r.raise_for_status()
        return None

    def get_user_favorites(self, user_id: str = None) -> list:
        """
        Return a list containing post data for the posts the user has liked

        user_id defaults to the user currently logged in
        """
        user_id = user_id or self.user_id()

        url = self.LexPersonalsURL + 'getUserFavorites'
        head  = {'authorization': 'Bearer ' + self.tokens['id_token']}
        query = {'userId': user_id}

        r = requests.get(url, params=query, headers=head)
        if r.status_code == 200:
            print(r.content)
            return r.json()

        r.raise_for_status()
        return None

    def get_user_posts(self, user_id: str = None) -> list:
        """
        Return a list containing the user's posts

        user_id defaults to the user currently logged in
        """
        user_id = user_id or self.user_id()

        url   = self.LexPersonalsURL + 'getUserPosts'
        head  = {'authorization': 'Bearer ' + self.tokens['id_token']}
        query = {'userId': user_id}

        r = requests.get(url, params=query, headers=head)
        if r.status_code == 200:
            return r.json()

        r.raise_for_status()
        return None

    def get_user_post(self, post_id: str = None) -> list:
        """
        Return the given post object

        user_id defaults to the user currently logged in
        """
        if not post_id:
            raise ValueError("post_id cannot be None, give us a string.")

        url   = self.LexPersonalsURL + 'getPost'
        head  = {'authorization': 'Bearer ' + self.tokens['id_token']}
        query = {'id': post_id}

        r = requests.get(url, params=query, headers=head)
        if r.status_code == 200:
            return r.json()

        r.raise_for_status()
        return None

    def get_user_chats_v2(self) -> list:
        """
        Return a list containing the user's most recent messages and the
        profiles of the users in the conversation
        """
        url   = self.LexPersonalsURL + 'getUserChatsV2'
        head  = {'authorization': 'Bearer ' + self.tokens['id_token']}

        r = requests.get(url, headers=head)
        if r.status_code == 200:
            return r.json()

        r.raise_for_status()
        return None

    def get_mutually_blocked_users(self, user_id: str = None) -> list:
        """
        Return a list containing profile data for the user's blocklist

        user_id defaults to the user currently logged in
        """
        user_id = user_id or self.user_id()

        url   = self.LexPersonalsURL + 'getMutuallyBlockedUsers'
        head  = {'authorization': 'Bearer ' + self.tokens['id_token']}
        query = {'user_id': user_id}

        r = requests.get(url, params=query, headers=head)
        if r.status_code == 200:
            return r.json()

        r.raise_for_status()
        return None

    def is_username_available(self, username: str, user_id: str = None) -> dict: # noqa
        """
        Return a dict containing a single key/value ("available"/boolean)
        answering whether the username is available or not

        user_id defaults to the user currently logged in
        """
        user_id = user_id or self.user_id()

        url   = self.LexPersonalsURL + 'usernameAvailable'
        head  = {'authorization': 'Bearer ' + self.tokens['id_token']}
        query = {
            'userId': user_id,
            'username': username
        }

        r = requests.get(url, params=query, headers=head)
        if r.status_code == 200:
            return r.json()

        r.raise_for_status()
        return None

    def update_user(self, user_data: dict = None) -> dict:
        """
        Update the user object stored by the Lex servers.
        Requires a valid and unexpired fcmToken. Generally you can
        get that by running get_user(), modifying the object,
        and posting the same object back
        """
        if not user_data:
            raise ValueError("You have to provide a user_data dictionary")

        url  = self.LexPersonalsURL + 'updateUser'
        head = {'authorization': 'Bearer ' + self.tokens['id_token']}
        body = user_data

        r = requests.post(url, json=body, headers=head)
        if r.status_code == 200:
            return r.json()

        r.raise_for_status()
        return None
