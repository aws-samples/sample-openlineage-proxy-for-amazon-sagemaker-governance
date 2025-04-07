import os
import json
import boto3

from event_utils import dict_get_key_values, dict_replace_key_values
from namespace_utils import get_redshift_serverless_namespace

DOMAIN_ID = os.environ['DOMAIN_ID']

datazone = boto3.client('datazone')
redshift_serverless = boto3.client('redshift-serverless')

def create_update_map(original_namespaces_and_names):
    """Creates a dict to map namespaces and names into new ones accepted by DataZone"""
    update_map = {}
    for namespace, name in original_namespaces_and_names:
        if 'redshift://' in namespace: 
            update_map[name] = {'namespace': get_redshift_serverless_namespace(namespace, redshift_serverless), 'name': name}
        else: 
            update_map[name] = {'namespace': namespace, 'name': name}

    return update_map

def lambda_handler(event, context):
    
    event_summaries = []
    for record in event['Records']:
        
        # Read lineage event
        lineage_event = json.loads(record['body'])
        print("\n  Full original event:")
        print(json.dumps(lineage_event))

        lineage_event_summary = {
            'run_id': lineage_event['run']['runId'],
            'event_type': lineage_event['eventType'],
            'event_time': lineage_event['eventTime'],
            'job_name': lineage_event['job']['name'],
            'inputs': [input['name'] for input in lineage_event['inputs']],
            'outputs': [output['name'] for output in lineage_event['outputs']],
            'event_len': len(record['body'])
        }

        try:
            # Translate event namespaces for DataZone compatible ones - Best Effort
            namespaces_and_names = set()
            dict_get_key_values(lineage_event, ['namespace', 'name'], namespaces_and_names)
            update_map = create_update_map(namespaces_and_names)
            
            # Apply updates to event twice. First when namespace is the key to find and second when name is the key to find
            new_lineage_event = lineage_event.copy()
            dict_replace_key_values(new_lineage_event, update_map)

            print("\n  Full new event:")
            print(json.dumps(new_lineage_event))
            
            # Post Lineage Event into DataZone
            datazone.post_lineage_event(domainIdentifier=DOMAIN_ID, event=json.dumps(new_lineage_event))
            lineage_event_summary['post_status'] = 'Succeeded'
            print("\n  Succeeded.")

        except Exception as e:
            lineage_event_summary['post_status'] = 'Failed'
            print("\n  Failed.")
            print(f"Error: {e}")

        finally:
            event_summaries.append(lineage_event_summary)

    print("\n  Final Summary:")
    print(json.dumps(event_summaries))
    
    return {
        'statusCode': 200,
        'body': json.dumps('All lineage events covered, check logs for possible errors')
    }
