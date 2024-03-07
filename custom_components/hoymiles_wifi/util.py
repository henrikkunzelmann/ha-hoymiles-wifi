"""Utils for hoymiles-wifi."""

from typing import Union

from homeassistant.config_entries import ConfigEntry
from hoymiles_wifi.inverter import Inverter
from hoymiles_wifi.utils import generate_inverter_serial_number

from .error import CannotConnect


async def async_get_config_entry_data_for_host(host) -> tuple[str, list[str], list[dict[str, Union[str, int]]]]:
    """Migrate data from version 1 to version 2."""

    inverter = Inverter(host)

    real_data = await inverter.async_get_real_data_new()
    if real_data is None:
        raise CannotConnect

    dtu_sn = real_data.device_serial_number

    inverters = [generate_inverter_serial_number(sgs_data.serial_number) for sgs_data in real_data.sgs_data]

    ports = [{
        "inverter_serial_number": generate_inverter_serial_number(pv_data.serial_number),
        "port_number": pv_data.port_number
    } for pv_data in real_data.pv_data]

    return dtu_sn, inverters, ports
