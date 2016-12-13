# server.py
from inet import module, package

patients = package('patients')
auth = module(patients, 'auth')

@auth.send
def verify_token(token):
    return False

@auth.send
def get_user(token):
    return None


# client.py
from inet import function

verify = function('patients.auth.verify_token')


if __name__ == '__main__':
    tok = get_token()
    if verify(tok):
        print('Logged in successfully')

