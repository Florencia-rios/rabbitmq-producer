from flask import Flask

from queues_jobs_service.send import send_to_workers
from queues_nlp_worker.send import send_to_jobs_service_from_nlp
from queues_ocr_worker.send import send_to_jobs_service_from_ocr

# Creamos una instancia de la aplicación Flask
app = Flask(__name__)

@app.route('/job-ocr', methods=['POST'])
def send_job_to_ocr():
    return send_to_jobs_service_from_ocr()

@app.route('/job-nlp', methods=['POST'])
def send_job_to_nlp():
    return send_to_jobs_service_from_nlp()

@app.route('/job-finished', methods=['POST'])
def send_job_to_jobs_service():
    return send_to_workers()

if __name__ == '__main__':
    # Ejecutamos la aplicación Flask en el servidor local en el puerto 5000
    app.run(debug=True)