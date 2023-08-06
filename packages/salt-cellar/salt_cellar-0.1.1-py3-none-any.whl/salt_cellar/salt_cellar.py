from ast import literal_eval
from collections import namedtuple
from datetime import datetime
from itertools import groupby
from math import nan
from typing import Iterable, List, Optional

import sqlalchemy

from .exceptions import DatabaseUnavailableError
from .lvdatatype import unpack

ElementData = namedtuple("ElementData", "name indices type")
ClusterData = namedtuple("ClusterData", "name subsys cluster elements start end limit")


class Ingredient:
    '''A description of the requested data'''

    def __init__(
        self,
        element: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ):
        '''Create a new Ingredient

        element should be a string formatted in one of the following ways:
        "subsystem:cluster:element>datatype"
        "subsystem:cluster:element:[i0, i1, ..., in]>datatype"
        where [...] is a list of element indicies
        '''
        self.name, self.type = element.rsplit('>', 1)
        splits = self.name.split(':')

        self.subsys, self.cluster, self.element = splits[:3]
        self.indices = sorted(literal_eval(splits[3])) if len(splits) > 3 else None
        self.start = start
        self.end = end

    def __repr__(self):
        drilldown = ':'.join([self.subsys, self.cluster, self.element])
        drilldown += f":{self.indices}" if self.indices else ""

        return f'Ingredient("{drilldown}>{self.type}", {self.start}, {self.end})'

    def __getattr__(self, name):
        if name == 'subsys_cluster':
            return f"{self.subsys}_{self.cluster}"
        elif name == 'is_array':
            return self.indices is not None
        elif name == 'is_enum':
            return self.type.startswith('e') or self.type.startswith('array_e')
        else:
            raise AttributeError(f"No attribute exists for '{name}'")


class ResultContainer:
    def __init__(self, results: Iterable, **kwargs):
        self.data = results

        # pass on all provided kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def first(self):
        return next(self.data)

    def last(self):
        item = None
        for item in self.data:
            pass

        return item


def make_sql_safe(string):
    '''
    Replaces all characters which are illegal for *SQL* statements to legal
    characters, as well as converting all legal characters to lower case.

    Based on the LabVIEW subVI:
    salt_tcs_els:source:trunk/src/support VIs/Replace illegal characters.vi
    '''
    # a dictionary of 'illegal': 'equivalent' string replacement pairs
    replacements = {
        ' ': '_',
        '/': '_',
        '-': '_',
        '%': 'percent',
        '?': '',
        '&': 'and',
        ',': '',
        '(': '',
        ')': '',
        'dec': 'declination',
        'declinationlination': 'declination',  # make backwards compatible
        '\'': '',
        '.': '_',
    }

    string = string.lower()

    for illegal, equivalent in replacements.items():
        string = string.replace(illegal, equivalent)

    return string


def collate_request(data_request):
    '''
    Suggested input format:
    [{
        'subsys': 'SubSys_name',
        'cluster': 'cluster_name',
        'element': 'element_name',
        'index': '2',
        'key': 'subsys_name--cluster_name--element_name--2',
        'dataType': 'array_boolean',
        'fromTime': '1424416440',
        'toTime': '1424420042',
        'limit': '1000000'
    }, {
        'subsys': 'SubSys_name',
        'cluster': 'cluster_name',
        'element': 'element_name',
        'index': '1',
        'key': 'subsys_name--cluster_name--element_name--1',
        'dataType': 'array_boolean',
        'fromTime': '1424416440',
        'toTime': '1424420042',
        'limit': '1000000'
    }]

    '''

    def sort_sc(dr):
        return f"{dr['subsys']}_{dr['cluster']}"

    def sort_e(dr):
        return dr['element']

    clusters = []
    # group by subsys_cluster
    for subsys_cluster, elements_it in groupby(
        sorted(data_request, key=sort_sc), sort_sc
    ):

        elements = []
        # group by element name
        for element, indices_it in groupby(sorted(elements_it, key=sort_e), sort_e):
            indices = []
            # iterate through each element index (might only be 1)
            for each in indices_it:
                try:
                    idx = int(each['index'])
                    if idx >= 0:
                        indices.append(idx)
                except KeyError:
                    pass
                finally:
                    data_type = each['dataType']
                    cluster = each['cluster']
                    subsys = each['subsys']

            elements.append(
                ElementData(name=element, type=data_type, indices=sorted(indices),)
            )

        first = data_request[0]
        clusters.append(
            ClusterData(
                name=subsys_cluster,
                subsys=subsys,
                cluster=cluster,
                elements=elements,
                start=datetime.fromtimestamp(int(first['fromTime'])),
                end=datetime.fromtimestamp(int(first['toTime'])),
                limit=int(first['limit']),
            )
        )

    return clusters


def _decode(ingredients, result):
    item = {'timestamp': result['_timestamp_']}
    for ingr in ingredients:
        # print(ingr)
        unpacked = unpack(
            value=result[make_sql_safe(ingr.element)],
            data_type=ingr.type,
            indices=ingr.indices,
            enum_desc=ingr.is_enum,
            size_flag=True,
        )
        size, unpacked = unpacked  # separate out blob size

        # Special Cases
        # For historical 'HRS - sensor temp status' race condition
        if (
            ingr.subsys == 'HRS'
            and ingr.cluster == 'sensor_temp_status'
            and ingr.element == 'Sensors'
        ):
            # print(size, ingr.indices, unpacked)

            if size == 9:
                # for idx, v in [(7, x),(8, y),(9, z)]:
                #     if idx >= 8:
                #         v = nan
                #     else:
                #         v = v
                #     return v
                unpacked = [
                    nan if idx >= 8 else v for idx, v in zip(ingr.indices, unpacked)
                ]

        item[ingr.name] = unpacked

    return item


class SaltCellar:
    def __init__(self, connection: str, **eng_kwargs):
        self.db_engine = sqlalchemy.create_engine(connection, **eng_kwargs)

    def _create_cluster_query(self, ingredients):
        '''Assembles SQL query from the various query bits'''

        # time in seconds from 1 Jan 1904 till 1 Jan 1970
        LabviewTimeOffset = 2082844800

        # extract query metadata from first element
        ingredient = ingredients[0]

        elements = ', '.join(
            [f"`{make_sql_safe(ingr.element)}`" for ingr in ingredients]
        )
        table = make_sql_safe(ingredient.subsys_cluster)
        start = ingredient.start.timestamp() + LabviewTimeOffset
        end = ingredient.end.timestamp() + LabviewTimeOffset

        return (
            f"SELECT "
            f"UNIX_TIMESTAMP(`_timestamp_`) AS `_timestamp_`, "
            f"{elements} "
            f"FROM {table}__timestamp "
            f"WHERE `timestamp` > {start} "
            f"AND `timestamp` < {end} "
            f"ORDER BY `timestamp` ASC "
            f";"
        )

    def single_query(
        self,
        fields: List[str],
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        **kwargs,
    ):
        '''
        Make a single query to a table that contains all requested fields
        '''
        ingredients = [Ingredient(each, start, end) for each in fields]
        query = self._create_cluster_query(ingredients)

        try:
            results = self.db_engine.execute(query)
        except sqlalchemy.exc.OperationalError as err:
            if "[Errno 111] Connection refused" in str(err):
                raise DatabaseUnavailableError(
                    "Connection to ELS database refused, please check credentials."
                )
            else:
                raise err

        decoded = (_decode(ingredients, each) for each in results)
        rc = ResultContainer(decoded, rowcount=results.rowcount)

        return rc
