import os.path

from django.core.management.base import BaseCommand, ArgumentParser, CommandError

from cloud.services.usecases import LoadInfrastructureUsecase


class Command(BaseCommand):
    help = 'Loads infrastructure to DB'

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument(
            '--filename',
            '-f',
            required=True,
            type=str
        )
        parser.add_argument('-d', '--delete', dest='is_delete', action='store_true')

    def handle(self, *args, **options):
        if not os.path.exists(options.get('filename')):
            raise CommandError('File not found')
        is_delete = options.get('is_delete')
        filename = options.get('filename')

        LoadInfrastructureUsecase(is_delete_old=is_delete).execute(filename)
