from sensors.light_sensor import LightSensor


class RightLightSensor(LightSensor):
    def __init__(self, agent, environment, config):
        super().__init__(agent, environment, config, position=[-config["light_sensor_distance"], 0])