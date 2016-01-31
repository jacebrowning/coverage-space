# pylint: disable=no-self-use,expression-not-assigned

# TODO: get these tests working

# import sys
# from subprocess import Popen, check_output
#
# from expecter import expect
#
#
# def httpie(args):
#     command = "http " + args
#     print("$ {}".format(command))
#     raw = check_output(command + " --ignore-stdin", shell=True)
#     stdout = raw.decode('utf-8')
#     print(stdout)
#     return stdout
#
# class TestClients:
#
#     @classmethod
#     def setup_class(cls):
#         command = [sys.executable, "manage.py", "server", "--port=5555"]
#         cls.server = Popen(command, env={'CONFIG': 'test'})
#
#     @classmethod
#     def teardown_class(cls):
#         cls.server.terminate()
#
#     def test_httpie(self):
#         """Full integraiton test using HTTPie."""
#
#         expect(httpie("POST localhost:5555/owner/repo/reset")) == \
#             '{"unit": 0.0, "integration": 0.0, "overall": 0.0}'
#
#         expect(httpie("GET localhost:5555/owner/repo")) == \
#             '{"unit": 0.0, "integration": 0.0, "overall": 0.0}'
#
#         expect(httpie("PATCH localhost:5555/owner/repo unit=1")) == \
#             '{"unit": 1.0, "integration": 0.0, "overall": 0.0}'
