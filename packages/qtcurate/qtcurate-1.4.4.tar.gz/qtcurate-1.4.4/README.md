# Qtcurate-SDK-Python
Python SDK for Search and Data extraction

## Overview and Definitions
**Theia** is a semantic data extraction tool that can read PDF, HTML, Ms Excel, CSV and plain text documents and extract
 information in structured format using dictionaries. It is essential to understand the utility of dictionaries in 
 extraction context:
 
 ### Dictionary

In the simplest case, a dictionary is a list of phrases. Theia searches for every phrase in the dictionary in the input documents and based on the _extraction type_ decides to extract data. 
At a minimum, a dictionary must have a Name and at least one entry, one search phrase.
Users can also assign categories to dictionary entries. 

Searching for dictionary phrases in the content is based on the techniques used in modern full-text search engines. Users can use various text analyzers, synonyms, stop words and fuzziness.


### Extraction Types

Each dictionary can have one optional extraction type:

1. **Number**: Search for the phrases AND a number in proximity to the found phrases.
2. **Date**: Search for the phrases AND a date in proximity to the found phrases.
3. **Regex**: Search for the phrases AND a custom regular expression in proximity to the found phrases.

Without setting an extraction type the dictionary will essentially be used for tagging documentnts.

Search phrases and types should appear in reading order, either in a sentence or in a table. By default **Theia** expects the phrase and the type to appear close (but not necessarily next) to each other. Users can configure the allowable gap between dictionary phrases and types using regular expressions.


### Examples

| Input | Dictionary Phrase List | Extraction Type | Output |
|-------|------------|-----------------|--------|
|Revenue was $201.5 million , an increase of 36% year-over-year.| revenue | Number | `201,500,000`|
| <table><tr><td>Activity Date</td><td>Due Date</td><td>Amount</td></tr><tr><td>July 25, 2019</td><td>October 23, 2010</td><td>$117,000</td></tr> </table>| Activity Date | Date | `07/25/2019`|
|Fuel Consumption:  18.1 L/100km| Consumption | Regex ([\d\\.]+) .*?100km| `18.1`|
Gas Consumption is 23.1 L per 100km| Consumption | Regex ([\d\\.]+) .*?100km| `23.1`|
The car consumes 24 litre of gas per 100km| Consumption | Regex ([\d\\.]+) .*?100km| `24`|


In the following we will cover the details of configuring and submitting extraction jobs via our REST API. Extensive end-to-end examples can be found in our Java and Python SDK repositories.



## Table of content

