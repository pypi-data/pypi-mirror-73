import logging
import time

from django.conf import settings
from django.core.management import BaseCommand

from isc_common import setAttr
from isc_common.ws.webSocket import WebSocket
from kaf_pas.production.models.launches import LaunchesManager, Launches

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        # WebSocket.send_message(
        #     host=settings.WS_HOST,
        #     port=settings.WS_PORT,
        #     channel=f'{settings.WS_CHANNEL}_uandrew',
        #     message=dict(type='refresh_production_order_grid')
        # )

        # rec = DelProps(model_2_dict(Production_order.objects.filter(id=219127)[0]))
        # delAttr(rec, 'date')
        # setAttr(rec, 'value_start', 100000)

        # for i in range(0, 1000):
        #     WebSocket.row_refresh_grid(grid_id='refresh_production_order_grid_row',records=[dict(id=219009, value_start=random.randint(0, 10000))])

        # WebSocket.full_refresh_grid(settings.GRID_CONSTANTS.refresh_production_launch_grid)
        # record = LaunchesManager.getRecord(Launches.objects.get(id=143))
        record = {'id': 130, 'code': '2020 / 07 / 1', 'name': None, 'description': None, 'parent_id': None, 'demand_id': None, 'demand__code': None, 'status_id': 6, 'status__code': 'route_made', 'status__name': 'Выполнена маршрутизация111', 'qty': '', 'priority': 0, 'editing': True, 'deliting': True}
        # setAttr(record, 'value_sum', 100)
        # setAttr(record, 'value_made', 0)
        WebSocket.row_refresh_grid(settings.GRID_CONSTANTS.refresh_production_launch_grid_row, record)

        # for i in range(0, 101):
        #     setAttr(record, 'value_made', i)
        #     WebSocket.row_refresh_grid(settings.GRID_CONSTANTS.refresh_production_launch_grid_row, record)
        #     time.sleep(1)



        # record = LaunchesManager.getRecord(Launches.objects.get(id=144))
        # setAttr(record, 'value_sum', 100)
        # setAttr(record, 'value_made', 0)
        # WebSocket.row_refresh_grid(settings.GRID_CONSTANTS.refresh_production_launch_grid_row, record)
        # for i in range(0, 101):
        #     setAttr(record, 'value_made', i)
        #     WebSocket.row_refresh_grid(settings.GRID_CONSTANTS.refresh_production_launch_grid_row, record)
        #     time.sleep(1)
