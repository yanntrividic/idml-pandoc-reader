import subprocess
import re
import sys
from packaging import version
import logging
from pathlib import Path

def check_java_version():
    """Returns the Java version
    Based on https://www.getorchestra.io/guides/how-to-check-java-version-in-python-with-apache-iceberg
    """
    try:
        # Run the 'java -version' command
        result = subprocess.run(['java', '-version'], stderr=subprocess.PIPE, text=True)
        # Java version information is in the stderr output
        output = result.stderr
        # Extract the version number
        if 'version' in output:
            version_line = output.splitlines()[0]
            java_version = version_line.split('"')[1]            
            # Extract the semantic versioning number using regex
            match = re.search(r'\d+\.\d+\.\d+', java_version)
            if match:
                semver = match.group(0)
                # Compare with 7.0.0 using packaging.version
                if version.parse(semver) >= version.parse("7.0.0"):
                    logging.info(f"Requirement met, Java version is {semver} (>= 7.0.0)")
                    return 1
                else:
                    logging.error(f"Java version {semver} is lower than required (>= 7.0.0).")
                    logging.error(f"Please install a more recent version.")
                    return -1
            else:
                logging.error("Could not extract a valid semantic version number from Java version string.")
                return -1
        else:
            logging.error("Java version could not be determined.")
            return -1
    except FileNotFoundError:
        logging.error("Java is not installed or not in the system PATH.")
        return -1

def idml2hubxml(input, **options):
    if check_java_version():
        logging.info("idml2hubxml starting...")

        filename = Path(input).stem

        output_folder = options["idml2hubxml_output"]

        if options["idml2hubxml_script"] is None:
            e = NameError("Your .env file is missing the IDML2HUBXML_SCRIPT_FOLDER entry")
            logging.error(e)
            raise e
        else:
            cmd = [options["idml2hubxml_script"] + "/idml2xml.sh", "-o", output_folder, input]
            logging.info("Now running: " + " ".join(cmd))
            subprocess.run(cmd, capture_output=True) # comment out this line to just get the previous run of idml2xml

        outputfile = output_folder + "/" + filename + ".xml"
        logfile = output_folder + "/" + filename + ".log"

        logging.info("Output of idml2xml written at: " + outputfile)
        logging.info("idml2xml log file written at: " + logfile)
        logging.info("idml2hubxml done.")
        return outputfile
    else:
        print("There is a problem with your Java installation. Please consult the logs.")
        sys.exit(1)