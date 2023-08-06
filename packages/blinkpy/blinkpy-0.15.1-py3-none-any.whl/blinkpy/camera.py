"""Defines Blink cameras."""

from shutil import copyfileobj
import logging
from blinkpy import api

_LOGGER = logging.getLogger(__name__)


class BlinkCamera:
    """Class to initialize individual camera."""

    def __init__(self, sync):
        """Initiailize BlinkCamera."""
        self.sync = sync
        self.name = None
        self.camera_id = None
        self.network_id = None
        self.thumbnail = None
        self.serial = None
        self.motion_enabled = None
        self.battery_voltage = None
        self.clip = None
        self.temperature = None
        self.temperature_calibrated = None
        self.battery_state = None
        self.motion_detected = None
        self.wifi_strength = None
        self.last_record = None
        self._cached_image = None
        self._cached_video = None

    @property
    def attributes(self):
        """Return dictionary of all camera attributes."""
        attributes = {
            "name": self.name,
            "camera_id": self.camera_id,
            "serial": self.serial,
            "temperature": self.temperature,
            "temperature_c": self.temperature_c,
            "temperature_calibrated": self.temperature_calibrated,
            "battery": self.battery,
            "battery_voltage": self.battery_voltage,
            "thumbnail": self.thumbnail,
            "video": self.clip,
            "motion_enabled": self.motion_enabled,
            "motion_detected": self.motion_detected,
            "wifi_strength": self.wifi_strength,
            "network_id": self.sync.network_id,
            "sync_module": self.sync.name,
            "last_record": self.last_record,
        }
        return attributes

    @property
    def battery(self):
        """Return battery as string."""
        return self.battery_state

    @property
    def temperature_c(self):
        """Return temperature in celcius."""
        return round((self.temperature - 32) / 9.0 * 5.0, 1)

    @property
    def image_from_cache(self):
        """Return the most recently cached image."""
        if self._cached_image:
            return self._cached_image
        return None

    @property
    def video_from_cache(self):
        """Return the most recently cached video."""
        if self._cached_video:
            return self._cached_video
        return None

    def snap_picture(self):
        """Take a picture with camera to create a new thumbnail."""
        return api.request_new_image(self.sync.blink, self.network_id, self.camera_id)

    def set_motion_detect(self, enable):
        """Set motion detection."""
        if enable:
            return api.request_motion_detection_enable(
                self.sync.blink, self.network_id, self.camera_id
            )
        return api.request_motion_detection_disable(
            self.sync.blink, self.network_id, self.camera_id
        )

    def update(self, config, force_cache=False, **kwargs):
        """Update camera info."""
        # force = kwargs.pop('force', False)
        self.name = config["name"]
        self.camera_id = str(config["id"])
        self.network_id = str(config["network_id"])
        self.serial = config["serial"]
        self.motion_enabled = config["enabled"]
        self.battery_voltage = config["battery_voltage"]
        self.battery_state = config["battery_state"]
        self.temperature = config["temperature"]
        self.wifi_strength = config["wifi_strength"]

        # Retrieve calibrated temperature from special endpoint
        resp = api.request_camera_sensors(
            self.sync.blink, self.network_id, self.camera_id
        )
        try:
            self.temperature_calibrated = resp["temp"]
        except KeyError:
            self.temperature_calibrated = self.temperature
            _LOGGER.warning("Could not retrieve calibrated temperature.")

        # Check if thumbnail exists in config, if not try to
        # get it from the homescreen info in the sync module
        # otherwise set it to None and log an error
        new_thumbnail = None
        thumb_addr = None
        if config["thumbnail"]:
            thumb_addr = config["thumbnail"]
        else:
            _LOGGER.warning(
                "Could not find thumbnail for camera %s", self.name, exc_info=True
            )

        if thumb_addr is not None:
            new_thumbnail = "{}{}.jpg".format(self.sync.urls.base_url, thumb_addr)

        try:
            self.motion_detected = self.sync.motion[self.name]
        except KeyError:
            self.motion_detected = False

        clip_addr = None
        if self.name in self.sync.last_record:
            clip_addr = self.sync.last_record[self.name]["clip"]
            self.last_record = self.sync.last_record[self.name]["time"]
            self.clip = "{}{}".format(self.sync.urls.base_url, clip_addr)

        # If the thumbnail or clip have changed, update the cache
        update_cached_image = False
        if new_thumbnail != self.thumbnail or self._cached_image is None:
            update_cached_image = True
        self.thumbnail = new_thumbnail

        update_cached_video = False
        if self._cached_video is None or self.motion_detected:
            update_cached_video = True

        if new_thumbnail is not None and (update_cached_image or force_cache):
            self._cached_image = api.http_get(
                self.sync.blink, url=self.thumbnail, stream=True, json=False
            )
        if clip_addr is not None and (update_cached_video or force_cache):
            self._cached_video = api.http_get(
                self.sync.blink, url=self.clip, stream=True, json=False
            )

    def image_to_file(self, path):
        """
        Write image to file.

        :param path: Path to write file
        """
        _LOGGER.debug("Writing image from %s to %s", self.name, path)
        response = self._cached_image
        if response.status_code == 200:
            with open(path, "wb") as imgfile:
                copyfileobj(response.raw, imgfile)
        else:
            _LOGGER.error(
                "Cannot write image to file, response %s", response.status_code
            )

    def video_to_file(self, path):
        """Write video to file.

        :param path: Path to write file
        """
        _LOGGER.debug("Writing video from %s to %s", self.name, path)
        response = self._cached_video
        if response is None:
            _LOGGER.error("No saved video exist for %s.", self.name)
            return
        with open(path, "wb") as vidfile:
            copyfileobj(response.raw, vidfile)
