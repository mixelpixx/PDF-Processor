# Import the necessary libraries
import logging
import os.path
import gradio as gr
from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_renditions_element_type import \
    ExtractRenditionsElementType
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation

# Configure the logging level based on an environment variable or default to "DEBUG" level
logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))

def process_pdf(file):
    try:
        # Log the start of the process
        logging.info("Processing PDF...")
        
        # Create a credentials instance using client ID and secret from environment variables
        credentials = Credentials.service_principal_credentials_builder(). \
            with_client_id(os.getenv('PDF_SERVICES_CLIENT_ID')). \
            with_client_secret(os.getenv('PDF_SERVICES_CLIENT_SECRET')). \
            build()

        # Create an ExecutionContext using the credentials and a new ExtractPDFOperation instance
        execution_context = ExecutionContext.create(credentials)
        extract_pdf_operation = ExtractPDFOperation.create_new()

        # Use the uploaded file instead of hardcoded file path
        source = FileRef.create_from_local_file(file.name)
        extract_pdf_operation.set_input(source)  # Set this source file as the input for the operation

        # Build and set options for the PDF extraction operation, specifying what elements to extract
        extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
            .with_elements_to_extract([ExtractElementType.TEXT, ExtractElementType.TABLES]) \
            .with_elements_to_extract_renditions([ExtractRenditionsElementType.TABLES,
                                                  ExtractRenditionsElementType.FIGURES]) \
            .build()
        extract_pdf_operation.set_options(extract_pdf_options)  # Set these options in the operation

        # Execute the operation and get the result as a FileRef object
        result: FileRef = extract_pdf_operation.execute(execution_context)

        # Check if the "Processed" folder exists, if not create it
        processed_folder = 'Processed'
        if not os.path.exists(processed_folder):
            os.makedirs(processed_folder)

        # Save the result (a ZIP file containing the extracted data) to the "Processed" folder
        result.save_as(os.path.join(processed_folder, "ExtractTextTableWithFigureTableRendition.zip"))
        return "Processing complete. The result is saved in the 'Processed' folder."

    except (ServiceApiException, ServiceUsageException, SdkException) as e:
        logging.exception(f"Exception encountered while executing operation: {e}")
        return f"An error occurred while processing the PDF: {e}"
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        return f"An unexpected error occurred: {e}"

# Create Gradio interface
iface = gr.Interface(
    fn=process_pdf,  # function to call
    inputs=["file"],  # input type(s)
    outputs="text",  # output type
    live=False,  # disable live updates to change button label
    description="PDF Processor"  # change button label
)

# Log the start of the Gradio interface
logging.info("Starting Gradio Interface...")
iface.launch()



