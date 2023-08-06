from extras.plugins import PluginConfig


class AnimalSoundsConfig(PluginConfig):
    """
    This class defines attributes for the NetBox Animal Sounds plugin.
    """
    # Plugin package name
    name = 'netbox_file_upload'

    # Human-friendly name and description
    verbose_name = 'File Upload'
    description = 'A file upload plugin for Netbox'

    # Plugin version
    version = '0.1'

    # Plugin author
    author = 'Sean Collins'

    # Configuration parameters that MUST be defined by the user (if any)
    required_settings = []

    # Default configuration parameter values, if not set by the user

    # Base URL path. If not set, the plugin name will be used.
    base_url = 'file-upload'

    # Caching config
    caching_config = {}


config = AnimalSoundsConfig

