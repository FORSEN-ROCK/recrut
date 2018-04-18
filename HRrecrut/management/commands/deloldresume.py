import datetime

from django.core.management.base import BaseCommand, CommandError
from HRrecrut.views import DelOldResumeView


class Command(BaseCommand):
    help = 'Starts resume deledet'

    def add_arguments(self, parser):
        parser.add_argument(
                            '--debug',
                            action='store_true',
                            dest='debug',
                            default=False,
                            help='Set debug flag True/False')

    def handle(self, *args, **options):
        debug = options['debug']
        target_view = DelOldResumeView()

        begin_time = datetime.datetime.utcnow()
        target_view.delete(debug)
        end_time = datetime.datetime.utcnow()
        spend_sec = end_time - begin_time
        spend_minuts = round(spend_sec.seconds / 60, 2)
        begin_date = begin_time.strftime('%d-%m-%G %H:%M:%S')
        end_date = end_time.strftime('%d-%m-%G %H:%M:%S')
        self.stdout.write(
            'Delete, start - %s end - %s, spend = %s min' % (begin_date,
                                                            end_date,
                                                            spend_minuts)
        )