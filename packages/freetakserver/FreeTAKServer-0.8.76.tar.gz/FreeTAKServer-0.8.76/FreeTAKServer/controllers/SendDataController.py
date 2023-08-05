from logging.handlers import RotatingFileHandler
import logging
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
import sys
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
loggingConstants = LoggingConstants()
logger = CreateLoggerController("SendDataController").getLogger()


class SendDataController:

    def __init__(self):
        pass
    def sendDataInQueue(self, sender, processedCoT, clientInformationQueue, internalCoT = None):
        try:
            try:
                if processedCoT.modelObject.m_detail.Marti.m_Dest.callsign != '':
                    for client in clientInformationQueue:
                        try:
                            if client.modelObject.m_detail.m_Contact.callsign == processedCoT.modelObject.m_detail.Marti.m_Dest.callsign:
                                sock = client.socket
                                try:
                                    sock.send(processedCoT.xmlString)
                                except:
                                    logger.error('error sending data with marti to client data ' + str(processedCoT.xmlString) + 'error is '+str(e))
                                    return -1
                            else:
                                continue
                        except Exception as e:
                            logger.error('error sending data with marti to client within if data is ' + str(processedCoT.xmlString) + 'error is '+str(e))
                            return -1
                    return 1
            except:
                pass
            
            if sender == processedCoT:
                for client in clientInformationQueue:
                    try:
                        sock = client.socket
                        sock.send(processedCoT.idData.encode())
                        sender.socket.send(client.idData.encode())
                    except Exception as e:
                        logger.error('error in sending connection data ' + str(processedCoT.idData) + 'error is '+str(e))
                        return -1
                for CoT in internalCoT:
                    try:
                        sock = client.socket
                        sock.send(CoT.xmlString)
                    except Exception as e:
                        logger.error('error in sending internal CoT data to newly connected client data is ' + str(CoT.xmlString))
                return 1


            else:
                for client in clientInformationQueue:
                    if client != sender:

                        sock = client.socket
                        try:
                            sock.send(processedCoT.xmlString)
                        except Exception as e:
                            logger.error('error in sending of data ' + str(processedCoT.xmlString)+ 'error is '+ str(e))
                            continue
                    else:
                        continue
                return 1
        except Exception as e:
            logger.error(loggingConstants.SENDDATACONTROLLERSENDDATAINQUEUEERROR+str(e))
            return -1