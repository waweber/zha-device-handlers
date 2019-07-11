"""Netvox device."""
import zigpy.types as t
from zigpy.profiles import zha
from zigpy.quirks import CustomDevice, CustomCluster
from zhaquirks import Bus, LocalDataCluster
from zigpy.zcl.clusters.general import (
    Basic, Commissioning, Identify, PollControl, BinaryInput
)
from zigpy.zcl.clusters.security import IasZone

from zhaquirks.centralite import PowerConfigurationCluster

DIAGNOSTICS_CLUSTER_ID = 0x0B05  # decimal = 2821
ARRIVAL_SENSOR_DEVICE_TYPE = 0x8000


class FastPollingPowerConfigurationCluster(PowerConfigurationCluster):
    """FastPollingPowerConfigurationCluster."""

    cluster_id = PowerConfigurationCluster.cluster_id
    FREQUENCY = 45
    MINIMUM_CHANGE = 0

    async def configure_reporting(self, attribute, min_interval,
                                  max_interval, reportable_change,
                                  manufacturer=None):
        """Configure reporting."""
        result = await super().configure_reporting(
            PowerConfigurationCluster.BATTERY_VOLTAGE_ATTR,
            self.FREQUENCY,
            self.FREQUENCY,
            self.MINIMUM_CHANGE
        )
        return result

    def _update_attribute(self, attrid, value):
        self.endpoint.device.tracking_bus.listener_event(
            'update_tracking',
            attrid,
            value
        )
        super()._update_attribute(attrid, value)


class TrackingCluster(LocalDataCluster, BinaryInput):
    """Tracking cluster."""

    cluster_id = BinaryInput.cluster_id

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.endpoint.device.tracking_bus.add_listener(self)

    def update_tracking(self, attrid, value):
        """Update tracking info."""
        # prevent unbounded null entries from going into zigbee.db
        self._update_attribute(0, 1)


class IASZoneCluster(CustomCluster, IasZone):
    """Centralite acceleration cluster."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.client_commands.update({
            0x0000: (
                'status_change_notification',
                (t.bitmap16, t.bitmap8),
                False
            ),
        })


class Z308E3ED(CustomDevice):
    """Netvox Z308E3ED."""

    def __init__(self, *args, **kwargs):
        """Init."""
        self.tracking_bus = Bus()
        super().__init__(*args, **kwargs)

    signature = {
        #  <SimpleDescriptor endpoint=1 profile=260 device_type=1026
        #  device_version=0
        #  input_clusters=[0, 1, 3, 21, 1280, 32, 2821]
        #  output_clusters=[]>
        'endpoints': {
            1: {
                'profile_id': zha.PROFILE_ID,
                'device_type': zha.DeviceType.IAS_ZONE,
                'input_clusters': [
                    Basic.cluster_id,
                    PowerConfigurationCluster.cluster_id,
                    Identify.cluster_id,
                    PollControl.cluster_id,
                    IasZone.cluster_id,
                    Commissioning.cluster_id,
                    DIAGNOSTICS_CLUSTER_ID
                ],
                'output_clusters': [
                ],
            }
        }
    }

    replacement = {
        'endpoints': {
            1: {
                'device_type': ARRIVAL_SENSOR_DEVICE_TYPE,
                'input_clusters': [
                    Basic.cluster_id,
                    FastPollingPowerConfigurationCluster,
                    Identify.cluster_id,
                    PollControl.cluster_id,
                    IASZoneCluster,
                    TrackingCluster,
                    Commissioning.cluster_id,
                    DIAGNOSTICS_CLUSTER_ID
                ]
            }
        },
    }
