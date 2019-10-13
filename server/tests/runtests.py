import sys
import unittest

TEST_MODULES = [
    'server.test.test_msg',
    'server.test.test_question',
    'server.test.test_teacher',
    'server.test.test_teacherjob',
    'server.test.test_user',
    'server.test.test_answer_keywords',
    'server.test.test_order',
]


def all():
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)


def main(**kwargs):

    if len(sys.argv) > 1:
        unittest.main(module=None, argv=sys.argv, **kwargs)
    else:
        unittest.main(defaultTest="all", argv=sys.argv, **kwargs)


if __name__ == '__main__':
    main()
