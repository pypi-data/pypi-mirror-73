import time


class AssertMixin(object):
    def assert_record_and_map_equal(self, record, pairs):
        for key, value in pairs.items():
            if not isinstance(record, dict):
                record_value = getattr(record, key)
            else:
                record_value = record[key]

            self.assertEqual(record_value, value, "key:{}, value:{}, record_value:{}".format(
                key, value, record_value
            ))

    def assert_wait_until(self, assert_func, timeout=20):
        now = int(time.time())
        end = now + timeout
        while 1:

            now = int(time.time())
            if now >= end:
                raise ValueError("Timeout")
            ret = assert_func()
            if ret:
                break
            time.sleep(0.05)
