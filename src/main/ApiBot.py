from __future__ import print_function

from future.standard_library import install_aliases

from src.main.Intents.ClassAuthorName import ClassAuthorName
from src.main.Intents.GetCommitNamesByDate import GetCommitNamesByDate
from src.main.Intents.GetInfoAboutClass import GetInfoAboutClass
from src.main.Intents.GetWhoChangedOnClass import GetWhoChangedOnClass
from src.main.Intents.GetLatestCommitInformation import GetLatestCommitInformation
from src.main.Intents.GetLatestCommitInformationByName import GetLatestCommitInformationByName
from src.main.Intents.GetNumberOfCommitByDate import GetNumberOfCommitByDate
from src.main.Intents.GetCommentBodyByDateAndName import GetCommentBodyByDateAndName
from src.main.Intents.GetCommentBodyByDate import GetCommentBodyByDate
from src.main.Intents.IssueIntents.BugTicketsIssuedByCommit import BugTicketsIssuedByCommit
from src.main.Intents.IssueIntents.BuggyCommitsByDate import BuggyCommitsByDate
from src.main.Intents.IssueIntents.BugsCountsPerStatus import BugsCountsPerStatus
from src.main.Intents.IssueIntents.FixingCommitRate import FixingCommitRate
from src.main.Intents.IssueIntents.FixingCommitsForBugTicket import FixingCommitsForBugTicket
from src.main.Intents.IssueIntents.FixingCommitsIntroducedBugs import FixingCommitsIntroducedBugs
from src.main.Intents.IssueIntents.MostDeveloperHasOpenedClosedBugs import MostDeveloperHasOpenedClosedBugs
from src.main.Intents.IssueIntents.MostFileContainsBugs import MostFileContainsBugs
from src.main.Intents.IssueIntents.MostOccuranceBug import MostOccuranceBug
from src.main.Intents.IssueIntents.GetDevelopersWhoHasExperianceToFixBug import GetDevelopersWhoHasExperianceToFixBug
from src.main.Intents.UnknownIntent import UnknownIntent

install_aliases()

import json
import os
from src.main.Utility import *

from flask import Flask, request, session
from flask_cors import CORS, cross_origin
from src.main.OZAPIConstants import IntentConstants
import apiai
import time
import sys


developer_key = ""  # Your Dialogflow developer key here.

# Flask app should start in global layout
app = Flask(__name__)
app.secret_key = '' # Your app secret key here.
CORS(app, supports_credentials=True)

@app.route('/', methods=['POST'])
def webhook():

        # Read the user message.
        userMsg = request.form['userMsg']
        print(userMsg)

        # Call Dialogflow API.
        ai = apiai.ApiAI(developer_key)
        x = ai.text_request()
        x.session_id = "SID212192934"
        x.query = userMsg   # Send the user message as the query to Dialogflow.

        response = x.getresponse().read()   # Store the response.
        jsonResult = json.loads(response)   # Make it into json format.
        print(response)

        # Get the user message from the json response.
        speech = Utility.getSpeech(jsonResult)
        if speech != "":
           return speech

        # Get the intent name from the response.
        intentName = Utility.getIntent(jsonResult)

        # prepare the intent object given the intent name.
        userIntent = getIntent(intentName, jsonResult)

        # Process the response to the user's intent.
        resultToReturn = userIntent.ProcessRespone()

        return resultToReturn



def makeWebhookResult(stringToSend):

    speech = stringToSend

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
    }

def getIntent(intent, req):
    if (intent == IntentConstants.Get_Latest_Commit_Intent):
        returnedIntent = GetLatestCommitInformation(req)

    elif (intent == IntentConstants.Get_Latest_Commit_By_Dev_Name_Intent):
        returnedIntent = GetLatestCommitInformationByName(req)

    elif (intent == IntentConstants.Get_Commit_Body_By_Date_Period_And_Dev_Name_Intent):
        returnedIntent = GetCommentBodyByDateAndName(req)

    elif (intent == IntentConstants.Get_Commit_Body_By_Date_Period_Intent):
        returnedIntent = GetCommentBodyByDate(req)

    elif (intent == IntentConstants.Get_Name_Of_Who_Commit_By_Date_Intent):
        returnedIntent = GetCommitNamesByDate(req)

    elif (intent == IntentConstants.Get_Number_Of_Commit_By_Date_Intent):
        returnedIntent = GetNumberOfCommitByDate(req)

    elif (intent == IntentConstants.CLASS_AUTHOR_NAME_INTENT):
        returnedIntent = ClassAuthorName(req)

    elif (intent == IntentConstants.Get_Developers_Who_Made_Class_Changes):
        returnedIntent = GetWhoChangedOnClass(req)

    elif (intent == IntentConstants.Get_Commits_Info_Of_Specific_Class):
        returnedIntent = GetInfoAboutClass(req, False)

    elif (intent == IntentConstants.Get_Latest_Commit_Info_Of_Specific_Class):
        returnedIntent = GetInfoAboutClass(req, True)

    elif (intent == IntentConstants.Most_Occurance_Bug_Intent):
        returnedIntent = MostOccuranceBug(req)

    elif (intent == IntentConstants.Bugs_Counts_Per_Status):
        returnedIntent = BugsCountsPerStatus(req)

    elif (intent == IntentConstants.Most_Developer_Has_Opened_Bugs):
        returnedIntent = MostDeveloperHasOpenedClosedBugs(req, "Open")

    elif (intent == IntentConstants.GET_DEVELOPERS_WHO_HAS_EXPERIANCE_TO_FIX_BUG):
        returnedIntent = GetDevelopersWhoHasExperianceToFixBug(req)
#==============================================================================================
    elif (intent == IntentConstants.FIXING_COMMITS_FOR_BUG_TICKET):
        returnedIntent = FixingCommitsForBugTicket(req)

    elif (intent == IntentConstants.BUG_TICKETS_ISSUED_BY_COMMIT):
        returnedIntent = BugTicketsIssuedByCommit(req)

    elif (intent == IntentConstants.MOST_FILE_CONTAINS_BUGS):
        returnedIntent = MostFileContainsBugs(req)

    elif (intent == IntentConstants.BUGGY_COMMITS_BY_DATE or intent == IntentConstants.FIXING_COMMITS_BY_DATE):
        returnedIntent = BuggyCommitsByDate(intent, req)

    elif (intent == IntentConstants.Fixing_COMMITS_RATE or intent == IntentConstants.BUGGY_COMMITS_RATE): ## There is no intent defined in the NLU but the functionality is ready
        returnedIntent = FixingCommitRate(intent, req)

    elif (intent == IntentConstants.FIXING_COMMITS_INTRODUCED_BUGS):
        returnedIntent = FixingCommitsIntroducedBugs(req)

    elif (intent == "greeting"):
        returnedIntent = "Hi"

    elif (intent == "HowAreYou"):
        returnedIntent = "I am fine :)"

    else:
        returnedIntent = UnknownIntent(req)

    return returnedIntent


if __name__ == '__main__':

    # Start listening on port 6543.
    port = int(os.getenv('PORT', 6543))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='127.0.0.1')

