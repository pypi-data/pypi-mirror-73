import json
import sqlalchemy
import marshmallow
import configparser
import sqlalchemy.orm


class db:
    """
        Database abstraction layer for agnostic interfacing with DBMS.

        Wrapps arround SQLAlchemy to allow for ORM if needed.

        Supports querying into existing database schemas,
        that are built using a DDL.

        Example:
        ```
        db = i6.db(
            info = False,
            debug = True,
            db_conn_string = 'postgresql+psycopg2://user:password@host:5432/database'
        )

        # Provided with no arguments the class will read from the file
        # ./db_secret.ini using configparser

        # db_secret.ini:

        [postgresql]

        host     = 127.0.0.1

        database = schema_name

        user     = user_name

        password = user_password

        port     = 5432
        ```
    """

    __engine = None
    __info = None

    def __init__(self, info = None, debug = None, db_conn_string = None):
        try:
            self.set_engine(debug, db_conn_string)

            if (info is None) or (info == True):
                self.set_info()
        except:
            pass

    def get_config(self):
        """
            Looks into the 'db_secret.ini' file, and extracts config
            
            Example usage, The config for a postgresql database connection
            looks for the 'db_secret.ini' file, that should look like this:
            ```
            [postgresql]

            host     = 127.0.0.1

            database = schema_name

            user     = user_name

            password = user_password

            port     = 5432
            ```
        """

        try:
            filename = '.sec-db.ini'
            section = 'postgresql'

            parser = configparser.ConfigParser()
            parser.read(filename)

            db_config = dict()
            if parser.has_section(section):
                params = parser.items(section)
                db_config['dbms'] = section
                for param in params:
                    db_config[param[0]] = param[1]
            else:
                return '1'
        except:
            pass
            return '1'
        else:
            return db_config

    def set_engine(self, debug = None, db_conn_string = None):
        """
            Sets the engine member variable

            Example usage, init from constructor:
            ```
            self.set_engine(debug, db_conn_string)
            ```
        """

        try:
            if db_conn_string is None:
                params = self.get_config()

                if params != '1':
                    db_string = str()
                    db_string += params['dbms']
                    db_string += '://'
                    db_string += params['user']
                    db_string += ':'
                    db_string += params['password']
                    db_string += '@'
                    db_string += params['host']
                    db_string += ':'
                    db_string += params['port']
                    db_string += '/'
                    db_string += params['database']
                else:
                    return '1'

            else:
                db_string = str(db_conn_string)

            if debug == True:
                self.__engine = sqlalchemy.create_engine(db_string, echo=True)
            else:
                self.__engine = sqlalchemy.create_engine(db_string)
        except:
            pass
            return '1'
        else:
            return '0'

    def set_info(self):
        """
            Sets the info member variable
            
            Example usage, print id of table 1:
            ```
            print(db.info['tables'][0]['data'][0]['name'])
            ```
        """

        try:
            result = {'tables': []}
            inspector = sqlalchemy.inspect(self.__engine)

            for table in inspector.get_table_names():
                entry = {'table': table, 'data': []}
                for column in inspector.get_columns(table):
                    entry['data'].append(column)
                result['tables'].append(entry)
        except:
            pass
            return '1'
        else:
            self.__info = result
            return '0'

    def serialize_table(self, table_name = None, query = None):
        """
            Serializes the table of a given table_name

            Returns a serializable JSON object

            Uses the info member variable to get the database
            structure, and reflects the table onto a Marshmallow
            object.

            ```
            serialized = self.serialize_table(table_name=table_name, query=query)
            ```
        """

        try:
            # From info extract column names for table_name
            db_table = {'table':[]}
            tables = self.__info['tables']

            for data in tables:
                if data['table'] == table_name:
                    db_table['table'].append({'name':data['table'], 'columns':()})
                    for column in data['data']:
                        db_table['table'][0]['columns'] += (column['name'],)

            # Serialize Sqlalchemy result
            class SqlToJson(marshmallow.Schema):
                class Meta:
                    fields = db_table['table'][0]['columns']
            sql_to_json_many = SqlToJson(many=True)
            
            result = sql_to_json_many.dump(query)
        except:
            pass
            return '1'
        else:
            return result

    
    def call_proc(self, proc_name = None, input = None):
        """
            Calls a Stored procedure.

            Example usage, call stored procedure p_newest_time:
            ```
            db.call_proc('p_newest_time')
            ```
        """

        try:
            if input is None:
                input = ''

            query = 'CALL' + ' ' + str(proc_name) + '(' + str(input) + ')'
            
            session = sqlalchemy.orm.sessionmaker(bind=self.__engine)()
            session.execute(sqlalchemy.text(query))
            session.commit()
        except:
            pass
            try:
                session.rollback()
                return '1'
            except:
                pass
                return '1'
        finally:
            try:
                session.close()
                return '0'
            except:
                pass
                return '1'

    
    def set_table(self, table_name = None, data = None, remove_columns = None, json = None):
        """
            Insert statement, inserts into table_name, data, and removes_colums
            like ['id', 'time_stamp'] etc..

            Example usage, insert rows from table 'live_map' into table 'map',
            and remove columns, 'id' and 'time_stamp', since they are generated
            by the DBMS:
            ```
            result = db.get_table('live_map')

            for row in result:
                db.set_table('map', row, ['id', 'time_stamp'])
            ```
        """

        try:
            session = None
            if data is not None:

                if (json is None) or (json == True):
                    if (isinstance(data, str)):
                        data = json.loads(data)
                        
                if not isinstance(data, list):
                    arr = []
                    arr.append(data)
                    data = arr
                
                metadata = sqlalchemy.MetaData(bind=None)
                table = sqlalchemy.Table(table_name, metadata, autoload = True, autoload_with = self.__engine)
                session = sqlalchemy.orm.sessionmaker(bind=self.__engine)()

                for row in data:
                    if remove_columns is not None:
                        for i in range(len(remove_columns)):
                            if remove_columns[i] in row:
                                del row[remove_columns[i]]
                    session.execute(table.insert().values(row))
                
            else:
                raise Exception
        except:
            pass
            if session is not None:
                session.rollback()
            return_code = '1'
        else:
            if session is not None:
                session.commit()
            return_code = '0'
        finally:
            if session is not None:
                session.close()
            return return_code
    
    def get_table(self, table_name = None, json = None):
        """
            Select * from table_name

            Example usage, select all rows from table 'live_map':
            ```
            result = db.get_table('live_map')
            ```
        """

        try:
            # Select * from table_name
            metadata = sqlalchemy.MetaData(bind=None)
            table = sqlalchemy.Table(table_name, metadata, autoload = True, autoload_with = self.__engine)
            stmt = sqlalchemy.select([table])
            query = self.__engine.execute(stmt).fetchall()
            
            if query is None:
                raise Exception

            if (json is None) or (json == True):
                serialized = self.serialize_table(table_name=table_name, query=query)
                if serialized != '1':
                    result = json.dumps(serialized)
                else:
                    raise Exception
            else:
                result = query
        except:
            pass
            return '1'
        else:
            return result

    
    def print_table(self, table_name = None):
        """
            Print * from table_name

            Example usage, select and print all rows from table 'live_map':
            ```
            db.print_table('live_map')
            ```
        """

        try:
            print(self.get_table(table_name=table_name))
        except:
            pass
            return '1'
        else:
            return '0'

    def get_newest(self, table_name = None, query_key = None, json = None):
        """
            Get the newest record of table_name
            
            Select * from table_name order by id desc limit 1

            Example usage, select newest record in table 'live_map':
            ```
            result = db.get_newest('live_map')
            ```
        """

        try:
            metadata = sqlalchemy.MetaData(bind=None)
            table = sqlalchemy.Table(table_name, metadata, autoload = True, autoload_with = self.__engine)
            stmt = sqlalchemy.select([table]).order_by(sqlalchemy.desc(query_key)).limit(1)
            query = self.__engine.execute(stmt).fetchall()

            if (json is None) or (json == True):
                result = self.serialize_table(table_name=table_name, query=query)
            else:
                result = query

            if result == '1':
                raise Exception
            elif (json is None) or (json == True):
                result = json.dumps(result[0])
            else:
                result = result[0]
        except:
            pass
            return '1'
        else:
            return result
