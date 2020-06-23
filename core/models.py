

class UserDetails(object):
    def __init__(self, twitter_id, api_key, api_secret, access_token, access_token_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.twitter_id = twitter_id

    @staticmethod
    def from_dict(source):
        pass

    def to_dict(self):
        return {
            'twitter_id': self.twitter_id,
            'api_key': self.api_key,
            'api_secret': self.api_secret,
            'access_token': self.access_token,
            'access_token_secret': self.access_token_secret
        }

    def __repr__(self):
        return(
            f'UserDetails(\
                twitter_id={self.twitter_id}, \
                api_key={self.api_key}, \
                api_secret={self.api_secret}, \
                access_token={self.access_token}, \
                access_token_secret={self.access_token_secret}, \
            )'
        )
