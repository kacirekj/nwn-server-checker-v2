import hashlib

from flask import abort

import constant


def validate_password(request):
    try:
        password = request.args.get('password').encode('utf-8')
        password_sha_3_512 = hashlib.sha3_512(password).hexdigest()
        print(password)
        print(constant.ADMIN_PASSWORD.encode('utf-8'))
        if constant.PASSWORD_SHA_3_512 != password_sha_3_512 and password != constant.ADMIN_PASSWORD.encode('utf-8'):
            raise Exception()
    except:
        abort(401, "Incorrect password. Please contact administrator.")
