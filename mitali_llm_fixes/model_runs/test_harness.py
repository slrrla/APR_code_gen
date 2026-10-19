"""Run an unchanged unittest file, recording its existing test outcomes as JSON."""
import json
import os
from pathlib import Path
import runpy
import sys
import traceback
import unittest


def exception_record(err):
    kind, value, tb = err
    return {'type': kind.__name__, 'message': str(value),
            'frames': [{'file': f.filename, 'line': f.lineno, 'function': f.name}
                       for f in traceback.extract_tb(tb)],
            'traceback': ''.join(traceback.format_exception(kind, value, tb))}


def main():
    test, output = map(Path, sys.argv[1:3])
    data = {'tests_run': 0, 'events': [], 'finished': False}

    def save():
        temp = output.with_suffix('.tmp')
        temp.write_text(json.dumps(data, indent=2), encoding='utf-8')
        temp.replace(output)

    class RecordedResult(unittest.TextTestResult):
        def addSuccess(self, test):
            data['events'].append({'test': test.id(), 'kind': 'success'})
            super().addSuccess(test)

        def addError(self, test, err):
            data['events'].append({'test': test.id(), 'kind': 'error', **exception_record(err)})
            super().addError(test, err)

        def addFailure(self, test, err):
            data['events'].append({'test': test.id(), 'kind': 'failure', **exception_record(err)})
            super().addFailure(test, err)

        def addSkip(self, test, reason):
            data['events'].append({'test': test.id(), 'kind': 'skip', 'message': reason})
            super().addSkip(test, reason)

        def addExpectedFailure(self, test, err):
            data['events'].append({'test': test.id(), 'kind': 'expected_failure', **exception_record(err)})
            super().addExpectedFailure(test, err)

        def addUnexpectedSuccess(self, test):
            data['events'].append({'test': test.id(), 'kind': 'unexpected_success'})
            super().addUnexpectedSuccess(test)

        def addSubTest(self, test, subtest, err):
            if err:
                data['events'].append({'test': str(subtest),
                    'kind': 'failure' if issubclass(err[0], test.failureException) else 'error',
                    **exception_record(err)})
            super().addSubTest(test, subtest, err)

        def stopTest(self, test):
            super().stopTest(test)
            data['tests_run'] = self.testsRun
            save()

    class RecordedRunner(unittest.TextTestRunner):
        resultclass = RecordedResult

    # Only the result recorder changes. Test assertions and target source stay intact.
    unittest.TextTestRunner = RecordedRunner
    unittest.runner.TextTestRunner = RecordedRunner
    sys.argv = [str(test)]
    sys.path.insert(0, str(test.parent))
    try:
        runpy.run_path(str(test), run_name='__main__')
        data['finished'] = True
    except SystemExit as exc:
        data['finished'] = True
        raise
    except BaseException:
        data['events'].append({'test': 'test_module', 'kind': 'harness_error',
                               **exception_record(sys.exc_info())})
        data['finished'] = True
        raise
    finally:
        save()


if __name__ == '__main__':
    main()
