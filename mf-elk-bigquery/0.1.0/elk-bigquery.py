#!/usr/bin/python3
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from google.api_core.exceptions import BadRequest
from google.cloud import bigquery
from google.oauth2 import service_account
import argparse
import json
import time
import sys

class elk_bigquery():
    def __init__(self):
        # Elasticsearch client
        try:
            self.es_client = Elasticsearch(host='localhost', port=9200)
        except:
            sys.exit("Error creating elasticsearch client. Exit")


    # Issue the query and get results in json format
    def get_json_data_from_elasticsearch(self, query, index):
        try:
            result = scan(client=self.es_client,
                      query=json.loads(query),
                      scroll='1m',
                      index=index,
                      raise_on_error=True,
                      preserve_order=False,
                      clear_scroll=True)

            json_result = list(result)
            return (json_result)
        except:
            sys.exit("Error executing the query. Exit.")
    
    # Turn a nested dictionary into a dictionary that only has one layer of keys
    # Key names reformated as firstlayer_secondlayer_thirdlayer, connected by underscore
    def flatten_dict(self, nested_dict, parent_key='', sep='_'):
        try:
            items = []
            for key, value in nested_dict.items():
                new_key = f"{parent_key}{sep}{key}" if parent_key else key
                if isinstance(value, dict):
                    items.extend(self.flatten_dict(value, new_key, sep=sep).items())
                else:
                    items.append((new_key, value))       
            return dict(items)
        except:
            sys.exit("Error flattening the json data into one line per object. Exit")

    # Read the data from _source and merge it with the meta data
    # Flatten the json results: one json object per line
    def reformat_data(self, json_results, output_file='output.json'):
        try:
            final_results = []
            for item in json_results:
                meta_data={}
                meta_data['_id'] = item['_id']
                meta_data['_index'] = item['_index']
                #meta_data['_score'] = item['_score']
                meta_data['_type'] = item['_type']
                #print (meta_data)
                item_in_source = item['_source']
                item_in_source['timestamp']=item_in_source['@timestamp']
                del (item_in_source['@timestamp']) 
         
                merged_object= meta_data.copy()
                merged_object.update(item_in_source)
                #print (merged_object)
                updated_object=self.flatten_dict(merged_object, sep='_')
                final_results.append(updated_object)
     
            with open(output_file, 'w') as out:
                for item in final_results:
                    json_line = json.dumps(item)
                    out.write(json_line + '\n')  
        except:
            sys.exit("Error processing the data. Exit.")




    # Specify the bigquery schema and output the schema to a json file
    def specify_bigquery_schema(self, input_file='output.json', output_file='schema.json'):
        json_objects = []
        with open(input_file, 'r') as input:
            for line in input:
                json_object = json.loads(line)
                json_objects.append(json_object)
        with open(output_file, 'w') as schema_file:
            schema_objects = []
            for object in json_objects:
                #schema_object={}
                for key in object.keys():
                    schema_object={}
                    if (isinstance(object[key],dict)):
                        schema_object['name']=key
                        schema_object['type']='JSON'
                        if (schema_object not in schema_objects):
                            schema_objects.append(schema_object)
                    elif (isinstance(object[key],str)):
                        schema_object['name']=key
                        schema_object['type']='STRING' 
                        if (schema_object not in schema_objects):
                            schema_objects.append(schema_object)
                    elif (isinstance(object[key],bool)):
                        schema_object['name']=key
                        schema_object['type']='BOOL' 
                        if (schema_object not in schema_objects):
                            schema_objects.append(schema_object)
                    elif (isinstance(object[key],list)):
                        unique_types = set(type(item) for item in object[key])
                        if (len(unique_types)==1):
                            if (isinstance(object[key][0],str)):
                                schema_object['name']=key
                                schema_object['type']='STRING'
                                schema_object['mode']='REPEATED'
                            elif (isinstance(object[key][0],int) or isinstance(object[key][0],float)):
                                schema_object['name']=key
                                schema_object['type']='FLOAT64' 
                                schema_object['mode']='REPEATED'
                            elif (isinstance(object[key][0],dict)):
                                schema_object['name']=key
                                schema_object['type']='JSON' 
                                schema_object['mode']='REPEATED'
                        if (schema_object not in schema_objects):
                            schema_objects.append(schema_object)
                    elif (isinstance(object[key],int)):
                        schema_object['name']=key
                        schema_object['type']='FLOAT64' 
                        if (schema_object not in schema_objects):
                            schema_objects.append(schema_object)
                    elif (isinstance(object[key],float)):
                        schema_object['name']=key
                        schema_object['type']='FLOAT64' 
                        if (schema_object not in schema_objects):
                            schema_objects.append(schema_object)
            json.dump(schema_objects, schema_file)

# Create bigquery client using the key and schema and  upload data 
    def upload_data(self, key_file_path, table_id, schema_file_path='schema.json', data_file_path='output.json'):
        credentials = service_account.Credentials.from_service_account_file(
        key_file_path,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

        bigquery_client=bigquery.Client(
            credentials=credentials,
            project=credentials.project_id,
        )
        schema = bigquery_client.schema_from_json(schema_file_path)
        
        # LoadJobConfig constructor
        job_config = bigquery.LoadJobConfig(
            # autodetect=True,
            schema=schema,
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            write_disposition='WRITE_APPEND'
        ) 
        # Allow column addition if data to be dumped to the same table has more columns(different schema)
        job_config.schema_update_options = [
            bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION
        ]

        # Upload the data
        with open(data_file_path, 'rb') as input_file:
            job = bigquery_client.load_table_from_file(input_file, table_id, job_config=job_config)

        while job.state != 'DONE':
            job.reload()
            time.sleep(3)

        try:
            print (job.result())
        except BadRequest as e:
            for e in job.errors:
                print('ERROR: {}'.format(e['message']))




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='python script to export elasticsearch data to bigquery')
    parser.add_argument('--query', type=str, required=True, help='query for elasticsearch data ')
    parser.add_argument('--index', type=str, required=True, help='name of elasticsearch index')
    parser.add_argument('--key', type=str, required=True, help='bigquery service account key file path')
    parser.add_argument('--table', type=str, required=True, help='bigquery table id')
    args = parser.parse_args()
    eb=elk_bigquery()
    eb.reformat_data(eb.get_json_data_from_elasticsearch(query=args.query, index=args.index))
    time.sleep(2)
    eb.specify_bigquery_schema()
    time.sleep(2)
    eb.upload_data(key_file_path=args.key, table_id=args.table)



