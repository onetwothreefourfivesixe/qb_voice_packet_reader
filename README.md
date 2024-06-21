# QB Voice Packet Reader (Flask Branch)

This branch of the QB Voice Packet Reader repository contains the Flask implementation of the QB Packet Reader application.

## Table of Contents

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## About

The QB Packet Reader is an application designed to read questions used in quiz bowl competitions out loud, while also printing the questions out as well. This branch utilizes the Flask framework to create a web-based interface for the QB Packet Reader.

## Installation

As this is still an unfinished project, as not all core features have been added, I would highly recommend not trying to run this locally yet.

But to install and run the Flask version of QB Voice Packet Reader, follow these steps:

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/onetwothreefourfivesixe/qb_packet_reader.git

   Or use Github Desktop.

2. Switch to the "flask" branch:

    ```bash
    git checkout flask

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    For Windows Users, you will need to first install the Aeneas Python package seperately beforehand. Click the following link to download the seperate installer: https://github.com/sillsdev/aeneas-installer/releases/download/v1.7.3.0_4/aeneas-win64-setup-1.7.3.0_4.exe

    For Linux users, simply go into the requirements.txt file, delete the first line, and replace it with:

    ```bash
    aeneas==1.7.3
    ```

    before running the previous command.

4. Run the application with the following command:

    ```bash
    flask run

5. Access the application in any web broswer at 'http://localhost:5000'.

## Usage

To actually make use of the application, press the 'n' key to bring up the next question, press space to buzz in, and press enter to submit your answer to the question.

Keep in mind, I am still working on this, so many features, such as changing the question type or reading speed, are not implemented yet.

## License

This project is licensed under the MIT License.