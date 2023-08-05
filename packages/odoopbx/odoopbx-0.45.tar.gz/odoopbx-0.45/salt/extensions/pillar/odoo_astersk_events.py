'''
Pillar that takes events map from Odoo
'''
import logging

log = logging.getLogger(__name__)

__virtualname__ = 'odoo_asterisk_events'


def __virtual__():
    return True


def ext_pillar(minion_id, pillar, config):
    try:
        events_map = __salt__['odoo.execute'](
            'asterisk_common.event',
            'search_read',
            [[['is_enabled', '=', True], ['source', '=', 'AMI']]],
            log_error=False
        )
        return {
            'asterisk_events_map': events_map or [],
        }
    except Exception as e:
        log.info('Events map not loaded: %s', e)
        return {
            # Do not return events.
            'asterisk_events_map': []
        }
