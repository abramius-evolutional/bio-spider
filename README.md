# bio-spider

This example of application which extracts publications and additional information from the site http://bioline.org.br/

Some information (full text) is in PDF format. This part is converted to text format.

#### Frameworks

Scrapy (https://scrapy.org/) for parsing and data extraction.
PyPDF2 (https://pythonhosted.org/PyPDF2/) for converting PDF documents to text format.

#### Environment

This application is wrapped into a docker container, which lets develop and deploy in the same environment.

#### Deployment (Linux)

Install Docker and Docker-compose.

Then, in the directory, which contains docker-compose.yml file:

    $ sudo docker-compose up -d
  
and you can see log this way:
  
    $ sudo docker-compose logs -f

#### Data interface

The parsed url is 

    http://bioline.org.br/titles?id=md&year=2016&vol=19&num=01&keys=V19N1

The application work result is in the file /spider/data/result.json

And the logs of updating events is in the file /spider/data/log.txt

The item of the parsing result is the json serialized string with the format:

    {
      "journal_name": <...>,
      "journal_issn": <...>,
      "title": <title of the article>,
      "author": <authors of the article>,
      "abstract": <...>,
      "full_text": <full article from the PDF file>
    }

Updating the information goes every ten minutes by the cron job

In the file log.txt you can see updating logs in this format:

    [2016-10-26 22:40:05.080844] updating (http://bioline.org.br/titles?id=md&year=2016&vol=19&num=01&keys=V19N1)
    [2016-10-26 22:50:05.071425] updating (http://bioline.org.br/titles?id=md&year=2016&vol=19&num=01&keys=V19N1)
