import requests

from memfault_cli.authenticator import Authenticator
from memfault_cli.context import MemfaultCliClickContext


class MemfaultChunk:
    def __init__(self, ctx: MemfaultCliClickContext, authenticator: Authenticator):
        self.ctx = ctx
        self.authenticator = authenticator

    def post(self, data: bytes):
        url = f"{self.ctx.chunks_url}/api/v0/chunks/{self.ctx.device_serial}"

        request_args = self.authenticator.requests_auth_params()
        request_args["headers"]["Content-Type"] = "application/octet-stream"
        response = requests.post(url, data=data, **request_args)
        if response.status_code >= 400:
            raise Exception(
                f"Request failed with HTTP status {response.status_code}\nResponse body:\n{response.content.decode()}"
            )
