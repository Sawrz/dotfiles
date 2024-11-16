import subprocess


class SoundDevices(object):
    def __init__(self, device_aliases):
        """
        Control Sound output by keeping track of sound device ids and ability to change them.
        :param device_aliases: Map the name you want to use to the device name. You can find the device name with pactl list short sinks
        :type device_aliases: dict
        """
        self.device_aliases = device_aliases

        self.update_device_map()

    @staticmethod
    def __extract_process_information__(process):
        output, error = process.communicate()

        if error is not None:
            raise Exception(error)

        output = str(output)
        output = output.split("'")[1]
        output = output.split("\\n")[:-1]

        return [element.split("\\t") for element in output]

    def update_device_map(self):
        # get all available devices
        process = subprocess.Popen("pactl list short sinks", stdout=subprocess.PIPE, shell=True)
        available_devices = self.__extract_process_information__(process=process)

        self.device_map = {}
        for key, value in self.device_aliases.items():
            for index, device in enumerate(available_devices):
                if value in device[1]:
                    self.device_map[key] = device[0]
                    available_devices.pop(index)
                    break

    def switch(self, device_name):
        device_id = self.device_map[device_name]

        subprocess.call(f"pacmd set-default-sink {device_id}", shell=True)
        process = subprocess.Popen("pactl list short sink-inputs", stdout=subprocess.PIPE, shell=True)

        current_streams = self.__extract_process_information__(process=process)

        for stream in current_streams:
            subprocess.call(f"pactl move-sink-input {stream[0]} {device_id}", shell=True)

