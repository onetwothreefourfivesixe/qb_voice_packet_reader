# QB Voice Packet Reader (Flask Branch)

This branch of the QB Voice Packet Reader repository contains the Flask implementation of the QB Packet Reader application.

## Table of Contents

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## About

The QB Packet Reader is an application designed to read questions used in quiz bowl competitions out loud, while also printing the questions out as well. This branch utilizes the Flask framework to create a web-based interface for the QB Voice Packet Reader. All questions are sourced from https://qbreader.org through its API.

## Installation

As this is still an unfinished project, I would highly recommend not trying to run this locally yet.

But to install and run the Flask version of QB Voice Packet Reader, follow these steps:

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/onetwothreefourfivesixe/qb_packet_reader.git
   ```

   Or use Github Desktop.

2. Switch to the "flask" branch:

    ```bash
    git checkout flask
    ```

    Or switch branches using Github Desktop.

3. For Windows Users, you may need to first install the Aeneas Python package seperately beforehand. Click the following link to download the seperate installer: https://github.com/sillsdev/aeneas-installer/releases/download/v1.7.3.0_4/aeneas-win64-setup-1.7.3.0_4.exe

    Otherwise, just make sure you have ffmpeg, ffprobe (usually provided by the ffmpeg package), and espeak installed and available on your command line before you continue to the next steps.

4. Create a Python Enviorment (venv). If you are using VS Code and Windows, do the following:
    
    a. Open the project in VS Code.
    b. Press ```bash Ctrl + Shift + P``` to bring up the commands.
    c. Search ```bash Python: Create Enviroment```.
    d. select ```bash Venv ```.
    e. If you used the Aeneas Python installer, select to use the 3.9.13 Python interpreter when making the enviorment.
    f. Run ```bash .venv\Scripts\activate```.

    For Non-Windows users, go to the following tutorial in order to do the same thing: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/.

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```
    
    If you did not follow step 3, delete the first line, and replace it with:

    ```bash
    aeneas==1.7.3
    ```

    before running the previous command.

4. Run the application with the following command:

    ```bash
    flask run

5. Access the application in any web broswer at 'http://localhost:5000'.

## Usage

To actually make use of the application, press the 'n' key to bring up the next question, press space to buzz in, and press enter to submit your answer to the question. If you want to switch the category or difficulty of the question, click 'Select question categories:' and 'Select question difficulties' respectively. These will reveal dropdown menus where you can select any combination of categories and difficulties to use. If you notice any similarites in the UI to QBReader, those are unintentional and not meant to directly copy it.

Keep in mind, I am still working on this, so many features, such changing reading speed, are not implemented yet.

## License

This project is licensed under the MIT License.