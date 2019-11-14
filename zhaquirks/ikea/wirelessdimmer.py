"""Device handler for IKEA of Sweden TRADFRI round wireless dimmer"""

from zhaquirks.const import (
    MODELS_INFO,
    ENDPOINTS,
    PROFILE_ID,
    DEVICE_TYPE,
    INPUT_CLUSTERS,
    OUTPUT_CLUSTERS,
    DEVICE_ROTATED,
    LEFT,
    COMMAND,
    COMMAND_MOVE,
    CLUSTER_ID,
    ARGS,
    RIGHT,
)
from zhaquirks.ikea import IKEA
from zigpy.profiles import zll
from zigpy.quirks import CustomDevice
from zigpy.zcl.clusters.general import (
    Basic,
    PowerConfiguration,
    Identify,
    Alarms,
    Groups,
    OnOff,
    LevelControl,
    Ota,
)
from zigpy.zcl.clusters.lightlink import LightLink

DIAGNOSTICS_CLUSTER_ID = 0x0B05  # decimal = 2821


class IkeaTradfriWirelessDimmer(CustomDevice):
    """Custom device representing the rotating wireless dimmers from IKEA."""

    signature = {
        # <SimpleDescriptor endpoint=1 profile=260 device_type=2064
        # device_version=2
        # input_clusters=[0, 1, 3, 9, 2821, 4096]
        # output_clusters=[3, 4, 6, 8, 25, 4096]>
        MODELS_INFO: [(IKEA, "TRADFRI wireless dimmer")],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zll.PROFILE_ID,
                DEVICE_TYPE: zll.DeviceType.COLOR_SCENE_CONTROLLER,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    PowerConfiguration.cluster_id,
                    Identify.cluster_id,
                    Alarms.cluster_id,
                    DIAGNOSTICS_CLUSTER_ID,
                    LightLink.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Identify.cluster_id,
                    Groups.cluster_id,
                    OnOff.cluster_id,
                    LevelControl.cluster_id,
                    Ota.cluster_id,
                    LightLink.cluster_id,
                ],
            }
        },
    }

    # no changes...
    replacement = {
        ENDPOINTS: {
            1: {
                PROFILE_ID: zll.PROFILE_ID,
                DEVICE_TYPE: zll.DeviceType.COLOR_SCENE_CONTROLLER,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    PowerConfiguration.cluster_id,
                    Identify.cluster_id,
                    Alarms.cluster_id,
                    DIAGNOSTICS_CLUSTER_ID,
                    LightLink.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Identify.cluster_id,
                    Groups.cluster_id,
                    OnOff.cluster_id,
                    LevelControl.cluster_id,
                    Ota.cluster_id,
                    LightLink.cluster_id,
                ],
            }
        }
    }

    device_automation_triggers = {
        (DEVICE_ROTATED, LEFT): {
            COMMAND: COMMAND_MOVE,
            CLUSTER_ID: LevelControl.cluster_id,
            ARGS: [1, int],
        },
        (DEVICE_ROTATED, RIGHT): {
            COMMAND: COMMAND_MOVE,
            CLUSTER_ID: LevelControl.cluster_id,
            ARGS: [0, int],
        },
    }
