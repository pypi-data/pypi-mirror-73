
import logging
import traceback
from urllib.request import Request

logger = logging.getLogger(__name__)


def install():
    # noinspection PyBroadException
    try:
        from urllib.request import OpenerDirector
        from urllib.error import HTTPError

        _open = OpenerDirector.open

        def _agent_open(this: OpenerDirector, fullurl, data, timeout):
            if isinstance(fullurl, str):
                fullurl = Request(fullurl, data)

            try:
                res = _open(this, fullurl, data, timeout)
            except HTTPError as e:
                raise e
            return res

        OpenerDirector.open = _agent_open
    except Exception:
        logger.warning('failed to install plugin %s', __name__)
        traceback.print_exc()