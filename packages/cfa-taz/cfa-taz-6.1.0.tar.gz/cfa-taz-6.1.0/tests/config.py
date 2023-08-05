keyvault = {
    "name": "kvdvldev",
    "secret_name": "REGISTRY-PASSWORD",
    "tenant_id": "4a7c8238-5799-4b16-9fc6-9ad8fce5a7d9",
    "client_id": "9d6f83f7-af2f-4a8d-b692-e2329dbbef9d",
    "client_secret": "C89nigG4BeonI",
}

databricks = {"token": "dapi4850c02947b5b0a24aecb7aadd8ee7da"}

auth = {
    "resource_group": "RG-APPLI-RED-DEV",
    "managed_identity": "mi-aci-wag-dev-01",
    "subscription_id": "5f82da32-5cad-49a4-aec5-5ba8806e6d9c",
    "tenant_id": "4a7c8238-5799-4b16-9fc6-9ad8fce5a7d9",
    "client_id": "1300f1b6-1bc2-4658-a504-86a1850805d2",
    "client_secret": "E.ZmS5LjjYpqjsb38=DgAn5WtIibBd.@",
}

blob = {
    "storage_account_name": "zstalrsdvllogdev01",
    "storage_key": "z++1cFPTnrNBNIM6QONcnjYUXa1VZuCs6DpsP+x9ELEuItoAZyM/W+FQLqlxsy/DWfjxywsJu5FjW2O7Wc3P1A==",
    "storage_connection_string": "DefaultEndpointsProtocol=https;AccountName=zstalrsdvllogdev01;AccountKey=z++1cFPTnrNBNIM6QONcnjYUXa1VZuCs6DpsP+x9ELEuItoAZyM/W+FQLqlxsy/DWfjxywsJu5FjW2O7Wc3P1A==;EndpointSuffix=core.windows.net",
    "sas_key": "?sv=2019-10-10&ss=bfqt&srt=sco&sp=rwdlacupx&se=2021-05-05T23:11:11Z&st=2020-05-05T15:11:11Z&spr=https&sig=LwTi%2BFlw4kLJWYip8oINKHOnwkNMZOE3HbYVrcQ32qg%3D",
    "sas_url": "https://zstalrsdvllogdev01.blob.core.windows.net/?sv=2019-10-10&ss=bfqt&srt=sco&sp=rwdlacupx&se=2021-05-05T23:11:11Z&st=2020-05-05T15:11:11Z&spr=https&sig=LwTi%2BFlw4kLJWYip8oINKHOnwkNMZOE3HbYVrcQ32qg%3D",
    "container_name": "unittest-taz",
    "path": "test.csv",
    "sas_url_path": "test_sas_url.csv",
    "sas_key_path": "test_sas_key.csv",
    "localpath": "/tmp/test.csv",
    "gzip_path": "test.csv.gz",
    "data": "col1,col2,col3\nval11,val12,val13\nval21,val22,val23",
}

tables = {
    "storage_account_name": "zstalrsdvllogdev01",
    "storage_key": "z++1cFPTnrNBNIM6QONcnjYUXa1VZuCs6DpsP+x9ELEuItoAZyM/W+FQLqlxsy/DWfjxywsJu5FjW2O7Wc3P1A==",
    "storage_connection_string": "DefaultEndpointsProtocol=https;AccountName=zstalrsdvllogdev01;AccountKey=z++1cFPTnrNBNIM6QONcnjYUXa1VZuCs6DpsP+x9ELEuItoAZyM/W+FQLqlxsy/DWfjxywsJu5FjW2O7Wc3P1A==;EndpointSuffix=core.windows.net",
    "sas_key": "?sv=2019-10-10&ss=bfqt&srt=sco&sp=rwdlacupx&se=2021-05-05T23:11:11Z&st=2020-05-05T15:11:11Z&spr=https&sig=LwTi%2BFlw4kLJWYip8oINKHOnwkNMZOE3HbYVrcQ32qg%3D",
    "sas_url": "https://zstalrsdvllogdev01.blob.core.windows.net/?sv=2019-10-10&ss=bfqt&srt=sco&sp=rwdlacupx&se=2021-05-05T23:11:11Z&st=2020-05-05T15:11:11Z&spr=https&sig=LwTi%2BFlw4kLJWYip8oINKHOnwkNMZOE3HbYVrcQ32qg%3D",
    "table_name": "taztest",
}

acr = {
    "resource_group": "RG-APPLI-RED-DEV",
    "registry_name": "crreddev",
    "subscription_id": "5f82da32-5cad-49a4-aec5-5ba8806e6d9c",
    "image_name": "hello-world",
}

aci = {
    "resource_group": "RG-APPLI-RED-DEV",
    "container_group_name": "cg-taz-test-unit",
    "location": "northeurope",
    "subscription_id": "5f82da32-5cad-49a4-aec5-5ba8806e6d9c",
    "logs_sas_key": "?sv=2019-02-02&ss=bfqt&srt=sco&sp=rwdlacup&se=2021-04-05T02:04:07Z&st=2020-04-04T18:04:07Z&spr=https&sig=gcK6vxvENtBnXfCfVj7nPxdSsQYcY4rS4W740fTKA80%3D",
    "logs_container": "unittest-taz",
    "logs_storage_account": "zstalrsdvllogdev01",
}

dls = {
    "dls_name": "lemanhprod",
    "tenant_id": "4a7c8238-5799-4b16-9fc6-9ad8fce5a7d9",
    "client_id": "e3952129-496b-416b-a244-67c43bd5bddd",
    "client_secret": "/KauQDlt2yiL34n9xsCxPLJMgKVzf.==",
    # "https_proxy": "host.docker.internal:3128",
    "https_proxy": "localhost:3128",
    "path": "SNCF/landing/input/METEOFRANCE/data_files/OBSERVATIONS_5MN/2019",
    "glob_path": "SNCF/landing/input/METEOFRANCE/data_files/OBSERVATIONS_5MN/2019/matriceSNCF_20191212*",
    "file_name": "matriceSNCF_201905201520.csv",
    "gz_file_name": "SNCF/landing/input/METEOFRANCE/data_files/PREVISIONS/20190123/previsions_20190123_J1.csv.gz",
    "tmp_file_name": "/tmp/taz.tmp",
}

dls_glob = {}

queue = {
    "storage_account_name": "zstalrsdvllogdev01",
    "storage_connection_string": "DefaultEndpointsProtocol=https;AccountName=zstalrsdvllogdev01;AccountKey=z++1cFPTnrNBNIM6QONcnjYUXa1VZuCs6DpsP+x9ELEuItoAZyM/W+FQLqlxsy/DWfjxywsJu5FjW2O7Wc3P1A==;EndpointSuffix=core.windows.net",
    "queue_name": "taztest",
}
