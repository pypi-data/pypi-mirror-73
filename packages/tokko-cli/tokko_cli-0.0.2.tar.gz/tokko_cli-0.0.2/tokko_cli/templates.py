DAEMON_SYSTEM_D_SERVICE = """
[Unit]
Description={{ name }}
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
ExecStart=/usr/bin/python3 {{ service_script }}
StandardInput=tty-force

[Install]
WantedBy=multi-user.target
"""

DAEMON_STATUS_TEMPLATE = """TokkoCLI.{{ codename }}.{{ version }}.daemon is RUNNING
UpTime seconds: {{ "{:.2f}".format(runtime) }}
"""

PRE_DOCKER_COMPOSE_SERVICE_TEMPLATE = """
"""

PRE_PROJECT_TEMPLATE = """---
Project {{ project }}
RootFolder: {{ root_folder }}{% if services %}
DockerCompose Services:{% for service in services %}
 + "{{ service.name }}"
   * BaseImage:        ...  {% if service.baseImage %}{{ service.baseImage }}{% else %}Unknown{% endif %}
   * ContainerName:    ...  {{ service.containerName }}
   * Ports:            ...  {% if service.ports %}{% for port in service.ports %}{{ port }} {% endfor %}{% else %}-{% endif %}
   * Declared Network  ...  {% if service.networks %}{% for network in service.networks %}{{ network }}{% endfor %}{% else %}Unknown{% endif %}
   * Use volumes?      ...  {% if service.volumes %}Yes{% else %}No{% endif %}
   ---{% endfor %}{% endif %}
"""

CLI_FIRST_DAY_MESSAGE = """
Hi there!!
  Welcome {user} to your first day as Tokky! \o/
"""

CLI_LAST_DAY_MESSAGE = """
--------------------------
  _Go for them tiger!_
       Mary J. Watson

  CU!
--------------------------
"""

CLI_COMMAND_ERROR_TEMPLATE = """
{% for error in errors %}
Command {{ error.command }}[{{ error.index }}] ends with code {{ error.exit_code }}
Error: {{ error.message }}{% if error.output %}
Output: {{ error.output }}{% else %}-{% endif %}
{% endfor %}
"""

PROJECT_DEVELOP_COLLECT_TEMPLATE = """{% for name, service in develop_services.items() %}
[{{ name }}]
RequirePostgreDB = {% if service.require_postgre_db %}yes{% else %}no{% endif %}
DatabaseName = {{ service.database_name }}
RequireRabbitMQ = {% if service.require_rabbit_mq %}yes{% else %}no{% endif %}
Volumes = {{ service.volumes }}
ContainerPort = {{  service.port }}
Command = {{ service.running_service }}
ShouldPatchCommand = {% if service.patch_command %}yes{% else %}no{% endif %}
{% endfor %}
"""

PROJECT_DEPENDENCIES_COLLECT_TEMPLATE = """
"""

PROJECT_NETWORKS_COLLECT_TEMPLATE = """
"""
