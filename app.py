from flask import Flask, request, Response
import cal_parser
import logging
import sys
import re


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout)]
)

app = Flask(__name__)


@app.route('/ical-proxy', methods=['GET'])
def get_ical():
    if request.headers.getlist("X-Forwarded-For"):
        client_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        client_ip = request.remote_addr

    logging.info(f"Received request for ICAL calendar from {client_ip}")

    url = request.args.get('url')
    if not url:
        logging.error("No url provided")
        return "No url provided", 400

    try:
        ics_content, cal_name = cal_parser.generate_ics(url)
        cal_name = clean_filename(cal_name)
        logging.info(f"Response for ICAL calendar {cal_name} is sent")
        return Response(
            ics_content,
            mimetype='text/calendar',
            headers={'Content-Disposition': f"attachment; filename={cal_name}.ics"}
        )
    except Exception as e:
        logging.error(f"Error while generating ics: {str(e)}")
        return f"Error while generating ics: {str(e)}", 500

def clean_filename(filename):
    filename = filename.replace(' ', '_')
    return re.sub(r'[^\w\s-]', '', filename).strip()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)