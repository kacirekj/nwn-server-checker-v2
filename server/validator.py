import hashlib

from captcha.image import ImageCaptcha
from flask import abort

import context
import constant
import util

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


def validate_captha(request):
    captcha_hash = request.args.get('captchaHash')
    captcha_gues = request.args.get('captchaGues')
    if not captcha_hash or not captcha_gues:
        abort(401, "Missing captcha.")

    md5 = hashlib.md5(captcha_gues.encode('utf-8')).hexdigest()

    is_reused_captcha = captcha_hash in context.used_captcha_hashes
    if is_reused_captcha:
        abort(401, "This captcha has been already used and not guessed correctly.")

    is_captcha_match = md5 == captcha_hash
    if not is_captcha_match:
        context.used_captcha_hashes.add(captcha_hash)
        abort(401, "Incorrect captcha. Please try again.")


def create_captcha():
    while True:
        rand_int = util.generate_random_lowercase_string(3)
        md5 = hashlib.md5(str(rand_int).encode('utf-8')).hexdigest()
        if md5 not in context.used_captcha_hashes:
            break
    data = ImageCaptcha().generate(str(rand_int))
    return data, md5
