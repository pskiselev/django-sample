# It's the sample for processing image data with meta-information. 

## The solution based on Django and DRF. It's restful

The main idea is object Image with annotation relates one-to-one. The restriction of file size is 20 MB.

### Data representation
It can be difference for clients and internal-usage-users. 
In order not to duplicate the code, you can use different formats provided by the DRF
In most cases, I would suggest using query parameter different from 'format' because of it's for different types of format (e.g. json, csv, xlsx)
But here, as an example, the parameter "format" is used to represent the json for different types of use

### Image representation 
In general, storing images in your own database can often lead to performance problems, so I would recommend using something like AWS and only keeping a link to it. As an example, we will use a database and provide an opportunity to get it not from the database, but directly from the data store provided by Django.
For these purposes, you can use nginx, which will act as a reverse proxy server to serve static and media files.


### How to run
    Just run "docker-compose up"
For convenience, I use docker containerization, which will allow you to launch the application with one command and not install anything other than docker
Also, The link https://www.reddit.com/r/django/comments/bjgod8/dockerizing_django_with_postgres_gunicorn_and/ can be helpful
You can see docker-compose file (with dockerfiles for building). Also, I use one image for two services. One of it run application and other one for migrating db


### Data collection
REST uploading files (multiform) doesn't allow push a file with json data, but annotations we should store as 3-NF because it can be helpful in future (e.g. for calculate something).
Due to this, A request should contain two files (image and annotation.json). The last one parsed to relations as possible.


### Data storage
In this case I have only "Label" object. Due to this, DB looks like
#### Image <--> Annotation <-- Labels

### Additional
I don't like to use many 'if' statements. In cases of several types of representation the same data I use auxiliary class as registry to get needed serializer class for specified format. it's a good solution to add new formats in future.

