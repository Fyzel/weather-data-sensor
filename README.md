
# weather-data-sensor
This is a command line utility to read humidity, pressure, and temperature readings. The readings are written to a [Mosquitto Queue with submission daemon](https://github.com/Fyzel/weather-data-daemon) that submits to a  [RESTful web service](https://github.com/Fyzel/weather-data-api).

The sensor used for this application is the [BME280](https://cdn-shop.adafruit.com/datasheets/BST-BME280_DS001-10.pdf) from [Adafruit](http://adafru.it/2652).

For remote debugging of python scripts that access the GPIO pins, refer to [Remote Debug GPIO on Raspberry Pi](https://nathanpjones.com/2016/02/remote-debug-gpio-on-raspberry-pi/).


## Sensor Wiring
The connections for the sensor and the Raspberry Pi are given in the schematic below.

![Wiring Schematic](/docs/assets/images/schematic.png)


## Configuration

The application's configuration file specifies the following:
* the address to submit the JSON encoded readings for humidity, pressure, and temperature.
* the error range for the sensor's humidity, pressure, and temperature readings.
* the wait time between measurements (60 seconds).


## Humidity Output

The JSON formatting of humidity values are illustrated below.

| Attribute         | Datatype | Description                                        |
| ----------------- | -------- | -------------------------------------------------- |
| value             | decimal  | The humidity reading value                         |
| value_units       | string   | The units of the humidity value                    |
| value_error_range | decimal  | The error range for sensor in units                |
| timestamp         | datetime | A UTC datetime the record was measured             |
| elevation         | decimal  | The elevation that the record was measured         |
| elevation_units   | string   | The units of the elevation value                   |
| longitude         | decimal  | The dotted decimal notation value of the latitude  |
| longitude         | decimal  | The dotted decimal notation value of the longitude |


An example of the JSON is given below.

```JSON
{
    "value": 72.22,
    "value_units": "percent",
    "value_error_range": 0.001,
    "timestamp": "1990-12-25T23:59:59.12345Z",
    "elevation": 122,
    "elevation_units": "m",
    "latitude": -12.345678,
    "longitude": 0.1111
}
```


## Pressure Output

The JSON formatting of pressure values are illustated below.

| Attribute         | Datatype | Description                                        |
| ----------------- | -------- | -------------------------------------------------- |
| value             | decimal  | The pressure reading value                         |
| value_units       | string   | The units of the pressure value                    |
| value_error_range | decimal  | The error range for sensor in units                |
| timestamp         | datetime | A UTC datetime the record was measured             |
| elevation         | decimal  | The elevation that the record was measured         |
| elevation_units   | string   | The units of the elevation value                   |
| longitude         | decimal  | The dotted decimal notation value of the latitude  |
| longitude         | decimal  | The dotted decimal notation value of the longitude |


An example of the JSON is given below.

```JSON
{
    "value": 72.22,
    "value_units": "kPa",
    "value_error_range": 0.001,
    "timestamp": "1990-12-25T23:59:59.12345Z",
    "elevation": 122,
    "elevation_units": "m",
    "latitude": -12.345678,
    "longitude": 0.1111
}
```


## Temperature Output

The JSON formatting of temperature values are illustated below.

| Attribute         | Datatype | Description                                        |
| ----------------- | -------- | -------------------------------------------------- |
| value             | decimal  | The temperature reading value                      |
| value_units       | string   | The units of the temperature value                 |
| value_error_range | decimal  | The error range for sensor in units                |
| timestamp         | datetime | A UTC datetime the record was measured             |
| elevation         | decimal  | The elevation that the record was measured         |
| elevation_units   | string   | The units of the elevation value                   |
| longitude         | decimal  | The dotted decimal notation value of the latitude  |
| longitude         | decimal  | The dotted decimal notation value of the longitude |


An example of the JSON is given below.

```JSON
{
    "value": -10.12,
    "value_units": "C",
    "value_error_range": 0.001,
    "timestamp": "1990-12-25T23:59:59.12345Z",
    "elevation": 122,
    "elevation_units": "m",
    "latitude": -12.345678,
    "longitude": 0.1111
}
```
