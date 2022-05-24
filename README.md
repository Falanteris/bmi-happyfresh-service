BMI API Server
=============


HappyFresh Test project to measure Body Mass Index (BMI) though an API call.


Prerequisites
-------
The project is deployed via Docker and Docker Compose. In order to deploy it, you'll have to install Docker and Docker Compose first.

Installing Docker : _https://docs.docker.com/engine/install/_

Installing Docker Compose : _https://docs.docker.com/compose/install/_

And that's it!.The rest are containerized.


Run
-----

All you need to do is to run `docker-compose up -d app` which runs the application.

    docker-compose up -d app


Testing Changes / Revision
------

- Setup

In the `docker-compose.yml` file, there's a specific service that can allow immediate tests without needing to install anything from `requirements.txt`

All you need to do is `build` and `up` the service itself. Like so.


    docker-compose build app_test

    # building processes goes here..

    docker-compose up app_test 

    # test your revision of the code with test suites

- Configuration

You can modify the environment of which the test server is being hosted at by changing the `SERVICE_HOST` and `SERVICE_PORT` environment.

`SERVICE_HOST` ==> Network Interface to bind ( use 0.0.0.0 if you want to bind to all Interfaces)
`SERVICE_PORT` ==> Port where the API is listening from

Though, if you wish to access the `metrics` of the API, it is currently immutable and listening to connections on port `8070`. If the service collides with another service
listening to the port, you can remap the `metrics` port to another.

    - ports:
        - <IP>:<Port>:8070

