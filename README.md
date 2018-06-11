Deadlox

A tool to allow you to view the current or most recent deadlock happening on your Google Cloud Proxy MySQL database

usage:
copy `env.sample` to `env` and populate the details of your MySQL database
execute `./run`

If attempting to run the python application without docker, uncomment out the `setup_env()` call and make sure to download the cloud sql proxy binary from here: https://cloud.google.com/sql/docs/mysql/connect-admin-proxy#service-account
copy it over to the same directory as the deadlox script 


future:
complete re-write in Go, using https://github.com/GoogleCloudPlatform/cloudsql-proxy as a library so that everything can run self contained as a single binary. 
