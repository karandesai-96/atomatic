import os
import json
import sqlalchemy as sqlalc


def databrame_to_sql_table(dataframe):
    # obtain credentials
    json_data = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  "db_credentials.json"), 'r')
    cred = json.loads(json_data.read())
    json_data.close()

    # create sqlalchemy engine
    engine = sqlalc.create_engine(cred[u'engine'] + '://' + cred[u'user'] + ':'
                                  + cred[u'password'] + '@' + cred[u'host'] +
                                  ':' + cred[u'port'] + '/' + cred[u'db'])

    # create table in db
    dataframe.to_sql(name="Atomic Weights and Isotopic Composition",
                     con=engine, if_exists="replace", index=False, chunksize=1)
