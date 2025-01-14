import datetime
from webService import WebService
import Utilidades as ut
import PanoptoUpload as panup
import sys
import csv
import requests
import sys


if __name__ == "__main__":
    param = ut.mainRecordings(sys.argv[1:])
    webService = WebService() 
    report = []
    reporte_403 = []
    recordings_ids = ut.readCollabReport(param[0])
    if recordings_ids != None:
        print("Reading recordigns_id from file Admin Collab Report- recordings")
        for recording in recordings_ids:
            grabacion = webService.get_grabacion_uuid_data(recording['recording'])
            if grabacion == None:
                reporte_403.append([
                            recording['sessionOwner'],
                            recording['sessionName'],
                            recording['sessionId'],
                            recording['recording'],
                            recording['recName'],
                            'Not read access or resource do not exist'
                        ])        
            else:
                recording_lista = ut.listaGrabacionCollabData(grabacion)
                if recording_lista != None:
                    report_record = [recording['sessionOwner'],recording['recording'],recording_lista['recording_name'],recording_lista['duration'],recording_lista['size'],recording_lista['created']]
                    report.append(report_record)
                    recording_lista['recordingId'] = recording['recording']
                    ut.downloadRecordingsUUID(recording_lista)
                    panup.uploadrecordingUUID(recording_lista)
        if len(report) > 0: 
                print(ut.crearReporte(report))
        else:
            print('No downloading was executed')

        if len(reporte_403) > 0:
            print(ut.crearReporte_Recordings_403(reporte_403))
        else:
            print('No private recording was found')
    else:
        print("The file is not Recordings Report format")
     




