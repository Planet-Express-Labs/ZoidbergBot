import os

from zoidbergbot.config import MissingEnvironmentVariableError

# ugh, this is such a terrible solution.


nodes = {"us_east":
    {
        "host": "host",
        "port": 2333,
        "rest_uri": "http://host.host:2333",
        "password": "high-security",
        "identifier": "some creative name",
        "region": "us_east or some other discord region."
    }
}

# # Comment this guff out if you don't want to use env variables.
#
# required_vars = []
#
# # ctrl c + ctrl v
# for each in required_vars:
#     # checks each required variable if it exists and raises an exception if it isn't.
#     temp = os.getenv("zoidberg_music_" + each)
#     if temp is None:
#         raise MissingEnvironmentVariableError
#
# host = os.getenv("zoidberg_music_host")
# port = int(os.getenv("zoidberg_music_port"))
# password = os.getenv("zoidberg_music_password")
# region = os.getenv("zoidberg_music_region")
#
# nodes = {"Primary":
#     {
#         "host": host,
#         "port": port,
#         "rest_uri": f"http://{host}:{port}",
#         "password": password,
#         "identifier": region,
#         "region": region
#     }
#
# }
