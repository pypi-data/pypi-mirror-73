import psycopg2
import psycopg2.extras
from psycopg2.extras import DictCursor
from datetime import datetime
from humanize_db.utils.exceptions import TableNotFound
from humanize_db.core.db_entry import MetaEntry, AnnotationEntry, create_uuid
import logging

class ABDatabase:
    def __init__(self, **kwargs):
        if kwargs:
            try:
                self.conn = psycopg2.connect(**kwargs)
                self.cur = self.conn.cursor()
                self.tables = self.get_table_names()
            except (Exception, psycopg2.Error) as error :
                print ("Error while connecting to PostgreSQL", error)
        else:
            raise ValueError("Please insert valid parameters for db")
        psycopg2.extras.register_uuid()

    def init_tables(self):
        """Create tables in the PostgeSQL database"""
        tables = (
         """
        CREATE TABLE meta (
                            id SERIAL PRIMARY KEY,
                            meta_key VARCHAR NOT NULL,
                            seq VARCHAR NOT NULL,
                            chain_type VARCHAR,
                            iso_type VARCHAR,
                            germline VARCHAR,
                            species VARCHAR,
                            disease VARCHAR,
                            v_gene VARCHAR,
                            j_gene VARCHAR,
                            origin VARCHAR,
                            created_at TIMESTAMP,
                            UNIQUE (seq),
                            UNIQUE (meta_key)
                            )""",
        """
        CREATE TABLE kabat_annotation (
            kabat_id SERIAL PRIMARY KEY,
            meta_key VARCHAR NOT NULL,
            position VARCHAR,
            amino_acid CHAR(1),
            chain VARCHAR,
            region VARCHAR,
            FOREIGN KEY (meta_key) REFERENCES meta(meta_key) ON DELETE CASCADE
        )""",

        """
        CREATE TABLE imgt_annotation (
            imgt_id SERIAL PRIMARY KEY,
            meta_key VARCHAR NOT NULL,
            position VARCHAR,
            amino_acid CHAR(1),
            chain VARCHAR,
            region VARCHAR,
            FOREIGN KEY (meta_key) REFERENCES meta(meta_key) ON DELETE CASCADE
        )""",

        """
        CREATE TABLE chothia_annotation (
            chothia_id SERIAL PRIMARY KEY,
            meta_key VARCHAR NOT NULL,
            position VARCHAR,
            amino_acid CHAR(1),
            chain VARCHAR,
            region VARCHAR,
            FOREIGN KEY (meta_key) REFERENCES meta(meta_key) ON DELETE CASCADE
        )"""
        )
        try:
            for table in tables:
                self.cur.execute(table)
                self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)

    def insert_meta_entry(self, meta_obj):
        if isinstance(meta_obj, MetaEntry):
            new_meta_key = str(create_uuid())
            meta_obj.meta_key = new_meta_key
            meta_insert_query = "INSERT INTO meta (meta_key,seq,chain_type,iso_type,germline,species,disease,v_gene,j_gene,origin,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            meta_insert_values = (
                meta_obj.meta_key,
                meta_obj.sequence,
                meta_obj.chain_type,
                meta_obj.iso_type,
                meta_obj.germline,
                meta_obj.species,
                meta_obj.disease,
                meta_obj.v_gene,
                meta_obj.j_gene,
                meta_obj.origin,
                datetime.now())
            try:
                self.cur.execute(meta_insert_query,meta_insert_values)
                self.conn.commit()
                for anno_entry in meta_obj.get_annotation_data():
                    annotation_insert_values = (
                        anno_entry.meta_key,
                        anno_entry.position,
                        anno_entry.amino_acid,
                        anno_entry.chain,
                        anno_entry.region
                    )
                    if anno_entry.annotation_type == 'kabat':
                        query = "INSERT INTO kabat_annotation(meta_key,position,amino_acid,chain,region) VALUES (%s,%s,%s,%s,%s)"
                        self.cur.execute(query,annotation_insert_values)
                    if anno_entry.annotation_type == 'chothia':
                        query = "INSERT INTO chothia_annotation(meta_key,position,amino_acid,chain,region) VALUES (%s,%s,%s,%s,%s)"
                        self.cur.execute(query,annotation_insert_values)
                    if anno_entry.annotation_type == 'imgt':
                        query = "INSERT INTO imgt_annotation(meta_key,position,amino_acid,chain,region) VALUES (%s,%s,%s,%s,%s)"
                        self.cur.execute(query,annotation_insert_values)
                    self.conn.commit()
            except psycopg2.errors.UniqueViolation as e:
                self.conn.rollback()
                logging.error(e)
        else:
            raise TypeError('Insertion object must be of type MetaEntry.')


    def _drop_table(self,table_name):
        """Function to drop a specific table of current database. Confirmation needed.

        Parameters
        ----------
        table_name : string
            name of table

        Raises
        ------
        TableNotFound
            Raises if table does not exist in current database.
        """
        confirmation = input(f"Do you really want to delete the table {table_name}? [y/n]  ")
        if confirmation == "y":
            if table_name in self.tables:
                try:
                    query = " DROP TABLE "
                    query += table_name
                    query += ";"
                    self.cur.execute(query)
                    self.conn.commit()
                    print(f"\n+++ {table_name} DROPPED SUCCESSFULLY! +++\n")
                except (Exception, psycopg2.Error) as error:
                    print ("Error while connecting to PostgreSQL", error)
                    logging.error(error)
            else:
                raise TableNotFound("Could not find given table.")
        else:
            print("TABLE WAS NOT DELETED")

    def _drop_all_tables(self):
        """Function to drop all tables of database. USE CAREFULLY.
        """
        confirmation = input(f"Do you really want to delete ALL tables od the DB? [y/n]  ")
        if confirmation == "y":
            try:
                query = "DROP TABLE meta, chothia_annotation, imgt_annotation, kabat_annotation CASCADE; "
                self.cur.execute(query)
                self.conn.commit()
            except (Exception, psycopg2.Error) as error:
                logging.error(error)
        else:
            print("TABLE WAS NOT DELETED")

    def get_table_names(self):
        """Function to get names of all existing tables in database

        Returns
        -------
        string
            name of table
        """
        self.cur.execute("SELECT table_name FROM information_schema.tables WHERE (table_schema = 'public') ORDER BY table_name")
        db_tables_result = self.cur.fetchall()
        db_tables = []
        for entry in db_tables_result:
            db_tables.append(entry[0])
        return db_tables

    def show_table(self,table_name_list):
        """Function to show all entries of a database table.
        Results will be printed line by line in the shell.

        Parameters
        ----------
        table_name_list : string
            name of table

        Raises
        ------
        TableNotFound
            Raises if table does not exist in current database.
        """
        if all(tab_name in self.tables for tab_name in table_name_list):
            for table in table_name_list:
                sqlstate = f"SELECT * FROM {table} ;"
                self.cur.execute(sqlstate)
                results = self.cur.fetchall()
                for r in results:
                    print(r)
                if results == []:
                    print("No results found.")
        else:
            raise TableNotFound("Could not find given table.")

    def already_exists(self,seq):
        try:
            select_query = f"SELECT * FROM meta WHERE meta.seq='{seq}';"
            self.cur.execute(select_query)
            result = self.cur.fetchone()
            self.conn.commit()
            if result == None:
                return False
            return True
        except (Exception, psycopg2.Error) as error:
            self.conn.rollback()
            logging.error(error)

    def selectByMetaKey(self, meta_key):
        try:
            select_query = f"SELECT * FROM meta WHERE meta.meta_key='{meta_key}'"
            self.cur.execute(select_query)
            result = self.cur.fetchone()
            self.conn.commit()
            return result
        except (Exception, psycopg2.Error) as error:
            self.conn.rollback()
            logging.error(error)

    def selectByGermline(self, germline):
        try:
            select_query = f"SELECT * FROM meta WHERE meta.germline='{germline}'"
            self.cur.execute(select_query)
            result = self.cur.fetchone()
            self.conn.commit()
            return result
        except (Exception, psycopg2.Error) as error:
            self.conn.rollback()
            logging.error(error)

    def selectByPosition(self, table, position):
        try:
            select_query = f"SELECT * FROM {table} WHERE {table}.position='{position}'"
            self.cur.execute(select_query)
            result = self.cur.fetchall()
            self.conn.commit()
            return result
        except (Exception, psycopg2.Error) as error:
            self.conn.rollback()
            logging.error(error)

    def updateById(self, table, row_id ,position, meta_key):
        if table == 'kabat_annotation':
            id_column = "kabat_id"
        elif table == 'chothia_annotation':
            id_column = "chothia_id"
        elif table == 'imgt_annotation':
            id_column = "imgt_id"
        else:
            raise TableNotFound(f"Could not find table {table}.")
        try:
            update_query = f"UPDATE {table} SET position = '{position}' WHERE '{id_column}'='{row_id}' AND meta_key = '{meta_key}';"
            self.cur.execute(update_query)
            self.conn.commit()
        except (Exception, psycopg2.Error) as error:
            self.conn.rollback()
            logging.error(error)


    def updateMultipleEntries(self, table, entries):
        try:
            self.cur = self.conn.cursor(cursor_factory=DictCursor)
            if table == 'kabat_annotation':
                try:
                    qStr = "UPDATE kabat_annotation SET position = updated_position FROM (VALUES "
                    qParams = []
                    for entry in entries:
                        qStr += "(%s,%s,%s),"
                        qParams.extend([entry['id'], entry['meta_key'], entry['new_position']])
                    qStr = qStr[:-1]
                    qStr += " ) AS tmp(id, key, updated_position) WHERE (tmp.id = kabat_annotation.kabat_id) AND (tmp.key = kabat_annotation.meta_key)"
                    self.cur.execute(qStr, qParams)
                    self.conn.commit()
                except (Exception, psycopg2.Error) as error:
                    self.conn.rollback()
            elif table == 'chothia_annotation':
                try:
                    qStr = "UPDATE chothia_annotation SET position = updated_position FROM (VALUES "
                    qParams = []
                    for entry in entries:
                        qStr += "(%s,%s,%s),"
                        qParams.extend([entry['id'], entry['meta_key'], entry['new_position']])
                    qStr = qStr[:-1]
                    qStr += " ) AS tmp(id, key, updated_position) WHERE (tmp.id = chothia_annotation.chothia_id) AND (tmp.key = chothia_annotation.meta_key)"
                    self.cur.execute(qStr, qParams)
                    self.conn.commit()
                except (Exception, psycopg2.Error) as error:
                    self.conn.rollback()
            elif table == 'imgt_annotation':
                pass
            else:
                raise TableNotFound(f"{table} does not exist in db.")
        except Exception as err:
            logging.error(err)

    def selectBySequence(self, sequence):
        try:
            select_query = f"SELECT * FROM meta WHERE meta.seq='{sequence}'"
            self.cur.execute(select_query)
            result = self.cur.fetchone()
            self.conn.commit()
            return result
        except (Exception, psycopg2.Error) as error:
            self.conn.rollback()

    def meta_already_exists(self, key):
        try:
            select_query = f"SELECT meta_key FROM meta WHERE meta.meta_key='{key}';"
            self.cur.execute(select_query)
            result = self.cur.fetchone()
            self.conn.commit()
            if result == None:
                return False
            return True
        except (Exception, psycopg2.Error) as error:
            self.conn.rollback()
            logging.error(error)

    def update_germline(self, entries):
        try:
            qStr = "UPDATE meta SET germline = updated_germline FROM (VALUES "
            qParams = []
            for entry in entries:
                qStr += "(%s,%s,%s),"
                qParams.extend([entry['id'], entry['meta_key'], entry['germline']])
            qStr = qStr[:-1]
            qStr += " ) AS tmp(id, key, updated_germline) WHERE (tmp.id = meta.id) AND (tmp.key = meta.meta_key)"
            self.cur.execute(qStr, qParams)
            self.conn.commit()
        except (Exception, psycopg2.Error) as error:
            self.conn.rollback()
            logging.error(error)


    def close(self):
        """Function to close connection after ABDatabase instance was killed
        """
        self.cur.close()
        self.conn.close()

    def open(self,**kwargs):
        """Function to open database pipeline
        """
        self.conn = psycopg2.connect(**kwargs)
        self.cur = self.conn.cursor()
