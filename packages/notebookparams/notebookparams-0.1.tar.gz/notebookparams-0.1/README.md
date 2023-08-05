# notebookparams library

This library provides certain parameters for notebooks to be executed in ML environment. Following parameters can be obtained by calling the following methods from library:

#### Get notebook timeouts
--- get_notebook_timeout(notebook_timeout)
```
This method returns the timeouts for notebooks provided as argument to the method. for e.g.

get_notebook_timeout('INGESTION_NOTEBOOK_TIMEOUT')

Input: INGESTION_NOTEBOOK_TIMEOUT
Returns: 900

Input: EXPORT_NOTEBOOK_TIMEOUT
Returns: 300

Note:- Returned value is in seconds
```



