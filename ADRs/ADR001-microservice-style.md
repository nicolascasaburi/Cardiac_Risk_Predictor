# ADR 001: Use the microservice architecture style
## Context
The purpose of the app is to predict cardiac risk according to the data provided by the patient. The team is considering the use of the microservice architectural style to enhance the app's scalability, maintainability, and flexibility.
## Decision
The team has decided to adopt the microservice architectural style for backend services in the app.
## Rationale
The microservice architecture is chosen to address the need for a highly automated, evolvable software system made up of capability-aligned microservices. This style of architecture allows the app to be built as a set of small, independent services, each running in its own process and communicating with lightweight mechanisms. This will enable the team to develop, deploy, and scale each service independently, leading to improved maintainability, flexibility, and scalability of the app
## Status
Accepted
## Consequences
The adoption of the microservice architectural style will lead to an improved scalability, and the ability to evolve and maintain the app more effectively. However, it may also introduce challenges related to the complexity of dealing with a system that spans a huge scope. The team will need to ensure effective communication and coordination among the microservices. Additionally, the team will need to invest in tools and practices that support this architectural style.
## Conclusion:
By adopting the microservice architectural style, the development team aims to enhance the app's maintainability, flexibility, and scalability. The team will need to carefully manage the challenges associated with the increased complexity and ensure effective communication and coordination among the microservices.
