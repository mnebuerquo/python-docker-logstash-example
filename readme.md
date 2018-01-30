# Dockerized Python Logstash Test App

Uses logstash for logging all Python events.

# How do I use this?

0. Clone [this docker-compose ELK stack example](https://github.com/deviantony/docker-elk).
   This is the recommended example of how to use docker-compose for
   Elasticsearch, Logstash, and Kibana (ELK).
1. Add a section to the logstash config:
    ```
        tcp {
            port => 5999
            codec => json
        }
    ```
2. Add the json codec to the logstash Dockerfile so it will be installed at
   build time:
   ```
   RUN logstash-plugin install logstash-codec-json
   ```
3. Add port 5999 to logstash in the docker-compose.yml.
4. Create .env file in this repository's directory. This contains the environment
   for your app. (See `env.sample` for an example.) Set the following variables:
   * LOGSTASH_HOST=dockerelk_logstash_1
   * LOGSTASH_PORT=5999
   * FLASK_APP=src/flask_app.py
   * FLASK_DEBUG=1
5. Now build this app's Docker image:
   ```sh
   ./mn_build
   ```
6. Run the first test app, to generate some log data:
   ```sh
   ./python src/app.py
   ```
7. Open Kibana and see if you have content in Elasticsearch.
    1. Navigate to [http://localhost:5601](http://localhost:5601)
    2. Click *Management* in the left menu, then *Index Patterns*. Then choose
       `timestamp` for the time series value and click save.
    3. Click Discover in the left menu. You should see logstash as the selected
       index in the gray column in the left middle. If you see "No Results
       Found" then run your app again and click the magnifying glass in the
       search box above.
    4. When you have data you should see blue bars in the timeline and log
       records in a list below. It may take several seconds for log events to
       make it to Elasticsearch. If you don't see them in 20 seconds, there is
       probably something configured incorrectly.
8. Run the flask app:
   ```sh
   ./flask run --host=0.0.0.0
   ```
9. Hit the website and see "Hello World.":
   ```sh
   curl http://localhost:6000
   ```
10. Check Kibana again to see your logged messages from flask.

# Links
* https://github.com/deviantony/docker-elk
* https://github.com/eht16/python-logstash-async
* https://github.com/ulule/python-logstash-formatter
* https://github.com/mnebuerquo/create-python-app
* https://stackoverflow.com/questions/6234405/logging-uncaught-exceptions-in-python
