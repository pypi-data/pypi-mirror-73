import json

import pandas

from mindsdb.api.mysql.mysql_proxy.datahub.datanodes.datanode import DataNode
from mindsdb.interfaces.native.mindsdb import MindsdbNative
from mindsdb.integrations.clickhouse.clickhouse import Clickhouse
from mindsdb.integrations.mariadb.mariadb import Mariadb

class MindsDBDataNode(DataNode):
    type = 'mindsdb'

    def __init__(self, config):
        self.config = config
        self.mindsdb_native = MindsdbNative(config)

    def getTables(self):
        models = self.mindsdb_native.get_models()
        models = [x['name'] for x in models if x['status'] == 'complete']
        models += ['predictors']
        return models

    def hasTable(self, table):
        return table in self.getTables()

    def getTableColumns(self, table):
        if table == 'predictors':
            return ['name', 'status', 'accuracy', 'predict_cols', 'select_data_query', 'training_options']
        if table == 'commands':
            return ['command']
        model = self.mindsdb_native.get_model_data(name=table)
        columns = []
        columns += [x['column_name'] for x in model['data_analysis']['input_columns_metadata']]
        columns += [x['column_name'] for x in model['data_analysis']['target_columns_metadata']]
        for col in model['predict']:
            columns += [f"{col}_confidence"]
            if model['data_analysis_v2'][col]['typing']['data_type'] == 'Numeric':
                columns += [f"{col}_min", f"{col}_max"]
            columns += [f"{col}_explain"]

        # TODO this should be added just for clickhouse queries
        columns += ['select_data_query']
        return columns

    def _select_predictors(self):
        models = self.mindsdb_native.get_models()
        return [{
            'name': x['name'],
            'status': x['status'],
            'accuracy': x['accuracy'],
            'predict_cols': ', '.join(x['predict']),
            'select_data_query': x['data_source'],
            'training_options': ''  # TODO ?
        } for x in models]

    def delete_predictor(self, name):
        self.mindsdb_native.delete_model(name)

    def select(self, table, columns=None, where=None, where_data=None, order_by=None, group_by=None, came_from=None):
        ''' NOTE WHERE statements can be just $eq joined with 'and'
        '''
        if table == 'predictors':
            return self._select_predictors()

        select_data_query = None
        if came_from is not None and 'select_data_query' in where:
            select_data_query = where['select_data_query']['$eq']
            del where['select_data_query']

            '''
            @TODO (Urgent~ish)

            This is a horrible but function hack, however the proper way to do this is:
            1. Figure out the alias of the database sending the query
            2. Lookup the connection information in the config
            3. Send that information + the query + a name (maybe the hash of the query or the query itself) to the Datastore API and ask it to create a datasource

            That way we also avoid making the same query twice and we don't use the database integrations (meant to sync predictors) in order to query data (the role of the mindsdb_native datasources / the datastore / data skillet)
            '''
            if came_from == 'clickhouse':
                ch = Clickhouse(self.config, 'default_clickhouse')
                res = ch._query(select_data_query.strip(' ;') + ' FORMAT JSON')
                data = res.json()['data']
            elif came_from == 'mariadb':
                maria = Mariadb(self.config, 'default_mariadb')
                data = maria._query(select_data_query)

            if where_data is None:
                where_data = data
            else:
                where_data += data

        new_where = {}
        if where_data is not None:
            where_data = pandas.DataFrame(where_data)
        else:
            for key, value in where.items():
                if isinstance(value, dict) is False or len(value.keys()) != 1 or list(value.keys())[0] != '$eq':
                    # TODO value should be just string or number
                    raise Exception()
                new_where[key] = value['$eq']
            if len(new_where) == 0:
                new_where = None

            where_data = [new_where]

        res = self.mindsdb_native.predict(name=table, when_data=where_data)

        model = self.mindsdb_native.get_model_data(name=table)
        predicted_columns = model['predict']

        data = []
        keys = [x for x in list(res._data.keys()) if x in columns]
        min_max_keys = []
        for col in predicted_columns:
            if model['data_analysis_v2'][col]['typing']['data_type'] == 'Numeric':
                min_max_keys.append(col)

        length = len(res._data[predicted_columns[0]])
        for i in range(length):
            row = {}
            for key in keys:
                row[key] = res._data[key][i]
            for key in predicted_columns:
                row[key + '_confidence'] = res[i].explanation[key]['confidence']
                row[key + '_explain'] = json.dumps(res[i].explanation[key])
            for key in min_max_keys:
                row[key + '_min'] = res[i].explanation[key]['confidence_interval'][0]
                row[key + '_max'] = res[i].explanation[key]['confidence_interval'][-1]
            row['select_data_query'] = select_data_query
            data.append(row)

        return data
