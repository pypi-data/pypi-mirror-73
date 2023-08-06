"""
Type classes for the protobuf interface IdentityTookit uses
"""

from dataclasses import dataclass
from pure_protobuf.dataclasses_ import field, message
from pure_protobuf.types import int32


@message
@dataclass
class SendVerificationCodeRequest:
    phone_number: str = field(1, default='')


@message
@dataclass
class SendVerificationCodeResponse:
    session_info: str = field(1, default='')


@message
@dataclass
class VerifyPhoneNumberRequest:
    session_info: str = field(1, default='')
    verify_code: str  = field(3, default='')


@message
@dataclass
class VerifyPhoneNumberResponse:
    id_token:      str   = field(1, default='')
    refresh_token: str   = field(2, default='')
    expires_in:    int32 = field(3, default=int32(0))
    user_id:       str   = field(4, default='')
    is_new_user:   int32 = field(5, default=int32(0))
    phone_number:  str   = field(9, default='')


@message
@dataclass
class RefreshTokenRequest:
    grant_type:    str = field(1, default='refresh_token')
    refresh_token: str = field(3, default='')


@message
@dataclass
class RefreshTokenResponse:
    access_token:  str   = field(1, default='')
    expires_in:    int32 = field(2, default='')
    token_type:    str   = field(3, default='')
    refresh_token: str   = field(4, default='')
    id_token:      str   = field(5, default='')
    user_id:       str   = field(6, default='')
    project_id:    int32 = field(7, default='')


class TestTypes():
    # the lengths here are encoded in the byte strings. I don't care enough
    # to pull them out because it's not supposed to be an exhaustive test,
    # just a litmus test
    phone_number = '+000000000000'
    verify_code = '000000'
    session_info = 'A' * 247
    id_token = 'A' * 893
    unknown = 'A' * 226
    user_id = 'A' * 28
    expires_in = 3600
    is_new_user = 0

    @classmethod
    def dotest(self):
        """Test the above functions"""
        test = SendVerificationCodeRequest(self.phone_number).dumps()
        expected = b'\n\r' + self.phone_number.encode()
        assert test == expected

        test = SendVerificationCodeResponse(self.session_info).dumps()
        expected = b'\n\xf7\x01' + self.session_info.encode()
        assert test == expected

        test = VerifyPhoneNumberRequest(
            session_info=self.session_info,
            verify_code=self.verify_code
            ).dumps()
        expected = b'\n\xf7\x01' + self.session_info.encode() \
          + b'\x1a\x06' + self.verify_code.encode()
        assert test == expected

        test = VerifyPhoneNumberResponse(
            id_token=self.id_token,
            unknown=self.unknown,
            expires_in=self.expires_in,
            user_id=self.user_id,
            is_new_user=self.is_new_user,
            phone_number=self.phone_number
                ).dumps()
        expected = b'\n\xfd\x06' + self.id_token.encode()        \
                 + b'\x12\xe2\x01' + self.unknown.encode()       \
                 + b'\x18\x90\x1c"\x1c' + self.user_id.encode()  \
                 + b'(\x00J\r' + self.phone_number.encode()
        assert test == expected
