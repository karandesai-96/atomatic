import os
import json
import pandas as pd
import sqlalchemy as sqlalc
import utils.db_utils as dbu

test_dataframe = pd.DataFrame({"Int": [1, 2, 3], "Char": ['a', 'b', 'c']})


def test_df_to_sql():
    # obtain test credentials
    json_data = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  "test_db_credentials.json"), 'r')
    cred = json.loads(json_data.read())
    json_data.close()

    # create sqlalchemy engine
    engine = sqlalc.create_engine(cred[u'engine'] + '://' + cred[u'user'] + ':'
                                  + cred[u'password'] + '@' + cred[u'host'] +
                                  ':' + cred[u'port'] + '/' + cred[u'db'])

    # drop 'Test Table' if exists (might happen if test failed earlier)
    if engine.dialect.has_table(engine, "Test Table"):
        test_table = sqlalc.Table("Test Table", sqlalc.MetaData(engine))
        test_table.drop()

    dbu.df_to_sql(test_dataframe, "Test Table", testing=True)
    assert engine.dialect.has_table(engine, "Test Table")

    # teardown
    test_table = sqlalc.Table("Test Table", sqlalc.MetaData(engine))
    test_table.drop()
