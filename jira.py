import http.client
import configparser
import datetime as dt
import sys
import base64
import time
import logging
import teradata

def softdeleteproject(session,project):
    executed = True
    for value in session.execute("UPDATE AMO.PROJECTS_MASTER SET DELETED = 'Y' WHERE PROJECT_KEY = '" + str(project) + "';"):
        executed = False
    if executed:
        logger.info("Project has been soft deleted from Project Master-- " + str(project))

def moveproject(session,old_project,new_project):
    executed = True
    for value in session.execute("UPDATE AMO.PROJECTS_MASTER SET DELETED = 'Y',MOVED_TO = '"+new_project+"' WHERE PROJECT_KEY = '" + old_project + "';"):
        executed = False
    if executed:
        logger.info("Project " + old_project +" has been marked as Deleted and Moved in Project Master-- ")

def updateBusinesslogic(session):

      for update in session.execute("Update amo.PROJECTS_MASTER set deleted = 'Y' where PROJECT_KEY in (SELECT PROJECT_KEY from amo.TEAMS_MASTER where DELETE_REPORTING = 'YES') AND deleted = 'N';"):
        pass
      with session.cursor() as newcursor:
          for update in newcursor.execute("update amo.PROJECTS_MASTER	set REPORTED = 'Y' where PROJECT_KEY in ( SELECT PROJECT_KEY FROM amo.TEAMS_MASTER where DELETE_REPORTING is null) AND REPORTED = 'N';"):
            pass
      logger.info("Business Logic Updated in the PROJECTS_MASTER table")


# def getissuetype(issuekey,token):
#     import json
#     retries = 0
#     while retries < 10:
#         retries = retries + 1
#         try:
#             conn = http.client.HTTPSConnection("sonypictures.atlassian.net")
#             headers = {
#                 'authorization': token,
#                 'cache-control': "no-cache",
#             }
#             # conn.request("GET", "/rest/api/2/issue/SENG-967", headers=headers)
#             conn.request("GET", "/rest/api/2/issue/" + issuekey + "/", headers=headers)
#             res = conn.getresponse()
#         except Exception as exp:
#             # print("Retrying after exception : ",str(dt.datetime.now()), exp)
#             logger.exception("Retrying ( " + str(retries) + " ) after exception : ")
#             time.sleep(5)
#             continue
#         break
#     data = res.read()
#     jsonstr = data.decode("utf-8")
#     jsondata = json.loads(jsonstr)
#
#     return jsondata['fields']['issuetype']['name']

# def getissuedetails(issuekey,token):
#     import json
#     #retries = 0
#     #while retries < 10:
#     for retries in range(1,21):
#         #retries = retries + 1
#         try:
#             conn = http.client.HTTPSConnection("sonypictures.atlassian.net")
#             headers = {
#                 'authorization': token,
#                 'cache-control': "no-cache",
#             }
#             # conn.request("GET", "/rest/api/2/issue/SENG-967", headers=headers)
#             conn.request("GET", "/rest/api/2/issue/" + issuekey + "/", headers=headers)
#             res = conn.getresponse()
#         except Exception as exp:
#             # print("Retrying after exception : ",str(dt.datetime.now()), exp)
#             logger.exception("Retrying ( " + str(retries) + " ) after exception : ")
#             time.sleep(5)
#             continue
#         break
#     data = res.read()
#     jsonstr = data.decode("utf-8")
#     jsondata = json.loads(jsonstr)
#     issuetype = None
#     business_value = None
#     Category = None
#     issuetype = jsondata['fields']['issuetype']['name']
#
#     for value in jsondata['issues']:
#         try:
#             for Categoryvalue in value['fields']['customfield_10191']:
#                 Category = Categoryvalue['value']
#         except Exception as exp:
#             "No Business Value for the issues"
#         try:
#             for businessvalue in value['fields']['customfield_10219']:
#                 business_value = businessvalue['value']
#         except Exception as exp:
#             "No Business Value for the issues"
#
#     return [issuetype,business_value,Category]

