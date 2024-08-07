from dataclasses import dataclass
import numpy
import numpy.typing


@dataclass
class LocalConfig:
    device_id: str = "northstar1"
    server_ip: str = "192.168.1.19"
    stream_port: int = 8003
    has_calibration: bool = True
    camera_matrix: numpy.typing.NDArray[numpy.float64] = numpy.array([])
    distortion_coefficients: numpy.typing.NDArray[numpy.float64] = numpy.array([])


@dataclass
class RemoteConfig:
    camera_id: str = ""
    camera_resolution_width: int = 0
    camera_resolution_height: int = 0
    camera_auto_exposure: int = 1
    camera_exposure: int = 0
    camera_gain: int = 0
    fiducial_size_m: float = 0
    frame_rate: int = 0
    tag_layout: any = None


@dataclass
class ConfigStore:
    local_config: LocalConfig
    remote_config: RemoteConfig
