class Utility:

 @staticmethod
 def getIntent(response):   
    result = response.get("result")
    metadata = result.get("metadata")
    intentName=metadata.get("intentName")
    return intentName

 @staticmethod
 def getSpeech(response):
     result = response.get("result")
     fulfillment = result.get("fulfillment")
     speech = fulfillment.get("speech")
     return speech

 @staticmethod
 def getParm(request, parmName):
     result = request.get("result")
     parameters = result.get("parameters")
     return parameters.get(parmName)
