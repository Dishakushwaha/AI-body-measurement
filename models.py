class BodyMeasurementResult:
    def __init__(self, filename, measurements):
        self.filename = filename
        self.measurements = measurements

    def get_measurement(self, name):
        return self.measurements.get(name, 0)

    def to_dict(self):
        return {
            "filename": self.filename,
            "measurements": self.measurements
        }