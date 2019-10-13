import six

TRUE_STRINGS = ('1', 't', 'true', 'on', 'y', 'yes')
FALSE_STRINGS = ('0', 'f', 'false', 'off', 'n', 'no')


def bool_from_string(subject, strict=False, default=False):
    """Interpret a subject as a boolean.

    A subject can be a boolean, a string or an integer. Boolean type value
    will be returned directly, otherwise the subject will be converted to
    a string. A case-insensitive match is performed such that strings
    matching 't','true', 'on', 'y', 'yes', or '1' are considered True and,
    when `strict=False`, anything else returns the value specified by
    'default'.

    Useful for JSON-decoded stuff and config file parsing.

    If `strict=True`, unrecognized values, including None, will raise a
    ValueError which is useful when parsing values passed in from an API call.
    Strings yielding False are 'f', 'false', 'off', 'n', 'no', or '0'.
    """
    if isinstance(subject, bool):
        return subject
    if not isinstance(subject, six.string_types):
        subject = six.text_type(subject)

    lowered = subject.strip().lower()

    if lowered in TRUE_STRINGS:
        return True
    elif lowered in FALSE_STRINGS:
        return False
    elif strict:
        acceptable = ', '.join(
            "'%s'" % s for s in sorted(TRUE_STRINGS + FALSE_STRINGS))
        msg = "Unrecognized value '%(val)s', acceptable values are:" \
              " %(acceptable)s" % {'val': subject,
                                   'acceptable': acceptable}
        raise ValueError(msg)
    else:
        return default
