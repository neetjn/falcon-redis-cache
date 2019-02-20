from unittest import TestCase
from pylint.lint import Run


class LintTests(TestCase):

    def test_lint_package(self):

        filter = '--disable={rules}'\
            .format(rules=','.join([
                'fixme',
                'missing-docstring',
                'too-many-lines',
                'inconsistent-return-statements',
                'invalid-name',
            ]))

        with self.assertRaises(SystemExit) as lint_check:
            Run([filter, 'falcon_redis_cache'])
            self.assertEqual(lint_check.exception.code, 0)
