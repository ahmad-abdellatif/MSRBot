#INTENTS CONSTANTS
class IntentConstants:
    GET_COMMENT = "GetComment"
    GET_NAME = "GetName"

    Get_Latest_Commit_Intent = 'GetLatestCommitIntent'
    Get_Latest_Commit_By_Dev_Name_Intent = 'GetLatestCommitByDevNameIntent'
    Get_Commit_Body_By_Date_Period_And_Dev_Name_Intent = 'GetCommitBodyByDatePeriodAndDevNameIntent'

    FIXING_COMMITS_FOR_BUG_TICKET = "FixingCommitsForBugTicket"
    BUG_TICKETS_ISSUED_BY_COMMIT = "IntroducedBugsByCommit"
    MOST_FILE_CONTAINS_BUGS = "MostFileContainsBugs"
    BUGGY_COMMITS_BY_DATE = "BuggyCommitsByDate"
    FIXING_COMMITS_BY_DATE = "FixingCommitsByDate"
    BUGGY_COMMITS_RATE = "BuggyCommitsRate"
    Fixing_COMMITS_RATE = "FixingCommitsRate"
    FIXING_COMMITS_INTRODUCED_BUGS = 'FixingCommitsIntroducedBugs'

    Get_Name_Of_Who_Commit_By_Date_Intent = 'GetNameOfWhoCommitByDateIntent'

    RESULT_COULD_NOT_BE_FOUND = "Sorry, I could not find any result for your question"

    CLASS_AUTHOR_NAME_INTENT = 'GetClassAuthorName'
    Get_Developers_Who_Made_Class_Changes = 'GetDevelopersWhoMadeClassChanges'
    Get_Commit_Body_By_Date_Period_Intent = 'GetCommitBodyByDatePeriod'
    Get_Number_Of_Commit_By_Date_Intent = 'GetNumberOfCommitByDate'
    Get_Commits_Info_Of_Specific_Class = 'GetCommitsInfoAboutSpecificClass'
    Get_Latest_Commit_Info_Of_Specific_Class = 'GetLatestCommitInfoOfSpecificClass'
    GET_DEVELOPERS_WHO_HAS_EXPERIANCE_TO_FIX_BUG = 'GetDevelopersWhoHasExperianceToFixBug'

    Most_Occurance_Bug_Intent = 'MostOccuranceBug'
    Bugs_Counts_Per_Status = 'BugsCountsPerStatus'
    Most_Developer_Has_Opened_Bugs = 'MostDeveloperHasOpenedBugs'
    Most_Developer_Has_Closed_Bugs = 'MostDeveloperHasClosedBugs'

#ENTITY CONSTANTS
class EntityConstants:
    DATE = "date"
    LAST_ENTITY = "Last-Entity"
    DEVELOPERS_NAME_ENTITY = "Developers-Name"
    LATEST_ENTITY = "Latest"
    CLASS_NAME = "ClassesNames"
    JIRA_TICKETS = "JIRATickets"
    COMMIT_HASH = "CommitHash"