def getAllIssuesOfJIRAProjectSinceInception(project,token):
    import http.client
    import json

    conn = http.client.HTTPSConnection("sonypictures.atlassian.net")
    headers = {
        'authorization': token,
        'cache-control': "no-cache"
    }
    conn.request("GET", "/rest/api/2/search?jql=project="+project+"%20AND%20status%20changed%20to%20Released&startAt=0&maxResults=1", headers=headers)
    #conn.request("GET",
    #             "/rest/api/2/search?jql=project=" + project + "%20AND%20status%20changed%20to%20released%20after%20-92d%20before%20-0d%20&startAt=0&maxResults=1",
    #             headers=headers)
    res = conn.getresponse()
    data = res.read()
    jsonstr = data.decode("utf-8")
    jsondata = json.loads(jsonstr)

    try:
        print("Total issues in ",project," is :- ",jsondata['total'])
    except Exception as exp:
                logger.exception("Not able to acesss the Project : "+project)

    conn = http.client.HTTPSConnection("sonypictures.atlassian.net")
    headers = {
        'authorization': token,
        'cache-control': "no-cache"
    }

    endrange = jsondata['total']
    Counter = 0
    allissuessinceinception = []
    while (Counter < endrange):

        conn.request("GET", "/rest/api/2/search?jql=project="+project+"%20AND%20status%20changed%20to%20Released&startAt=" + str(Counter) + "&maxResults=100",headers=headers)

        res = conn.getresponse()
        data = res.read()
        jsonstr = data.decode("utf-8")
        jsondata = json.loads(jsonstr)

        Counter = Counter + 100
        for value in jsondata['issues']:
            issue_key = str(value['key'])
            issue_type = str(value['fields']['issuetype']['name'])
            business_value = []
            try:
                for businessvalue in value['fields']['customfield_10191']:
                    business_value.append(businessvalue['value'])
            except Exception as exp:
                pass
            category = None
            try:
                category = value['fields']['customfield_10219']['value']
            except Exception as exp:
                pass
            allissuessinceinception.append([issue_key,issue_type,business_value,category])

    return allissuessinceinception

def getLastNIssuesOfJIRAProject(project,lastNthissues,token):
    import http.client
    import json

    conn = http.client.HTTPSConnection("sonypictures.atlassian.net")
    headers = {
        'authorization': token,
        'cache-control': "no-cache"
    }

    Counter = 0
    allissuessinceinception = []
    while (Counter < lastNthissues):

        conn.request("GET", "/rest/api/2/search?jql=project="+project+"&startAt=" + str(Counter) + "&maxResults=100",headers=headers)
        res = conn.getresponse()
        data = res.read()
        jsonstr = data.decode("utf-8")
        jsondata = json.loads(jsonstr)

        Counter = Counter + 100
        for value in jsondata['issues']:
            allissuessinceinception.append(str(value['key']))

    return allissuessinceinception

def getAllprojectsOfJIRA(session,token):
    import json
    import http.client
    conn = http.client.HTTPSConnection("sonypictures.atlassian.net")
    headers = {
        'authorization': token,
        'cache-control': "no-cache"
    }
    conn.request("GET", "/rest/api/2/project", headers=headers)
    res = conn.getresponse()
    data = res.read()
    jsonstr = data.decode("utf-8")
    jsondata = json.loads(jsonstr)
    counter = 0
    for projectdetail in jsondata:
        doesprojectexit = True
        for value in session.execute("SELECT DISTINCT PROJECT_KEY from AMO.PROJECTS_MASTER WHERE PROJECT_KEY = '" + projectdetail['key'] + "';"):
            doesprojectexit = False

        if doesprojectexit:
            counter = counter + 1
            logger.info('Inserting -- '+str(counter) +" : "+str(projectdetail['id'])+ ", " +str(projectdetail['key'])+ ", " +str(projectdetail['name']))
            session.execute(
                "INSERT	INTO AMO.PROJECTS_MASTER (PROJECT_ID, PROJECT_KEY, PROJECT_NAME,CREATED_DT,REPORTED) VALUES (" + projectdetail[
                    'id'] + ", '" + projectdetail['key'] + "','" + projectdetail['name'].replace("'","''").replace("$","$$") + "',current_timestamp,'N');")
        else:
            counter = counter + 1
            #print('Ignored - Project already exist -- ',counter," : ", projectdetail['key'])
            logger.info('Ignored - Project already exist -- '+str(counter)+" : "+str(projectdetail['key']))

