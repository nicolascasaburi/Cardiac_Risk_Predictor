# ADR 006: Use of docker containers to distribute the microservices
## Context
The purpose of the app is to predict cardiac risk according to the data provided by the patient. The app will use microservices to perform different tasks such as log into the database, model prediction and user authentication. The microservices will be distributed using Docker containers.
## Decision
We will use Docker containers to distribute the microservices.
## Rationale
Docker containers provide a lightweight and portable way to package and distribute microservices. They allow us to isolate each microservice and its dependencies, making it easier to manage and deploy them. Docker containers also provide a consistent runtime environment, ensuring that the microservices will run the same way across different machines and environments. This makes it easier to test and deploy the app. Additionally, Docker containers provide a scalable and flexible way to distribute the microservices, allowing us to easily add or remove microservices as needed.
## Status
Accepted
## Consequences
Using Docker containers to distribute the microservices will require some additional setup and configuration. We will need to create Docker images for each microservice and configure the Docker containers to communicate with each other. We will also need to manage the Docker containers and ensure that they are running correctly. However, the benefits of using Docker containers outweigh the additional setup and configuration required.
## Conclusion
Using Docker containers to distribute the microservices is a good decision for our app. It provides a lightweight, portable, and scalable way to package and distribute the microservices. It also ensures a consistent runtime environment and makes it easier to manage and deploy the app.