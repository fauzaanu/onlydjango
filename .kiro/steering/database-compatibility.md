# Database Compatibility: PostgreSQL & SQLite

Tests run on SQLite for speed, production uses PostgreSQL. All code must work on both.

## Prohibited PostgreSQL-Only Features

### Fields (from `django.contrib.postgres.fields`)
- `ArrayField` - Use `JSONField` with a list instead
- `HStoreField` - Use `JSONField` instead
- `IntegerRangeField`, `BigIntegerRangeField`, `DecimalRangeField` - Store as two separate fields
- `DateRangeField`, `DateTimeRangeField` - Store as two separate fields
- `CITextField`, `CIEmailField`, `CICharField` - Use regular fields with `__iexact` lookups

### Aggregates (from `django.contrib.postgres.aggregates`)
- `ArrayAgg` - Use Python to aggregate in memory
- `StringAgg` - Use Python `join()` after query
- `BitAnd`, `BitOr`, `BitXor` - Compute in Python
- `BoolAnd`, `BoolOr` - Use `Exists` or compute in Python
- `Corr`, `CovarPop`, `RegrAvgX`, etc. - Statistical functions not available

### Lookups
- `trigram_similar` - Use `__icontains` instead
- `unaccent` - Handle in Python if needed
- `SearchVector`, `SearchQuery`, `SearchRank` - Use `__icontains` or external search

### Constraints
- `ExclusionConstraint` - Use application-level validation

## Safe to Use (Works on Both)

### Fields
- `JSONField` - Supported on SQLite 3.9+ (Python 3.9+ includes JSON1)
- All standard Django fields

### Lookups
- `__iexact`, `__icontains`, `__istartswith`, `__iendswith`
- `__in`, `__range`, `__gt`, `__lt`, `__gte`, `__lte`
- `__contains`, `__has_key`, `__has_keys` (for JSONField)

### Aggregates
- `Count`, `Sum`, `Avg`, `Max`, `Min`
- `StdDev`, `Variance`

## Pattern: Cross-Database Compatible Code

```python
# BAD - PostgreSQL only
from django.contrib.postgres.fields import ArrayField

class Post(models.Model):
    tags = ArrayField(models.CharField(max_length=50))

# GOOD - Works on both
class Post(models.Model):
    tags = models.JSONField(default=list)
```

```python
# BAD - PostgreSQL only
from django.contrib.postgres.aggregates import ArrayAgg

tags = Post.objects.values_list('tag', flat=True).aggregate(all_tags=ArrayAgg('tag'))

# GOOD - Works on both
tags = list(Post.objects.values_list('tag', flat=True))
```

## If You Must Use PostgreSQL-Specific Features

1. Skip the test with `@skipUnless`:
```python
from django.test import skipUnless
from django.db import connection

@skipUnless(connection.vendor == 'postgresql', "PostgreSQL specific")
def test_array_field_feature(self):
    ...
```

2. Document why it's necessary
3. Ensure the feature is not in a critical path tested by CI
