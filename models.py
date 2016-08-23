class ScriptExecutionRecord(models.Model):
    """
    Used to record some marks in programming, e.g. newest product id in weekly antique rss feed,
    latest run time of bronto scripts.
    Usage:
        Use data migration to generate a record with name and specified type before recording a new mark.
        Use .get(name=name) to retrieve the record in code. Then use value property to get or set value.
        If existing types can not match the requirement, add corresponding _get_<type>_value and _validate_<type>_value
        method to make sure the code works well.
    """
    DATETIME_PATTERN = '%Y-%m-%d %H:%M:%S'

    # Allowed types.
    DATETIME = 'datetime'
    INT = 'int'
    TYPE_CHOICES = (
        (DATETIME, "Date Time"),
        (INT, "Integer"),
    )

    name = models.CharField(max_length=128, unique=True)
    type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    _value = models.CharField(max_length=128, blank=True)

    def _get_int_value(self):
        return int(self._value)

    def _get_datetime_value(self):
        return datetime.datetime.strptime(self._value, self.DATETIME_PATTERN)

    def _get_value(self):
        if self._value:
            return getattr(self, '_get_%s_value' % self.type)()
        else:
            return None

    def _set_value(self, value):
        valid_value = getattr(self, '_validate_%s_value' % self.type)(value)
        self._value = valid_value

    def _validate_int_value(self, value):
        return int(value)

    def _validate_datetime_value(self, value):
        return value.strftime(self.DATETIME_PATTERN)

    value = property(_get_value, _set_value)
