#Junior Web App
This is the primary repository for Project Return's Junior web application. Beware - changes here will propagate directly to the application on Azure.

###About Junior
*Junior* is a Google Sheets spreadsheet used by the Project Return organization to catalog open job opportunities, match them to qualified participants, and track the placement process. Extensive business processes with multiple participants revolve around this spreadsheet.

###About the Junior Web Application
At the 2016 [Hack for the Community](http://hackforthecommunity.com/) event, representatives from Project Return worked with a team of technologists to analyze pain points in their usage of the Junior spreadsheet and brainstorm potential improvements. Given the spreadsheet's wide and complex usage and the Hack event's limited time window, it quickly became apparent that replacing or revamping the core tool was not feasible. However, a valuable option would be to layer some application functionality atop the spreadsheet to streamline one particularly arduous process - **matching a participant to appropriate opportunities**. The team agreed to focus here, and this repository represents the fruit of that effort.

This document describes the following major components of this web app:

1. [Spreadsheet](#spreadsheet)
2. [UI Layer](#ui-layer)
3. [API/Service Layer](#apiservice-layer)
4. [Hosting](#hosting)

## Spreadsheet
The Junior spreadsheet contains a tab named "Job Opportunities", which lists the current opportunities available to qualifying participants.

### Significant Columns
Several columns in the "Job Opportunities" tab are of specific importance to this web app, namely:

* "Company Name": The name of the employer offering the opportunity (and possibly the job title). (Text)
* "Conviction Restrictions": A column group (merged header cell over several columns); each column has a sub-header naming a conviction that may or may not prevent a participant from qualifying for the given job. (TRUE/FALSE)
* "Conviction Threshold (Yrs)": The number of years after which the Conviction Restrictions no longer apply to the given job. (Number)
* "Part Time / Full Time": The work schedule for the opportunity. If the cell includes "PT", the given job will be treated as having a part-time option available. (Text, possibly containing 'PT')
* "Industry": The name of the industry the employer operates in. (Text)
* "Type": Distinguishes various placement arrangements between Project Return and the employer. (Text)
* "Required Abilities": A column group (merged header cell over several columns); each column has a sub-header naming some ability that may or may not be required for work in the given job. (TRUE/FALSE)
* "Requires Driver's License": Whether a participant must have a license in order to qualify for the given job. (TRUE/FALSE)

## UI Layer
This is a client-side Single-Page Web application built in HTML/JS/CSS, using the [Vue framework](https://vuejs.org/). The source code for this layer is maintained in this repository's sibling named "[project-return-client](https://github.com/h4c-project-return/project-return-client)". The build output from that codebase is then checked into this repository at the following path for inclusion in the Azure deployment: [/junior_web/static](https://github.com/h4c-project-return/junior-web-azure/tree/master/junior_web/static)
  
Detailed documentation on working within and building the UI Layer's codebase are pending.

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
