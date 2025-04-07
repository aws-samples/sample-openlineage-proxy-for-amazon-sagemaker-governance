def get_redshift_serverless_namespace(original_namespace, redshift_serverless_client):
    """Function to get a compatible namespace for redshift serverless based on a reference one"""
    redshift_name = original_namespace.split('://')[1].split('.')[0]
    response = redshift_serverless_client.get_workgroup(workgroupName=redshift_name)
    if response['workgroup'] != {}:
        workgroup_endpoint = response['workgroup']['endpoint']
        namespace = f"redshift://{workgroup_endpoint['address']}:{workgroup_endpoint['port']}"
    
    else: namespace = original_namespace
    
    return namespace