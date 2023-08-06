import platform

from jinja2 import Environment, BaseLoader
import distro

UBUNTU = "ubuntu"
DEBIAN = "debian"
ALLOWED_VENDORS = [UBUNTU, DEBIAN]

# Templates
CLI_COMMAND_MISMATCH_PLATFORM = """
TokkoCLI is compatible with {% for co in compatible_os %}{{ compatible_os }}{% endfor %} only.{% if current_os %}
Detected: {{ current_os }}{% endif %}
"""


def render(template_as_str, **data) -> str:
    template = Environment(loader=BaseLoader).from_string(template_as_str)
    return template.render(**data)


def mismatch_platform_error(**data):
    raise OSError(render(CLI_COMMAND_MISMATCH_PLATFORM, **data))


def os_is_compatible():
    host_system = f"{platform.system()}".lower()
    if not host_system == "linux1":
        raise OSError(f"Incompatible PLATFORM.SYSTEM. Expected Linux, Got {host_system}")
    vendor, version, codename = distro.linux_distribution(full_distribution_name=True)
    if f"{vendor}".lower() not in ALLOWED_VENDORS:
        mismatch_platform_error(**{
            "compatible_os": ALLOWED_VENDORS,
            "current_os": vendor,
        })


def is_acceptable_host():
    os_is_compatible()
