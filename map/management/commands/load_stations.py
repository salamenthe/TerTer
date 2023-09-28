import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from map.models import TrainStation


class Command(BaseCommand):
    help = 'Load data from Train Station file'

    def handle(self, *args, **kwargs):
        data_file = settings.BASE_DIR / 'data' / 'referentiel-gares-voyageurs.csv'
        keys = ('alias_libelle_noncontraint', 'longitude_entreeprincipale_wgs84','latitude_entreeprincipale_wgs84','dtfinval')  # the CSV columns we will gather data from.

        records = []
        with open(data_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                records.append({k: row[k] for k in keys})

        for record in records:
            # add the data to the database
            print(record['dtfinval'], record['alias_libelle_noncontraint'])
            if record['dtfinval'] == '' and record['latitude_entreeprincipale_wgs84']!='' and record['longitude_entreeprincipale_wgs84']!='':
                TrainStation.objects.get_or_create(
                    station_name=record['alias_libelle_noncontraint'],
                    latitude=record['latitude_entreeprincipale_wgs84'],
                    longitude=record['longitude_entreeprincipale_wgs84']
                )