def getAllIssuesOfJIRAProject(session,LastNthIssuesToBeScanned,token):

    counter = 0
    #for project in session.execute("SELECT DISTINCT PROJECT_ID, PROJECT_KEY, PROJECT_NAME, CREATED_DT FROM AMO.PROJECTS_MASTER WHERE DELETED = 'N' AND PROJECT_KEY NOT IN ('GDS','MSPSD','GDSSD','GN1') AND PROJECT_KEY = 'GMDM';"):
    for project in session.execute("SELECT DISTINCT PROJECT_ID, PROJECT_KEY, PROJECT_NAME, CREATED_DT FROM AMO.PROJECTS_MASTER WHERE DELETED = 'N' AND REPORTED = 'Y' AND PROJECT_KEY NOT IN ('MSPSD','GDSSD','GN1','MSTE','JSD','GLOBE','AMOS','DPOC','PHTM5','LEGT','DPOC','DRURD');"):

        counter = counter +1
        #print(counter," : ",project[1])
        logger.info("Data Fetch Starts for " + str(counter)+" : "+str(project[1]))

        # Get all the issues of the project (project[1]) from the JIRA
        all_issues_n_issuetype_of_project_from_JIRA = getAllIssuesOfJIRAProjectSinceInception(project[1],token)

        #allissuesofprojectfromJIRA = getLastNIssuesOfJIRAProject(project[1],LastNthIssuesToBeScanned)

        # Get all the issues of the project (project[1]) from the DB
        all_issues_of_project_from_DB =  []
        with session.cursor() as newcursor:
                        for rows in newcursor.execute("SELECT DISTINCT ISSUE_KEY from AMO.ISSUES_MASTER WHERE PROJECT_KEY = '" + str(project[1]) + "';"):
                            # print(type(rows))
                            all_issues_of_project_from_DB.append((str(rows[0])))

        logger.info("From JIRA  : " + str(len(all_issues_n_issuetype_of_project_from_JIRA)))
        logger.info("From DB  : " + str(len(all_issues_of_project_from_DB)))

        # The issues which are not in DB but are in JIRA
        issues_to_be_inserted = []
        for issues in all_issues_n_issuetype_of_project_from_JIRA:
            if issues[0] not in all_issues_of_project_from_DB:
                issues_to_be_inserted.append(issues)

        logger.info("To Be Inserted : " + str(len(issues_to_be_inserted)))

        if len(issues_to_be_inserted) > 0:

            issue_details_to_be_inserted = []
            issue_business_value_to_be_inserted = []
            for issue in issues_to_be_inserted:
                logger.info("Following will be inserted  --  : " + str([project[1], str(issue)]))
                issue_details_to_be_inserted.append([str(project[0]), project[1],project[2].replace("'","''").replace("$","$$"),str(issue[0]),str(issue[1]),str(""),str(issue[3])])
                for business_value in issue[2]:
                    issue_business_value_to_be_inserted.append([str(issue[0]),str(business_value)])

            #Insert in the batchs of 2000 records , as teradata py does not allow more than 2MB data in one batch
            logger.info("About to insert data in Issues Master ..........................")
            issue_batch = 0
            while (issue_batch < len(issue_details_to_be_inserted)):
                with session.cursor() as newcursor:
                        newcursor.executemany(
                            """INSERT	INTO AMO.ISSUES_MASTER (PROJECT_ID, PROJECT_KEY, PROJECT_NAME,ISSUE_KEY,ISSUE_TYPE,BUSINESS_VALUE,CATEGORY,CREATED_DT)
                            VALUES (?,?,?,?,?,?,?,current_timestamp);""",issue_details_to_be_inserted[issue_batch:issue_batch+2000],batch=True)
                issue_batch = issue_batch+2000
            logger.info("Insertion completed in Issues Master ..........................")

            issue_batch = 0
            while (issue_batch < len(issue_business_value_to_be_inserted)):
                with session.cursor() as newcursor:
                    newcursor.executemany(
                        """INSERT	INTO AMO.ISSUES_BUSINESS_VALUE (ISSUE_KEY,BUSINESS_VALUE)
                        VALUES (?,?);""",
                        issue_business_value_to_be_inserted[issue_batch:issue_batch + 2000], batch=True)
                issue_batch = issue_batch + 2000

            logger.info("Insertion completed in ISSUES_BUSINESS_VALUE ..........................")

