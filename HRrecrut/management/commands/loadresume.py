import datetime

from django.core.management.base import BaseCommand, CommandError
from HRrecrut.views import LoadError, SearchKeyError, LoadResumeView


class Command(BaseCommand):
    help = 'Starts resume cheeck'

    def add_arguments(self, parser):
        parser.add_argument(
                            '--debug',
                            action='store_true',
                            dest='debug',
                            default=False,
                            help='Set debug flag True/False'
        )
        parser.add_argument(
                            '--download',
                            action='store_true',
                            dest='download',
                            default=False,
                            help='Set download flag True/False'
        )
        parser.add_argument(
                            '--update',
                            action='store_true',
                            dest='update',
                            default=False,
                            help='Set update flag True/False'
        )
        parser.add_argument(
                            '--reload_err',
                            action='store_true',
                            dest='relod_error',
                            default=False,
                            help='Set relod_error flag True/False'
        )

    def handle(self, *args, **options):
        debug = options['debug']
        download = options['download']
        update = options['update']
        relod_error = options['relod_error']
        target_view = LoadResumeView()
        begin_time = datetime.datetime.utcnow()
        try:
            target_view.load(debug, download, update, relod_error)
        except LoadError:
            pass
        except SearchKeyError:
            pass
        end_time = datetime.datetime.utcnow()
        spend_sec = end_time - begin_time
        spend_minuts = round(spend_sec.seconds / 60, 2)
        begin_date = begin_time.strftime('%d-%m-%G %H:%M:%S')
        end_date = end_time.strftime('%d-%m-%G %H:%M:%S')
        self.stdout.write(
            'Load, start - %s end - %s, spend = %s min' % (begin_date,
                                                           end_date,
                                                           spend_minuts)
        )