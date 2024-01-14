# ADR 002: Use of Python as the programming language
## Context
The purpose of the app is to predict cardiac risk according to the data provided by the patient.
## Decision
Python was chosen as the programming language for developing the app.
## Rationale
Python is a popular programming language for machine learning and data analysis. It offers a wide range of libraries and frameworks, such as Keras, for developing machine learning models. Its simplicity and readability make it well-suited for rapid development and prototyping, which is beneficial for a project like this. Additionally, Flask is a widely used web framework for Python, making it a suitable choice for developing the app's backend. Pymongo allows easy integration with MongoDB, which is a popular database for storing unstructured data, such as the one used in this project.
## Status
Accepted
## Consequences
The use of Python provides access to a rich ecosystem of machine learning and data analysis tools, which can facilitate the development of the cardiac risk prediction app. However, it's important to ensure that the selected libraries and frameworks are well-maintained and have strong community support to mitigate potential risks associated with dependencies.
## Conclusion
The decision to use Python as the programming language for the app is well-founded, considering its suitability for machine learning and web development, as evidenced by its widespread use in similar projects and the availability of relevant libraries and frameworks.
