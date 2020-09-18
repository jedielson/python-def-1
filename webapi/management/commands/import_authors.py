import csv
import os

from django.core.management.base import BaseCommand

from webapi.models import Author


class Command(BaseCommand):
    help = ("Given an csv file with one column named 'name', "
            "it will create authors on database with these names")

    def add_arguments(self, parser):
        parser.add_argument('file_path',
                            type=str,
                            help="The path for csv with authors")

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        is_csv = file_path.endswith('.csv')
        if not is_csv:
            self.stdout.write(
                self.style.ERROR('Error: The file must be an csv file'))
            return

        is_file = os.path.isfile(file_path)
        if not is_file:
            self.stdout.write(
                self.style.ERROR('Error: the path informed is not a file'))
            return

        with open(file_path) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')

            for row in reader:
                self.create_author(row[0])

    def create_author(self, name):
        '''
        Given an author name, creates the author on database.

        It does not accept the word 'name'

        Args:
            name (str): The name of author
        '''
        if name == 'name':
            return

        existing_author = Author.objects.filter(name=name)
        if existing_author:
            return

        Author.objects.create(name=name)
