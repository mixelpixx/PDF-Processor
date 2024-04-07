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

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def check_environment_variables():
    required_env_vars = ['PDF_SERVICES_CLIENT_ID', 'PDF_SERVICES_CLIENT_SECRET']
    for var in required_env_vars:
        if os.getenv(var) is None:
            logger.error(f"Environment variable {var} is not set.")
            raise Exception(f"Environment variable {var} is not set.")

def create_credentials():
    check_environment_variables()
    credentials = Credentials.service_principal_credentials_builder(). \
        with_client_id(os.getenv('PDF_SERVICES_CLIENT_ID')). \
        with_client_secret(os.getenv('PDF_SERVICES_CLIENT_SECRET')). \
        build()
    return credentials

def create_pdf_operation(file, credentials):
    execution_context = ExecutionContext.create(credentials)
    extract_pdf_operation = ExtractPDFOperation.create_new()
    source = FileRef.create_from_local_file(file.name)
    extract_pdf_operation.set_input(source)
    return extract_pdf_operation

def execute_operation(extract_pdf_operation):
    extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
        .with_elements_to_extract([ExtractElementType.TEXT, ExtractElementType.TABLES]) \
        .with_elements_to_extract_renditions([ExtractRenditionsElementType.TABLES,
                                              ExtractRenditionsElementType.FIGURES]) \
        .build()
    extract_pdf_operation.set_options(extract_pdf_options)
    result: FileRef = extract_pdf_operation.execute(execution_context)
    return result

def save_result(result):
    processed_folder = 'Processed'
    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)
    result.save_as(os.path.join(processed_folder, "ExtractTextTableWithFigureTableRendition.zip"))

def process_pdf(file):
    try:
        logger.info("Processing PDF...")
        credentials = create_credentials()
        extract_pdf_operation = create_pdf_operation(file, credentials)
        result = execute_operation(extract_pdf_operation)
        save_result(result)
        return "Processing complete. The result is saved in the 'Processed' folder."

    except ServiceApiException as e:
        logger.exception(f"Service API Exception encountered while executing operation: {e}")
        return f"An error occurred while processing the PDF: {e}"
    except ServiceUsageException as e:
        logger.exception(f"Service Usage Exception encountered while executing operation: {e}")
        return f"An error occurred while processing the PDF: {e}"
    except SdkException as e:
        logger.exception(f"SDK Exception encountered while executing operation: {e}")
        return f"An error occurred while processing the PDF: {e}"
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        return f"An unexpected error occurred: {e}"

iface = gr.Interface(
    fn=process_pdf,
    inputs=["file"],
    outputs="text",
    live=False,
    description="PDF Processor",
    allow_flagging=False,
    theme="huggingface",
    title="PDF Processor",
    analytics_enabled=False
)

logger.info("Starting Gradio Interface...")
iface.launch()
