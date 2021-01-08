from unittest import TestCase
from unittest.mock import *
from redis_sentinel_connector.redis_connector import RedisConnector


class RedisConnectorTestCase(TestCase):
    @patch('redis_sentinel_connector.redis_connector.TYPE', 'TEST')
    @patch('redis_sentinel_connector.redis_connector.REDIS_URL',
           'sentinel://:testefoobar@host1.sentinel.domain.com:26379,'
           'host2.sentinel.domain.com:26379,'
           'host3-155915407905.sentinel.domain.com:26379/service_name:redisservice')
    def setUp(self):
        self.redis_connector = RedisConnector()

    def test_connect_ping_should_return_true(self):
        redis_connection = self.redis_connector.connect()
        self.assertTrue(redis_connection.ping())

    def test_get_hosts_from_redis_url_must_return_3_hosts(self):
        hosts = self.redis_connector.get_hosts_from_redis_url()
        expected_host0 = "host1.sentinel.domain.com:26379"
        self.assertEqual(3, len(hosts))
        self.assertEqual(expected_host0, hosts[0])

    def test_extract_port_from_host_must_return_number_after_colon(self):
        host = "host1.sentinel.domain.com:26379"
        expected_port = "26379"
        self.assertEqual(expected_port, self.redis_connector.extract_port_from_host(host))

    def test_get_service_name_must_return_string_after_last_colon(self):
        expected_service_name = "redisservice"
        self.assertEqual(expected_service_name, self.redis_connector.get_service_name())

    def test_get_password_must_return_string_between_second_colon_and_at_symbol(self):
        expected_password = "testefoobar"
        self.assertEqual(expected_password, self.redis_connector.get_password())


class RedisConnectorExceptionTestCase(TestCase):
    @patch('redis_sentinel_connector.redis_connector.TYPE', None)
    @patch('redis_sentinel_connector.redis_connector.REDIS_URL', None)
    def test_when_type_environment_not_defined_and_redis_url_not_defined_should_make_exception(self):
        conn = RedisConnector()
        self.assertRaises(Exception, conn.connect)
