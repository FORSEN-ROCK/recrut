import datetime

from django.core.management.base import BaseCommand, CommandError
from HRrecrut.views import CheckSearchTasksView


class Command(BaseCommand):
    help = 'Starts resume download'

    def add_arguments(self, parser):
        parser.add_argument(
                            '--debug',
                            action='store_true',
                            dest='debug',
                            default=False,
                            help='Set debug flag True/False')

    def handle(self, *args, **options):
        debug = options['debug']
        target_view = CheckSearchTasksView()

        begin_time = datetime.datetime.utcnow()
        target_view.check(debug)
        end_time = datetime.datetime.utcnow()
        spend_sec = end_time - begin_time
        spend_minuts = round(spend_sec.seconds / 60, 2)
        begin_date = begin_time.strftime('%d-%m-%G %H:%M:%S')
        end_date = end_time.strftime('%d-%m-%G %H:%M:%S')
        self.stdout.write(
            'Check, start - %s end - %s, spend = %s min' % (begin_date,
                                                            end_date,
                                                            spend_minuts)
        )