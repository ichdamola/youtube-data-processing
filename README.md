# YouTube Data Processing Application

[![Codecov](https://codecov.io/github/ichdamola/youtube-data-processing/graph/badge.svg?token=WEQLCYEIU0)](https://codecov.io/github/ichdamola/youtube-data-processing)
[![Codecov Graph](https://codecov.io/gh/ichdamola/youtube-data-processing/graphs/sunburst.svg?token=WEQLCYEIU0)](https://codecov.io/github/ichdamola/youtube-data-processing)

<img width="1470" alt="screen" src="https://github.com/user-attachments/assets/68006549-f808-4ecd-be58-d3f9f3a2fd33">


## Overview

This project processes YouTube data using the YouTube API. It allows you to retrieve and manage video comments, providing insights into user interactions.

## Prerequisites

Before running the application, ensure you have the following:

1. **Python 3.x** installed on your machine.
2. **pip** for managing Python packages.
3. A valid **YouTube API Key** to access the YouTube Data API.

## Getting Started

To see how this project works locally, follow these steps:

### 1. Obtain Your YouTube API Key

Ensure you have your YouTube API Key ready. You can obtain it by creating a project in the [Google Developers Console](https://console.developers.google.com/).

### 2. Setup the Environment

Run the following command to set up the application environment:

```bash
make setup
```
This command will:

- Create a `.env` file for environment variables.
- Prompt you to enter your YouTube API key.
- Install required Python packages.
- Run database migrations.

### 3. Run Tests

To run the tests and check the code coverage, execute:

```bash
make test
```

This will:

- Run the test suite.
- Generate a coverage report.
- Upload coverage data to Codecov.

### 4. Run the Application

Start the application server with the following command:

```bash
make run
```

This command will launch the development server, allowing you to interact with the application locally.

## More Info

### Codecov Integration

The application uses Codecov for continuous integration and code coverage tracking. You can view detailed coverage reports and metrics on [Codecov](https://codecov.io/github/ichdamola/youtube-data-processing).

## Demo Video


https://github.com/user-attachments/assets/96eb6f17-640b-41b3-b29b-d18cc7cc7396



## License

This project is licensed under the MIT License. See the LICENSE file for details.
