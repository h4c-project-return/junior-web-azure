#Junior Web App
This is the primary repository for Project Return's Junior web application. Beware - changes here will propagate directly to the application on Azure.

###About Junior
*Junior* is a Google Sheets spreadsheet used by the Project Return organization to catalog open job opportunities, match them to qualified participants, and track the placement process. Extensive business processes with multiple participants revolve around this spreadsheet.

###About the Junior Web Application
At the 2016 [Hack for the Community](http://hackforthecommunity.com/) event, representatives from Project Return worked with a team of technologists to analyze pain points in their usage of the Junior spreadsheet and brainstorm potential improvements. Given the spreadsheet's wide and complex usage and the Hack event's limited time window, it quickly became apparent that replacing or revamping the core tool was not feasible. However, a valuable option would be to layer some application functionality atop the spreadsheet to streamline one particularly arduous process - **matching a participant to appropriate opportunities**. The team agreed to focus here, and this repository represents the fruit of that effort.

This document describes the following major components of this web app:

1. Spreadsheet (in brief - above)
2. UI Layer
3. API/Service Layer
4. Hosting

## UI Layer


## API/Service Layer


## Hosting
The Junior web application is currently hosted on Azure, using nonprofit grant credits donated by Microsoft in conjunction with the Hack for the Community event. Azure offers several advantages over other options considered, including:
* PaaS (no VM management required)
* Free subdomain (no DNS maintenance required)
* Automated deployment upon GitHub commit

However, it should be noted that Python support on Azure still seems somewhat immature. The base hosting setup in use at time of writing was derived from the [PTVS team's Flask hosting instructions](https://docs.microsoft.com/en-us/azure/app-service-web/web-sites-python-create-deploy-flask-app) and [artifacts](https://github.com/azureappserviceoss/FlaskAzure). This appears to be a work in process, with improvements and alternatives being discussed regularly on various blog posts.

### Deployment
Notiwthstand the above, setting up Azure to host this application is fairly straightforward:

1. Create new App Service.
   * Search for and select the "Flask" option from PTVS.
   * Place the App Service on a "Standard: 1 Small" Service plan. (Basic didn't seem to work, though I'm not sure why.)
2. Attach the new App Service to this GitHub repository.
   * Under Deployment Options, Disconnect the pre-built option.
   * Connect to GitHub to automatically pull code committed here.
3. Configure the application. 
Under Application Settings, configure the following name-value-pair App Settings:
   * `FLASK_SECRET_KEY`: A unique, unguessable string used to encrypt users' session cookies (e.g., a [GUID](https://www.guidgenerator.com/))
   * `GOOGLE_OAUTH_CLIENT_ID`: Client Id from Google Apps OAuth configuration
   * `GOOGLE_OAUTH_CLIENT_SECRET`: Client Secret from Google Apps OAuth configuration
   * `GOOGLE_SHEET_ID`: Sheet Id from Google Sheets
   * `GOOGLE_SHEET_RANGE_NAME`: The name of the Job Opportunities spreadsheet tab
