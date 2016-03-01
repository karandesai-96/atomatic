import os
import json
import sqlalchemy as sqlalc
import sqlalchemy_utils as sqlutil


def df_to_sql(dataframe, name):
    # obtain credentials
    json_data = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  "db_credentials.json"), 'r')
    cred = json.loads(json_data.read())
    json_data.close()

    # create sqlalchemy engine
    engine = sqlalc.create_engine(cred[u'engine'] + '://' + cred[u'user'] + ':'
                                  + cred[u'password'] + '@' + cred[u'host'] +
                                  ':' + cred[u'port'] + '/' + cred[u'db'])

    if not sqlutil.database_exists(engine.url):
        sqlutil.create_database(engine.url)

    # create table in db
    dataframe.to_sql(name=name, con=engine, if_exists="replace", index=False)
