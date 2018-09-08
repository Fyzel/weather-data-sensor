from configparser import ConfigParser
from datetime import datetime
from decimal import Decimal

import paho.mqtt.client as mqtt
from mqtt.MQTTConfig import MQTTConfig

# see https://learn.adafruit.com/adafruit-bme280-humidity-barometric-pressure-temperature-sensor-breakout/python-circuitpython-test
import board
import busio
import time
import adafruit_bme280


class App:
    def __init__(self):
        pass

    @staticmethod
    def on_connect(client, userdata, flags, rc) -> None:
        """
        The callback for when the client receives a CONNACK response from the server.

        :param client: The client instance for this callback
        :param userdata: The private user data as set in Client() or userdata_set()
        :param flags: Response flags sent by the broker
        :param rc: The connection result
        """
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("$SYS/#")

    @staticmethod
    def on_disconnect(client, userdata, rc) -> None:
        """
        Called when the MQTT client disconnects.

        :param client: The client instance for this callback
        :param userdata: The private user data as set in Client() or userdata_set()
        :param rc:
        :return:
        """
        if rc != 0:
            print('Unexpected disconnection. Reconnecting.')
            client.reconnect()

    @staticmethod
    def on_publish(client, userdata, mid) -> None:
        """
        Called when a message that was to be sent using the publish() call has completed transmission to the broker.

        :param client: The client instance for this callback
        :param userdata: The private user data as set in Client() or userdata_set()
        :param mid: The mid variable returned from corresponding publish() call to allow outgoing messages to be tracked
        """
        print('published {userdata} (mid: {mid})'.format(userdata=userdata, mid=mid))

    @staticmethod
    def main():
        """
        Main executable method.

        :return:
        """
        config = ConfigParser()
        config.read('config.ini')

        elevation = Decimal(config['GPS']['elevation'])
        elevation_units = config['GPS']['elevation_units']
        latitude = Decimal(config['GPS']['latitude_decimal'])
        longitude = Decimal(config['GPS']['longitude_decimal'])

        device_humidity_error_range = Decimal(config['Device']['humidity_error_range'])
        device_pressure_error_range = Decimal(config['Device']['pressure_error_range'])
        device_temperature_error_range = Decimal(config['Device']['temperature_error_range'])

        wait_time = int(config['Readings']['wait_time_seconds'])

        # Create library object using our Bus I2C port
        i2c = busio.I2C(board.SCL, board.SDA)
        bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
        # OR create library object using our Bus SPI port
        # spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        # bme_cs = digitalio.DigitalInOut(board.D10)
        # bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, bme_cs)

        # change this to match the location's pressure (hPa) at sea level
        bme280.sea_level_pressure = Decimal(config['Readings']['location_sea_level_pressure'])

        mqtt_config = MQTTConfig(config_file_path='config.ini')

        mqtt_client = mqtt.Client()
        mqtt_client.on_connect = App.on_connect
        mqtt_client.on_disconnect = App.on_disconnect
        mqtt_client.on_publish = App.on_publish

        mqtt_client.connect(host=mqtt_config.server_name,
                            port=mqtt_config.server_port,
                            keepalive=mqtt_config.local_timeout)
        mqtt_client.username_pw_set(username=mqtt_config.username,
                                    password=mqtt_config.password)

        while True:
            temperature = bme280.temperature
            pascals = bme280.pressure
            kilopascals = pascals / 1000.0
            humidity = bme280.humidity
            timestamp = datetime.utcnow()

            humidity_reading = '''{{
        "value": {humidity:.4f},
        "value_units": "percent",
        "value_error_range": {humidity_error_range:.6f},
        "timestamp": "{datetime}Z",
        "elevation": {elevation:.4f},
        "elevation_units": "{elevation_units}",
        "latitude": {latitude:.6f},
        "longitude": {longitude:.6f}
    }}'''.format(humidity=humidity,
                 humidity_error_range=device_humidity_error_range,
                 datetime=timestamp.isoformat(),
                 elevation=elevation,
                 elevation_units=elevation_units,
                 latitude=latitude,
                 longitude=longitude)

            pressure_reading = '''{{
        "value": {pressure:.4f},
        "value_units": "kPa",
        "value_error_range": {pressure_error_range:.6f},
        "timestamp": "{datetime}Z",
        "elevation": {elevation:.4f},
        "elevation_units": "{elevation_units}",
        "latitude": {latitude:.6f},
        "longitude": {longitude:.6f}
    }}'''.format(pressure=kilopascals,
                 pressure_error_range=device_pressure_error_range,
                 datetime=timestamp.isoformat(),
                 elevation=elevation,
                 elevation_units=elevation_units,
                 latitude=latitude,
                 longitude=longitude)

            temperature_reading = '''{{
        "value": {temperature:.4f},
        "value_units": "C",
        "value_error_range": {temperature_error_range:.6f},
        "timestamp": "{datetime}Z",
        "elevation": {elevation:.4f},
        "elevation_units": "{elevation_units}",
        "latitude": {latitude:.6f},
        "longitude": {longitude:.6f}
    }}'''.format(temperature=temperature,
                 temperature_error_range=device_temperature_error_range,
                 datetime=timestamp.isoformat(),
                 elevation=elevation,
                 elevation_units=elevation_units,
                 latitude=latitude,
                 longitude=longitude)

            (humidity_mqtt_result, humidity_mid) = mqtt_client.publish(topic=mqtt_config.topic_humidity,
                                                                       payload=humidity_reading,
                                                                       qos=2,
                                                                       retain=True)
            mqtt_client.loop(timeout=mqtt_config.local_timeout,
                             max_packets=mqtt_config.max_packets)
            (pressure_mqtt_result, pressure_mid) = mqtt_client.publish(topic=mqtt_config.topic_pressure,
                                                                       payload=pressure_reading,
                                                                       qos=2,
                                                                       retain=True)
            mqtt_client.loop(timeout=mqtt_config.local_timeout,
                             max_packets=mqtt_config.max_packets)
            (temperature_mqtt_result, temperature_mid) = mqtt_client.publish(topic=mqtt_config.topic_temperature,
                                                                             payload=temperature_reading,
                                                                             qos=2,
                                                                             retain=True)
            mqtt_client.loop(timeout=mqtt_config.local_timeout,
                             max_packets=mqtt_config.max_packets)

            print('MQTT Result Humidity: {humidity_mqtt_result} [mid: {humidity_mid}]'.format(
                humidity_mqtt_result=humidity_mqtt_result,
                humidity_mid=humidity_mid))

            print('MQTT Result Pressure: {humidity_mqtt_result} [mid: {pressure_mid}]'.format(
                humidity_mqtt_result=pressure_mqtt_result,
                pressure_mid=pressure_mid))

            print('MQTT Result Temperature: {temperature_mqtt_result} [mid: {temperature_mid}]'.format(
                temperature_mqtt_result=temperature_mqtt_result,
                temperature_mid=temperature_mid))

            # wait time in seconds
            time.sleep(wait_time)


if __name__ == '__main__':
    App.main()
