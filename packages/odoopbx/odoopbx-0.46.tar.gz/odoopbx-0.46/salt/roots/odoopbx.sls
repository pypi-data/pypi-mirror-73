{% if grains.os_family == "Debian" %}
include:
  - asterisk
  - odoo
  - caddy
  - agent
{% else %}
not-yet-supported:
  test.show_notification:
    - text: Sorry, {{ grains.os_family }} is not supported yet
{% endif %}