- [Installation](#installation)
- [Authentication](#authentication)
- [Data Dictionaries](#data-dictionaries)
  - [Create a New QtDictionary](#create-a-new-qtdictionary)
  - [Upload a TSV Dictionary File](#upload-a-tsv-dictionary-file)
  - [Update an Existing Dictionary](#update-an-existing-dictionary)
  - [Delete a Dictionary](#delete-a-dictionary)
  - [List Available Dictionaries](#list-available-dictionaries)
  - [Fetch dictionary](#fetch-dictionary)
- [Data Extraction](#data-extraction)
  - [Processing Files](#processing-files)
  - [Processing Web URLs](#processing-web-urls)
  - [Processing Data Streams](#mining-data-streams)
  - [Extracting Typed Entities](#extracting-typed-entities)
  - [Status Monitoring](#status-monitoring)
- [Searching in the Results](#searching-in-the-results)
- [Exporting the Results](#exporting-the-results)
  - [Exporting in Excel Format](#exporting-in-excel-format)
  - [Exporting in JSON](#exporting-in-json)
- [Clear temporary data](#clear-temporary-data)


### Installation

You can install it with pip. You have to have Python 3.5 or above
```
pip install qtcurate
```

### Authentication

Valid API key is required for all operations.

If API key is valid, than the response will be `HTTP 200` containing user profile data.

If API key is missing or not valid, the endpoint will return `HTTP 401`


### Data Dictionaries
Dictionaries are a list of phrases used for searching in input documents. Each entry of a dictionary has a `str` and an 
optional `category`.  Once a phrase is found **Theia** produces an extraction object:Dictionaries are a list of phrases 
used for searching in input documents. Each entry of a dictionary has a `str` and an optional `category`.  Once a phrase
 is found **Theia** produces an extraction object:

Authentication with API KEY
```
dic = QtDict(api_key=YOUR-API-KEY)
```
Dictionaries are a list of phrases used for searching in input documents. Each entry of a dictionary has a `str` and an optional `category`.  Once a phrase is found **Theia** produces an extraction object:

```json
{
	"start": 6188,
	"end": 6196,
	"str": "sales of equipment",
	"line": 309,
	"category": "Sales",
	"dict_name": "Revenue",
	"dict_id": "92e7e423-304a-421c-a612-b6dc4215fd09"
}
```
`str` is the found phrase.
`start`, `end` and `line` are the positions of the found phrase.
`category` (optional) and is only produced if the found phrase was associated with a category.
`dict_name` assigned by user when creating a dictionary
`dict_id` returned by **Theia** once a dictionary is created.


**Theia** uses various strategies for matching on dictionary phrases allowing users to configure the fuzziness of search. User can also provide a list synonyms and stop phrases for the value matching. For example, user can only have "Apple Inc" as one phrase in the dictionary and provide "inc", "corp", "corporation" and "company" as synonyms, allowing you to find all occurrences of "Apple the Company", "Apple Corporations" and "Apple Corp" in the content.


Dictionaries can be created in two ways: 
- By providing dictionary entries in the request payload
- By uploading a TSV file
#### Create a New QtDictionary

Create data dictionaries with create() function
First we prepare data
Name is required.
```
dic.name("Name of QtDict)
```
Two ways to create entries
```
qt_str = "some str"
category = "some category"
dic.add_entry(str, category)
```
or
```
tmp_dictionary = {"str": "some key", "category": "some value"}
dic.entries(tmp_dictionary)
```
where method entries take a Python dictionary with 2 elements where KEYS have string value "str" and "category"
After that we can create our QtDict
```
dic.create()
```
#### Return

```
{
  "id": "58608b1f-a0ff-45d0-b12a-2fb93af1a9ad",
  "name": "Name of dictionary",
  "global": false,
  "entries": [
  {
     "str": "some str",
     "category": "some category"
  }
  ]
}
```

#### Upload a TSV Dictionary File

Upload TSV data dictionaries with upload function:
```
dic.upload("file-path.tsv", "Name of dictionary")
```
TSV is required file format. Return is the same as create function Return.

#### Update an Existing QtDict

To update an existing QtDict:
```
dic.update(ID)
```
We use ID as argument of function.

#### Delete a QtDict

To delete an existing QtDict:
```
dic.delete(ID)
```
We use ID as argument of function.

#### List Available Dictionaries:

To list all of your existing dictionaries:
```
dic.list()
```
Return is a list of dictionaries
```
[
{
"id": "58608b1f-a0ff-45d0-b12a-2fb93af1a9ad",
"key": "user-example-com/58608b1f-a0ff-45d0-b12a-2fb93af1a9ad.csv.gz",
"name": "My dictionary",
"global": false,
"entries": []
}
{
...
}
]
```

#### Fetch QtDict:
To fetch data from the QtDict
```
dic.fetch(ID)
```
We use ID as argument of function.

Return
```
{
"id": "58608b1f-a0ff-45d0-b12a-2fb93af1a9ad",
"key": "user-example-com/58608b1f-a0ff-45d0-b12a-2fb93af1a9ad.csv.gz",
"name": "My dictionary",
"global": false,
"entries": []
}
```

### Data Extraction

Data Extraction is the process of identifying search phrases found in the input documents along with extraction types 
(date, number or regex) and producing structured data. Input documents can be streamed from content files, data APIs or 
directly from public URLs.

Authenticate with API_KEY

```
dp = DataProcess(api_key="1234")
```

#### Processing Files

First, upload all content files for DataProcess:
```
dp.upload("file.pdf")
```

PDF, TXT, XLS, XLSX, CSV and HTML formats are supported. Image documents, such as TIFF, PNG or scanned PDF, 
will automatically run through OCR before data extraction.

#### Return

```
{
"uuid": "c351283c-330c-418b-8fb7-44cf3c7a09d5",
"fileName": "file.pdf",
"link": "http://portal.document.quantxt.amazonaws.com/user@example.com/c351283c-330c-418b-8fb7-44cf3c7a09d5",
"date": "2019-10-25T20:14:41.925+02:00",
"contentType": "application/pdf",
"source": "file.pdf"
}
```
`uuid`s along with dictionaries are provided for the exraction engine.

Now you can mine data via dictionaries. First you have to prepare additional options.
`vocabId` (required) id of the dictionary.
`title` is optional but it is highly recommended for easier distinction between different tagging jobs.

`vocabValueType` (Optional): can have one of the following values: `NUMBER`, `DATETIME`, `REGEX`. If no extraction type 
is set, the dictionary will be used for tagging documents. If set, the engine will extract only entities that are 
associated with an entity of this type. 

If `REGEX` is set user will also need to provide the look up regular expression 
via `phraseMatchingPattern`. The following pattern matches on social securities numbers:

```
dp.files(uuid)
dp.title("My data mining with files and dictionaries")
dp.search_rule("758345h-a0ff-45d0-b12a-2fb93af1a9ad", vocab_value_type_input=DictionaryType.REGEX, 
                phrase_matching_pattern="(\d{3}-\d{2}-\d{4})")

dp.create()
```
#### Return

```
{
    "id": "puvqrjfhqq",
    "title": "My data mining with files and dictionaries",
    "excludeUttWithoutEntities": true,
    "files": ["c351283c-330c-418b-8fb7-44cf3c7a09d5"],
    "searchDictionaries": [
        { 
            "vocabId": "58608b1f-a0ff-45d0-b12a-2fb93af1a9ad",
            "vocabValueType": "NUMBER"
        }
    ]
}
```

`id` is the extraction job id. You can use it to monitor status of the job or retrieve the results once completed.
You can set `sortByPosition`, `excludeUttWithoutEntities`, `stitle`, `sources`, `query` with following methods:
```
dp.sort_by_position(True)
dp.exclude_utt_without_entities(True)
dp.stitle("some stitle string")
dp.sources("id of source files")
dp.query("some query string")
```


**Function parameters:**

`chunk`
(Optional, string) can be `SENTENCE` or `PAGE` or `NONE`. This will result in splitting of data into semantic chunks 
before processing. For example, this allows user to split the content of an article in semantic sentences and apply 
entity dictionaries at sentence level.

`excludeUttWithoutEntities`
(Optional, boolean) if `true` the output will only include chunks that have at least one label from the input 
dictionaries.

`stitle` (Optional, string) Override command.

`query` (Optional, string) Set query for source.

To delete a data container:
```
dp.delete("puvqrjfhqq")
```

#### Processing Web URLs:

Processing can be performed on a list of URLs. All parameters in processing files are applicable here.
```
dp.search_rule("758345h-a0ff-45d0-b12a-2fb93af1a9ad")
dp.urls(["url1", "url2"])
dp.create()
```

**Theia can process both static and dynamic web pages. However, a number of websites use mechanisms to block web page 
scrapping. Theia built-in Web parser is not designed to bypass such blocking mechanisms**

#### Processing Data Streams

Extraction data from streams or third party data APIs is supported. For example, user can stream documents directly from
 Amazon S3, Google Drive, DropBox and many other document repositories that are available via an API. Please contact 
 <support@quantxt.com> for details.
 
 #### Re-Use Data Processing Pipelines

A project is essentially a collection of data dictionaries along with extraction parameters. Once a project is 
completed, user can re-use the data processing piepline to process more documents. 
User can either append more documents to a current project or clone the project into a new project and process new
documents.

To append fresh data to an already completed project:

#### Update function

```js
dp.update(ID, list_of_files)
```
#### Return

```
{
    "index": "cjaejhvtao",
    "progress": 36,
    "progress_msg": "Collecting data..."
}
```

#### Re-Use Data Processing Pipelines

A project is essentially a collection of data dictionaries along with extraction parameters. Once a project is 
completed, user can re-use the data processing piepline to process more documents. 
User can either append more documents to a current project or clone the project into a new project and process new 
documents.

To append fresh data to an already completed project:

#### Request
```js
dp.clone(ID, list_of_files)
```
The above will use dictionaries and extraction parameters from `cjaejhvtao` project to process `uuid_1` and `uuid_2`.
 The call above will return a new `id`.
#### Status Monitoring

The progress functions allows user to check the progress of a submitted data mining job:

#### Function

```
dp.progress()
```

The search result is an array of all active data processing jobs:

```
[
{
"dp_id": "cjaejhvtao",
"progress": 36,
"progress_msg": "Collecting data..."
}
]

```

`dp_id` Unique ID of the running job

`progress`  Progress in % (a number between 0 to 100).

`progress_msg` (Optional) Progress message.


It is also possible to check the progress of a specific data mining job:

#### Function

```
dp.progress("cjaejhvtao")
```

#### Return

```
{
"dp_id": "cjaejhvtao",
"progress": 36,
"progress_msg": "Collecting data..."
}
```

### Searching in the Results


The search endpoint allows user to run full-text and [faceted search](https://en.wikipedia.org/wiki/Faceted_search) in the extracted data.

#### Function

```
dp.search("puvqrjfhqq", param_from, size, f1, f2)
```

**Function parameters:**

`q`
(Optional, string) Search query that filters the main content `title` field. It supports boolean `OR`, `AND` and `NOT` 
parameters.

`f`
(Optional, string) Query filters must be used in pairs. Filters are created for each input dictionary. For example, to 
include results that have one or more label from `Vehicle` dictionary the request should look like: `&f=Vehicle&f=*`. 
To include results that are labeled with `Ford` or `BMW` from the `Vehicle` dictionary, the request would be 
`&f=Vehicle&f=BMW&f=Vehicle&f=Ford`

`from`
(Optional, int) Offset for paging results. Defaults to 0. Each page contains 20 items.

`size`
(Optional, int) Number of results to return. Maximum is 200.


#### Return

```
{
"Total": 2610,
"results": [
{
"title": "The Federal Reserve Bank of New York provides gold custody to several central banks, governments and official international organizations on behalf of the Federal Reserve System.",
"id": "Wv8fBG4Bc3WI8L9MbaO2",
"link": "https://www.hamilton.edu/news/story/hamilton-nyc-program-tours-federal-reserve-museum",
"score": 0.10268514747565982,
"source": "abc15.com",
"date": "2018-05-24T00:00:00.000Z",
"tags": [
"Federal Reserve",
"New York"
]
}
],
"aggs": {
"Tag": [{
"key": "Central bank",
"count": 878
}, {
"key": "Gold",
"count": 523
}
}
}
```

`Total`: Number of results.

`result []`: The array that contains result items.

`aggs` : Facets over the results with count of items for each facet.


### Exporting the Results

Results can be exported in XLSX or JSON format:

#### Exporting in Excel Format

```
dp.report_to_xlsx("puvqrjfhqq", "name-of-output-file.xlsx")
```


#### Exporting in JSON

```
dp.report_to_json("puvqrjfhqq", "name-of-output-file.json")

```

### Clear temporary data
Both classes QtDict and DataProcess have a method `clear()` to delete all used variable.
```
dic.clear()
dp.clear()
```
The export output is limited to 5000. All `/search` parameters can be passed here to export the desired slice of the data.


For technical questions please contact <support@quantxt.com>
