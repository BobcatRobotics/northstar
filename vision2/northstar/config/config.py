from dataclasses import dataclass
import numpy
import numpy.typing


@dataclass
class LocalConfig:
    device_id: str = "northstar"
    server_ip: str = "localhost"
    stream_port: int = 8003
    has_calibration: bool = True
    camera_matrix: numpy.typing.NDArray[numpy.float64] = numpy.array([])
    distortion_coefficients: numpy.typing.NDArray[numpy.float64] = numpy.array([])


@dataclass
class RemoteConfig:
    camera_id: str = "2"
    camera_resolution_width: int = 800
    camera_resolution_height: int = 600
    camera_auto_exposure: int = 1
    camera_exposure: int = 100000
    camera_gain: int = 1
    fiducial_size_m: float = 0
    tag_layout: any = None
    frame_rate: int = 50


@dataclass
class ConfigStore:
    local_config: LocalConfig
    remote_config: RemoteConfig