def cleanAllprojectsOfJIRA(session,token):
    import json
    import http.client

    for project_key in session.execute("SELECT DISTINCT PROJECT_KEY from AMO.PROJECTS_MASTER WHERE DELETED = 'N'; "):
        project_key_from_db = str(project_key[0])
        logger.info("Checking the project : " + project_key_from_db)


        #retries = 0
        #while retries < 10:
        for retries in range(1,21):
             #retries = retries + 1
             try:
                 conn = http.client.HTTPSConnection("sonypictures.atlassian.net")
                 headers = {
                     'authorization': token,
                     'cache-control': "no-cache"
                 }
                 conn.request("GET", "/rest/api/2/project/" + project_key_from_db, headers=headers)
                 res = conn.getresponse()
             except Exception as exp:
                 logger.exception("Retrying ( " + str(retries) + " ) after exception : ")
                 time.sleep(5)
                 continue
             break

        data = res.read()
        jsonstr = data.decode("utf-8")
        jsondata = json.loads(jsonstr)
        try :
            project_key_jira = str(jsondata['key'])

            if project_key_from_db != project_key_jira:
                with session.cursor() as newcursor:
                    moveproject(newcursor,project_key_from_db,project_key_jira)
        except Exception as exp:
            with session.cursor() as sessiontodelete:
                softdeleteproject(sessiontodelete,project_key_from_db)


with open('AllJiraProjectAndIssues.log', 'w'):
    pass
# logging.basicConfig(filename='AllJiraProjectAndIssues.log',level=logging.DEBUG,
#                     format= '%(filename)s:##:%(funcName)s:##:%(asctime)s:##:%(levelname)s:##:%(message)s')
# logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(filename)s:##:%(funcName)s:##:%(asctime)s:##:%(levelname)s:##:%(message)s')
file_handler = logging.FileHandler('AllJiraProjectAndIssues.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

#print("Script Starts :", str(dt.datetime.now()))
logger.info("Script Starts")

config = configparser.ConfigParser()
config.read('Jira.ini')
token = config['DEFAULT']['authorization']
LastNthIssuesToBeScanned = int(config['DEFAULT']['LastNthIssuesToBeScanned'])

overalllist=[]

udaExec = teradata.UdaExec(logRetention=90)#,logLevel='WARNING'
with udaExec.connect("${dataSourceName}") as session:
#with udaExec.connect(method="odbc",system=sys.argv[1],username=sys.argv[2], password=base64.b64decode(sys.argv[3]).decode('utf-8')) as session:
    #print("Teradata Connection establisted :", str(dt.datetime.now()))
    logger.info("Teradata Connection establisted")
    for url in (config['DEFAULT']['Urls']).split(','):
        #print("Data Fetch Starts for ", url + " at :" + str(dt.datetime.now()))
        logger.info("Data Fetch Starts for "+str(url))
        try:
            #print("Start inserting Projects")
            logger.info("Start inserting Projects")
            getAllprojectsOfJIRA(session,token)

            logger.info("Start updating business logic")
            updateBusinesslogic(session)
            #logger.info("Start cleaning Projects")
            #cleanAllprojectsOfJIRA(session,token)
        #except: "Problem loading the projects"
        except Exception as exp:
            logger.exception("Problem loading the projects")
        #try:
        #print("Start inserting issues")
        logger.info("Start inserting issues")
        getAllIssuesOfJIRAProject(session,LastNthIssuesToBeScanned,token)
        #except Exception as exp:
        #        print(exp)
        #        print("Problem loading the issues")

session.close()
#print("Script Ends", str(dt.datetime.now()))
logger.info("Script Ends")
