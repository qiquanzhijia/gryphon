
import os
import random
import string

from tornado.gen import coroutine

from server.conf import root_path
from server.conf import upload_path
from server.handlers.api.base import BaseAPIHandler
from server.handlers.api.base import auth_require


class FileHandler(BaseAPIHandler):

    @coroutine
    @auth_require
    def post(self):
        file1 = self.request.files['file1'][0]
        original_fname = file1['filename']
        extension = os.path.splitext(original_fname)[1]
        fname = ''.join(
            random.choice(string.ascii_lowercase + string.digits) for x in
            range(6))
        final_filename = fname + extension
        fpath = os.path.join(upload_path, final_filename)
        output_file = open(fpath, 'wb')
        output_file.write(file1['body'])
        self.write({"path": fpath.replace(root_path, "")})
