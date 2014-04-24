import os.path
from mock import Mock
from django.test import TestCase
from django.core.files import File
from datetime import date
from django.contrib.auth.models import User
from globallometree.apps.allometric_equations.models import (
    Submission, AllometricEquation
)
from globallometree.apps.taxonomy.models import (
    Species, SpeciesGroup
)
from globallometree.apps.locations.models import (
    Location, LocationGroup
)
import globallometree.settings as settings

class SubmissionTestCase(TestCase):
    fixtures = [os.path.join(
        os.path.dirname(__file__), 'test_data', 'locations.yaml'
    )]

    def setUp(self):
        user_mock = Mock(spec=User)
        user_mock._state = Mock()
        user_mock.id = '1'

        Submission.objects.create(
            submitted_notes = 'Test submission',
            date_uploaded = date(2007, 12, 5),
            user = user_mock,
            imported = False
        )

    def set_submitted_file(self, submission, file_name):
        submission.submitted_file.save(
            'test_import_success.txt',
            File(open(os.path.join(
                os.path.dirname(__file__), 'test_data', file_name
            )))
        )

    def test_import_data_successful(self):
        """A submission with a correct file is successfully imported"""

        s = Submission.objects.latest('id')
        self.set_submitted_file(s, 'test_import_success.txt')

        output = s.import_data(run_verified=True, import_good_rows_anyway=True)

        self.assertEqual(len(output['errors']), 0)
        self.assertEqual(len(output['missing_headers']), 0)
        self.assertEqual(len(output['missed_rows']), 0)
        self.assertEqual(len(output['ok_headers']), 72)
        self.assertEqual(output['rows_to_import'], output['total_rows_imported'])
        self.assertEqual(
            AllometricEquation.objects.count(),
            output['total_rows_imported']
        )
        self.assertEqual(
            Species.objects.count(),
            output['species_inserted']
        )
        self.assertEqual(
            SpeciesGroup.objects.count(),
            output['species_groups_inserted']
        )
        self.assertEqual(
            Location.objects.count(),
            output['locations_inserted']
        )
        self.assertEqual(
            LocationGroup.objects.count(),
            output['location_groups_inserted']
        )

        os.unlink(os.path.join(
            settings.MEDIA_ROOT, 'data_submissions', 'test_import_success.txt'
        ))
