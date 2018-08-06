#!/usr/bin/python


import models
import sys

sys.path.append('../')  # noqa: E402
import config  # noqa: E402

test_uuid = 'f3159e3b-7ca6-4243-83dd-376755ab4721'

ss = models.create_db(config.DB_URL, config.DB_DEBUG)

# Test adding an architecture
foo = models.get_one_or_create(ss,
                               models.LU_Architecture,
                               short_name='unknown',
                               long_name='unknown',
                               description='unknown')
print foo
bar = ss.query(models.LU_Architecture).all()
print bar
foo = models.get_one_or_create(ss,
                               models.LU_Architecture,
                               short_name='x86_64',
                               long_name='AMD 64 reference',
                               description='64 bit architecture')
print foo
bar = models.get_only_one(ss,
                          models.LU_Architecture,
                          short_name='x86_64',
                          long_name='AMD 64 reference',
                          description='64 bit architecture')
print bar


ss.close()
##
##
