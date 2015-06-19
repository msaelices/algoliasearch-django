from django.core.management.base import BaseCommand
import django.contrib.algoliasearch


class Command(BaseCommand):
    help = 'Send all index to Algolia.'

    def add_arguments(self, parser):
        parser.add_argument('--batchsize', nargs='?', default=1000, type=int)
        parser.add_argument('--model', nargs='+', type=str)

    def handle(self, *args, **options):
        '''Run the management command.'''
        self.stdout.write('The following models were indexed:')
        for model in AlgoliaSearch.get_registered_model():
            adapter = AlgoliaSearch.get_adapter(model)
            if options['model'] and not (model.__name__ in options['model']):
                continue

            counts = adapter.index_all(batch_size=options['batchsize'])
            self.stdout.write('\t* {} --> {}'.format(model.__name__, counts))