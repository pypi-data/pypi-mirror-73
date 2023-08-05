from requests import Session
import json


class WorkersKV:
    _endpoint = "https://api.cloudflare.com/client/v4/accounts" \
                "/{account_identifier}/storage/kv/namespaces/{namespace}"

    def __init__(self, account_id, namespace, token, email):
        self._endpoint = self._endpoint.format(account_identifier=account_id, namespace=namespace)
        self._s = Session()
        self._s.headers.update({"X-Auth-Email": email, "X-Auth-Key": token})

    @staticmethod
    def _handle_result(result, return_result=True):
        is_success = result.get('success')
        if not is_success:
            raise WorkersKVError(result.get('errors'))
        elif return_result:
            return result.get('result')

    @property
    def ls(self):
        return self._handle_result(self._s.get(f"{self._endpoint}/keys").json())

    @property
    def endpoint(self):
        return self._endpoint

    def __setitem__(self, key, value):
        if not (isinstance(value, dict) or isinstance(value, list)):
            raise TypeError("Expecting a list or dict")
        data = json.dumps(value, ensure_ascii=False).encode('utf-8')
        self._handle_result(
            self._s.put(f"{self._endpoint}/values/{key}", data=data).json(),
            False
        )

    def __getitem__(self, item):
        r = self._s.get(f"{self._endpoint}/values/{item}")
        r.encoding = 'utf-8'
        loaded = json.loads(r.text)
        if isinstance(loaded, dict) and (error := loaded.get('errors')):
            raise WorkersKVError(error)
        return loaded


class WorkersKVError(Exception):
    pass
