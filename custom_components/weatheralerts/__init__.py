"""The weatheralerts component."""

async def async_setup(hass, config):
    """Set up the weatheralerts component."""
    return True

async def async_setup_entry(hass, entry):
    """Set up weatheralerts from a config entry."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True

async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")
