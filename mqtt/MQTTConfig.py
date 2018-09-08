from configparser import ConfigParser


class MQTTConfig:
    def __init__(self, config_file_path: str):
        """
        Initialization with configuration file.
        :param config_file_path:
        :type config_file_path: str
        """
        self._config_file_path = config_file_path

        config = ConfigParser()
        config.read(config_file_path)

        self._client_name = config['MQTT']['client_name']
        self._server_name = config['MQTT']['server_name']
        self._server_port = int(config['MQTT']['server_port'])
        self._local_timeout = int(config['MQTT']['local_timeout'])
        self._max_packets = int(config['MQTT']['max_packets'])
        self._username = config['MQTT']['username']
        self._password = config['MQTT']['password']
        self._topic_humidity = config['MQTT']['topic_humidity']
        self._topic_pressure = config['MQTT']['topic_pressure']
        self._topic_temperature = config['MQTT']['topic_temperature']

    @property
    def config_file_path(self) -> str:
        """
        The configuration file path
        :return: The configuration file
        :rtype: str
        """
        return self._config_file_path

    @property
    def client_name(self) -> str:
        """
        The MQTT client name
        :return: The MQTT client name
        :rtype: str
        """
        return self._client_name

    @property
    def server_name(self) -> str:
        """
        The MQTT server name
        :return: The MQTT server name
        :rtype: str
        """
        return self._server_name

    @property
    def server_port(self) -> int:
        """
        The MQTT server port
        :return: The MQTT server port
        :rtype: int
        """
        return self._server_port

    @property
    def local_timeout(self) -> int:
        """
        The timeout to reach the MQTT server
        :return: The timeout to reach the MQTT server
        :rtype: int
        """
        return self._local_timeout

    @property
    def max_packets(self) -> int:
        """
        The maximum number of packets to send to the MQTT server. Not used in library.
        :return: The maximum number of packets to send to the MQTT server
        :rtype: int
        """
        return self._max_packets

    @property
    def username(self) -> str:
        """
        The MQTT server username
        :return: The MQTT server username
        :rtype: str
        """
        return self._username

    @property
    def password(self) -> str:
        """
        The MQTT server password
        :return: The MQTT server password
        :rtype: str
        """
        return self._password

    @property
    def topic_humidity(self) -> str:
        """
        The MQTT server topic for humidity data
        :return: The MQTT server topic for humidity data
        :rtype: str
        """
        return self._topic_humidity

    @property
    def topic_pressure(self) -> str:
        """
        The MQTT server topic for pressure data
        :return: The MQTT server topic for pressure data
        :rtype: str
        """
        return self._topic_pressure

    @property
    def topic_temperature(self) -> str:
        """
        The MQTT server topic for temperature data
        :return: The MQTT server topic for temperature data
        :rtype: str
        """
        return self._topic_temperature

    def __repr__(self):
        """
        Return a string representation of the MQTT object.
        :return: A string representation of the MQTT object.
        """
        return '<MQTTConfig: server: {self.server_name}:{self.server_port:d}>'
