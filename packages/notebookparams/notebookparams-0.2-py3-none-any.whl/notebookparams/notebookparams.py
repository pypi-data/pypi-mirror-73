
def get_notebook_path(notebook_path):
    switcher = {
        'INGESTION_NOTEBOOK_PATH' : INGESTION_NOTEBOOK_PATH,
        'CONNECT_NOTEBOOK_PATH'   : CONNECT_NOTEBOOK_PATH
    }

    return switcher.get(notebook_path, "Notebook path does not exist")

def get_notebbook_timeout(notebook_timeout):
    switcher = {
        'INGESTION_NOTEBOOK_TIMEOUT'       : INGESTION_NOTEBOOK_TIMEOUT,
        'CLTV_NOTEBOOK_TIMEOUT'            : CLTV_NOTEBOOK_TIMEOUT,
        'P13N_NOTEBOOK_TIMEOUT'            : P13N_NOTEBOOK_TIMEOUT,
        'SMARTSEGMENT_NOTEBOOK_TIMEOUT'    : SMARTSEGMENT_NOTEBOOK_TIMEOUT,
        'CONNECT_NOTEBOOK_TIMEOUT'         : CONNECT_NOTEBOOK_TIMEOUT,
        'POST_NOTEBOOK_TIMEOUT'            : POST_NOTEBOOK_TIMEOUT,
        'EXPORT_NOTEBOOK_TIMEOUT'          : EXPORT_NOTEBOOK_TIMEOUT
    }

    return switcher.get(notebook_timeout, "Notebook timeout value does not exist")

def get_corporation_id(corp_id):
    switcher = {
            'BRONZE_CORPORATION_ID_1'     : BRONZE_CORPORATION_ID_1,
            'BRONZE_CORPORATION_ID_2'     : BRONZE_CORPORATION_ID_2,
            'GOLD_CLTV_CORPORATION_ID_1'  : GOLD_CLTV_CORPORATION_ID_1,
            'GOLD_CLTV_CORPORATION_ID_2'  : GOLD_CLTV_CORPORATION_ID_2
    }
    return switcher.get(corp_id, "corporation id does not exist")

def get_brand_id(brand_name):
    switcher = {
        'BRONZE_BRAND_1'     : BRONZE_BRAND_1['BRAND_ID'],
        'BRONZE_BRAND_2'     : BRONZE_BRAND_2['BRAND_ID'],
        'GOLD_CLTV_BRAND_1'  : GOLD_CLTV_BRAND_1['BRAND_ID'],
        'GOLD_CLTV_BRAND_2'  : GOLD_CLTV_BRAND_2['BRAND_ID']
    }
    return switcher.get(brand_name, "brand name does not exist")

def get_external_id(brand_name):
    switcher = {
        'BRONZE_BRAND_1'    : BRONZE_BRAND_1['EXTERNAL_ID'],
        'BRONZE_BRAND_2'    : BRONZE_BRAND_2['EXTERNAL_ID'],
        'GOLD_CLTV_BRAND_1' : GOLD_CLTV_BRAND_1['EXTERNAL_ID'],
        'GOLD_CLTV_BRAND_2' : GOLD_CLTV_BRAND_2['EXTERNAL_ID']
    }
    return switcher.get(brand_name, "brand external id does not exist")

#if __name__ == '__main__':
INGESTION_NOTEBOOK_PATH        = '../cgp-corporation-ingest/alsea-historical-ingest'
CONNECT_NOTEBOOK_PATH          = '../cgp-data-connect/alsea-demo-connect'
INGESTION_NOTEBOOK_TIMEOUT     = '900'
CLTV_NOTEBOOK_TIMEOUT          = '2700'
P13N_NOTEBOOK_TIMEOUT          = '2700'
SMARTSEGMENT_NOTEBOOK_TIMEOUT  = '2700'
CONNECT_NOTEBOOK_TIMEOUT       = '300'
POST_NOTEBOOK_TIMEOUT          = '300'
EXPORT_NOTEBOOK_TIMEOUT        = '300'

BRONZE_CORPORATION_ID_1                    = '560e8801-0e8a-465e-a34f-9e14fbcbd174'
BRONZE_CORPORATION_ID_2                    = 'e4b8ffc4a6884c828781cd16a4005e4d'
BRONZE_BRAND_1                             = {'BRAND_ID': '8c2c8c28-7267-4b7b-84f2-c45be3834cb6', 'EXTERNAL_ID': '36001'}
BRONZE_BRAND_2                             = {'BRAND_ID': 'f0fbce53-ebf4-4893-8d04-f043a6f7dc93', 'EXTERNAL_ID': '31017'}
GOLD_CLTV_CORPORATION_ID_1                 = '560e8801-0e8a-465e-a34f-9e14fbcbd174'
GOLD_CLTV_CORPORATION_ID_2                 = 'e4b8ffc4a6884c828781cd16a4005e4d'
GOLD_CLTV_BRAND_1                          = {'BRAND_ID': '8c2c8c28-7267-4b7b-84f2-c45be3834cb6', 'EXTERNAL_ID': '36001'}
GOLD_CLTV_BRAND_2                          = {'BRAND_ID': 'f0fbce53-ebf4-4893-8d04-f043a6f7dc93', 'EXTERNAL_ID': '31017'}

#print(get_corporation_id('GOLD_CLTV_CORPORATION_ID_1'))