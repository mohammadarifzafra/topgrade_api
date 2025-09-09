from ninja import Schema

class LoginSchema(Schema):
    email: str
    password: str

class SignupSchema(Schema):
    fullname: str
    email: str
    password: str
    confirm_password: str

class RequestOtpSchema(Schema):
    email: str

class ResetPasswordSchema(Schema):
    email: str
    otp: str
    new_password: str
    confirm_password: str

class RequestPhoneOtpSchema(Schema):
    phone_number: str

class PhoneSigninSchema(Schema):
    phone_number: str
    otp: str

class RefreshTokenSchema(Schema):
    refresh_token: str