# Hypothesis-Topic-Visualization

This project originated from the SciBeh workshop and should visualizes a given topic modelling of hypothes.is annotations. 
The current state should be considered as a *prototype* and is not ready for production yet.

The server uses a Django backend and was developed and tested on Python 3.8.6. The current deployment 
is on an Heroku instance at https://still-beach-75211.herokuapp.com/.

## Development
The development environment uses an SQLite database. Please use `DJANGO_SETTINGS_MODULE=hypothesis_topic_visualization.settings`
as settings. First install the requirements and initialize the database afterwards:
```
pip install -r requirements.txt
python manage.py migrate
```
Now import the default configuration (singleton) with the dedicated command:
```
python manage.py loaddata configuration.json
```
Afterwards the server can be started with the following command:
```
python manage.py runserver
```
The server now runs at http://localhost:8000

## Import annotation data
After everything is set up one can execute `python load_scibeh_documents.py` to import new annotations and topics.

```
usage: load_scibeh_documents.py [-h] -f DOCUMENTS_FILE -t TOPICS_FILE [--clear]

optional arguments:
  -h, --help            show this help message and exit
  -f DOCUMENTS_FILE, --documents-file DOCUMENTS_FILE
  -t TOPICS_FILE, --topics-file TOPICS_FILE
  --clear
```

The documents file should have the following format:
```
[
    {
        "id": "af8088d410dd5c42023672f007694d48b1ef8d86",
        "url": "http://example.com",
        "lang": "en",
        "type": "article",
        "title": "A title",
        "summary": "A summary",
        "tags": ["covid-19", "example-tag"],
        "date": "2020-10-23"
    },
    ...
]
```
The topics file should have the following format:
```
{
    "topics": [
        {
            "title": "A title",
            "description": "A description",
            "keywords": ["keyword1", "keyword2]
        },
        ...
    ],
    "documents": [
        {
          "id": "af8088d410dd5c42023672f007694d48b1ef8d86",
          "topics": [0.1, 0.3, ...] // Probability distribution over the topics that were defined before
        },
        ...
    ]
}
```

## Roadmap (new features)
* Improve search and integrate a system like vespa.ai or elasticsearch
* Improve the underlying topic model
* Visualize connections between topics (depending on the underlying model)
* Allow for more filter options during search
* Make topic allocations exchangeable, i.e. include a field that defines an allocations name and allow and admin
to switch to a different model.
* Extend the admin panel so that all models can be modified.
* Allow and admin to update the data instead of executing a script.

## Make the project production-ready
* Compile the Django project into a docker image
* Update the settings so that they are compatible with a Docker (maybe Kubernetes environment)
* Create an imprint
* Integrate a persistent database (which should be dependent on the deployment environment)
