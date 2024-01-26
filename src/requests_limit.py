from time import sleep
import logging

request_limit = 5000
default_timeout = 60 * 60 + 5


def check_requests_limit(request_count: int, limit=request_limit, timeout=default_timeout) -> int:
    if request_count >= limit:
        logging.warning(f"The request limit has been exceeded. Pause for an {timeout / 3600:.3f} hours")
        sleep(timeout)

        return 0

    return request_count
