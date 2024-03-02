# PDF-Processor

PDF-Processor is a Python application that uses Adobe's PDF Services SDK to extract text and tables from PDF files. The extracted data is saved as a ZIP file in the 'Processed' folder. This application provides a user-friendly interface to upload and process PDF files.

## Overview of the Code

The main script (`main.py`) performs the following steps:

1. Configures logging level.
2. Defines a function `process_pdf` that:
    - Logs the start of the process.
    - Creates a credentials instance using client ID and secret from environment variables.
    - Creates an ExecutionContext using the credentials and a new ExtractPDFOperation instance.
    - Sets the uploaded file as the input for the operation.
    - Builds and sets options for the PDF extraction operation, specifying what elements to extract.
    - Executes the operation and gets the result as a FileRef object.
    - Checks if the "Processed" folder exists, if not creates it.
    - Saves the result (a ZIP file containing the extracted data) to the "Processed" folder.
3. Creates a Gradio interface to interact with the `process_pdf` function.
4. Launches the Gradio interface.

## Requirements


## Installation

1. Install the Adobe PDF Services SDK for Python. You can find the SDK and installation instructions [here](https://acrobatservices.adobe.com/dc-integration-creation-app-cdn/main.html?api=pdf-extract-api).
2. Install the Gradio library using pip:
    ```
    pip install gradio
    ```
3. Clone this repository or download the source code.
4. Replace the placeholders in the `Credentials/pdfservices-api-credentials.json` file with your Adobe PDF Services API credentials.

## Usage

1. Run the `launch_app.bat` file. This will start the Python script and open a new browser window with the Gradio interface.
2. In the Gradio interface, upload the PDF file you want to process.
3. Click the 'Submit' button to start the processing. Once the processing is complete, you will see a message indicating the successful completion of the process.
4. The result (a ZIP file containing the extracted data) will be saved in the 'Processed' folder.
