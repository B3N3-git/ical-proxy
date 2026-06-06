from flask import Flask, request, Response
import cal_parser  # Importiere dein Skript
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout)] # Expliziter StreamHandler
)

app = Flask(__name__)


@app.route('/ical_url', methods=['GET'])
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
        logging.info(f"Response for ICAL calendar {cal_name} is sent")
        return Response(
            ics_content,
            mimetype='text/calendar',
            headers={'Content-Disposition': 'attachment; filename=calendar.ics'}
        )
    except Exception as e:
        logging.error(f"Error while generating ics: {str(e)}")
        return f"Error while generating ics: {str(e)}", 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)