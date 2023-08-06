from qtcurate.config import BASE_URL
from time import sleep
import requests
import re
import json
from typing import Dict, List
import os.path
from qtcurate.exceptions import QtFileTypeError, QtArgumentError, QtConnectionError, QtRestApiError, QtDataProcessError
from qtcurate.data_types import SearchMode, DictionaryType, AnalyzeMode


tag_files = "files"
tag_urls = "urls"
tag_title = "title"
tag_stitle = "stitle"
vocab_id = "vocabId"
vocab_value_type = "vocabValueType"
tag_exclude_utt = "excludeUttWithoutEntities"
tag_search_dict = "searchDictionaries"
tag_sort_by_position = "sortByPosition"
phrase_matching_pattern = "phraseMatchingPattern"
between_key_and_value = "skipPatternBetweenKeyAndValue"
between_values = "skipPatternBetweenValues"
search_mod = "searchMode"
analyze_mod = "analyzeMode"
stop_word_list = "stopwordList"
synonym_l = "synonymList"
tag_query = "query"
tag_sources = "source"


class DataProcess:
    def __init__(self, api_key: str, environment: str = ""):
        self.session = requests.Session()
        self.headers = {"X-API-Key": api_key}
        self.temp_dict = dict()
        self.temp_dict[tag_exclude_utt] = True
        self.temp_dict[tag_sort_by_position] = False
        self.temp_dict[tag_search_dict] = []
        self.index = None
        if environment != "":
            environment = f"{environment}."
        self.url = f"http://{environment}{BASE_URL}"

    def connect(self, method: str, uri: str, data: Dict = None) -> Dict:
        if method.lower() == 'get':
            try:
                res = self.session.get(uri, headers=self.headers)

            except requests.exceptions.RequestException as e:
                raise QtConnectionError(f"Connection error: {e}")
            if res.status_code not in [200, 201, 202]:
                raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                     f"HTTP status code: {res.status_code}. Server message: {res.json()}")
        elif method.lower() == "delete":
            try:
                res = self.session.delete(uri, headers=self.headers)
            except requests.exceptions.RequestException as e:
                raise QtConnectionError(f"Connection error: {e}")
            if res.status_code not in [200, 201, 202]:
                raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                     f"HTTP status code: {res.status_code}. Server message: {res.json()}")
        elif method.lower() == "post":
            try:
                res = self.session.post(uri, headers=self.headers, data=json.dumps(data))
            except requests.exceptions.RequestException as e:
                raise QtConnectionError(f"Connection error: {e}")
            if res.status_code not in [200, 201, 202]:
                raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                     f"HTTP status code: {res.status_code}. Server message: {res.json()}")
        elif method.lower() == "put":
            try:
                res = self.session.put(uri, headers=self.headers, data=json.dumps(data))
            except requests.exceptions.RequestException as e:
                raise QtConnectionError(f"Connection error: {e}")
            if res.status_code not in [200, 201, 202]:
                raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                     f"HTTP status code: {res.status_code}. Server message: {res.json()}")

        return res

    def __repr__(self):
        return f"{self.temp_dict}"

    def get_id(self):
        return self.index

    def title(self, title_name: str) -> None:
        """Create title for mining data"""

        if isinstance(title_name, str):
            self.temp_dict[tag_title] = title_name
        else:
            raise QtArgumentError("Argument type error: String is expected as title")

    def query(self, value: str) -> None:
        """Create query for mining data"""

        if isinstance(value, str):
            self.temp_dict[tag_query] = value
        else:
            raise QtArgumentError("Argument type error: String is expected as query")

    def stitle(self, value: str) -> None:
        """Create title for mining data"""

        if isinstance(value, str):
            self.temp_dict[tag_stitle] = value
        else:
            raise QtArgumentError("Argument type error: String is expected as title")

    def sort_by_position(self, value: bool) -> None:
        """Set sortByPosition for mining data, this is optional parameter"""

        if isinstance(value, bool):
            self.temp_dict[tag_sort_by_position] = value
        else:
            raise QtArgumentError("Argument type error: Boolean is expected as sortByPosition")

    def exclude_utt_without_entities(self, value: bool) -> None:
        """Set exclude utt for mining data, this is optional parameter"""

        if isinstance(value, bool):
            self.temp_dict[tag_exclude_utt] = value
        else:
            raise QtArgumentError("Argument type error: Boolean is expected as exclude utt without entities")

    def files(self, list_of_files: list) -> None:
        """Create a list of existing files"""

        if isinstance(list_of_files, list):
            self.temp_dict[tag_files] = list_of_files
        else:
            raise QtArgumentError("Argument type error: Expected list of file IDs")

    def sources(self, list_of_files: list) -> None:
        """Create a list of existing files"""

        if isinstance(list_of_files, list):
            self.temp_dict[tag_sources] = list_of_files
        else:
            raise QtArgumentError("Argument type error: Expected list of file IDs")

    def urls(self, list_of_urls: list) -> None:
        """Create a list of existing files"""

        if isinstance(list_of_urls, list):
            self.temp_dict[tag_urls] = list_of_urls
        else:
            raise QtArgumentError("Argument type error: Expected list of urls")

    def search_rule(self, vocab_id_input: str,
                    vocab_value_type_input: DictionaryType = None,
                    skip_pattern_between_key_and_value: str = None,
                    skip_pattern_between_values: str = None,
                    re_phrase_matching_pattern: str = None,
                    stopword_list: str = None,
                    synonim_list: str = None,
                    search_mode: SearchMode = None,
                    analyze_mode: AnalyzeMode = None
                    ) -> None:
        """Prepare dictionary for searching"""

        vocab_dict = dict()
        if isinstance(vocab_id_input, str):
            vocab_dict[vocab_id] = vocab_id_input
        else:
            raise QtArgumentError("Argument type error: String is expected as dictionary_path id")

        if vocab_value_type_input is not None:
            if isinstance(vocab_value_type_input, DictionaryType):
                vocab_dict[vocab_value_type] = vocab_value_type_input.value
            else:
                raise QtArgumentError("Argument type error: DictionaryType object is expected as vocab_value_type")

            if vocab_value_type_input.value == "REGEX":
                if re_phrase_matching_pattern is not None:
                    if isinstance(re_phrase_matching_pattern, str):
                        try:
                            re.compile(re_phrase_matching_pattern)
                            valid = True
                        except re.error:
                            valid = False
                        if valid is False:
                            raise QtArgumentError("Argument type error: Please write valid regular expression.")
                        else:
                            vocab_dict[re_phrase_matching_pattern] = re_phrase_matching_pattern
                    else:
                        raise QtArgumentError(
                            "Argument type error: String is expected as re_phrase_matching_pattern")
                else:
                    raise QtArgumentError("Argument type error: If you use regex you have to add "
                                          "phrase_matching_pattern")

        if skip_pattern_between_key_and_value is not None:
            if isinstance(skip_pattern_between_key_and_value, str):
                vocab_dict[between_key_and_value] = skip_pattern_between_key_and_value
            else:
                raise QtArgumentError("Argument type error: String is expected as skip_pattern_between_key_and_value")

        if skip_pattern_between_values is not None:
            if isinstance(skip_pattern_between_values, str):
                vocab_dict[between_values] = skip_pattern_between_values
            else:
                raise QtArgumentError("Argument type error: String is expected as skip_pattern_between_values")

        if stopword_list is not None:
            if isinstance(stopword_list, str):
                vocab_dict[stop_word_list] = stopword_list
            else:
                raise QtArgumentError("Argument type error: String is expected as stopword_list")

        if synonim_list is not None:
            if isinstance(synonim_list, str):
                vocab_dict[synonym_l] = synonim_list
            else:
                raise QtArgumentError("Argument type error: String is expected as synonim_list")

        if search_mode is not None:
            if isinstance(search_mode, SearchMode):
                vocab_dict[search_mod] = search_mode.value
            else:
                raise QtArgumentError("Argument type error: SearchMode object is expected as search_mode")

        if analyze_mode is not None:
            if isinstance(analyze_mode, AnalyzeMode):
                vocab_dict[analyze_mod] = analyze_mode.value
            else:
                raise QtArgumentError("Argument type error: AnalyzeMode object is expected as analyze_mode")

        self.temp_dict[tag_search_dict].append(vocab_dict)

    def clear(self) -> None:
        """Remove all temporary data"""
        self.temp_dict.pop(tag_files, None)
        self.temp_dict.pop(tag_urls, None)
        self.temp_dict.pop(tag_title, None)
        self.temp_dict[tag_exclude_utt] = True
        self.temp_dict.pop(tag_search_dict, None)
        self.index = None

    def upload(self, file: str) -> Dict:
        """Upload files for data mining"""

        if not isinstance(file, str):
            raise QtArgumentError("Argument type error: String is expected as file path")

        extension = os.path.splitext(file)[1].lower()
        if extension not in [".pdf", ".txt", ".html", ".xls", ".xlsx", ".csv", ".tiff", ".png"]:
            raise QtArgumentError("Argument type error: PDF, TXT, XLS, XLSX, CSV, TIFF, PNG or HTML file expected")
        if not os.path.exists(file):
            raise QtArgumentError(f"Argument error: File {file} does not exist")
        files = {'file': open(file, 'rb')}

        res = self.connect("post", f"{self.url}search/file", files)
        self.index = res.json()['index']
        return res.json()

    def create(self) -> Dict:
        """Mine data via dictionaries"""

        self.headers["Content-Type"] = "application/json"
        correct = 0
        if len(self.temp_dict[tag_search_dict]) == 0:
            raise QtDataProcessError("DataProcess error: Please add parameters using search_rule function")
        if tag_files in self.temp_dict and len(self.temp_dict[tag_files]) > 0:
            data = {tag_files: self.temp_dict[tag_files]}
            correct += 1
        if tag_urls in self.temp_dict and len(self.temp_dict[tag_urls]) > 0:
            data = {tag_urls: self.temp_dict[tag_urls]}
            correct += 1
        if tag_sources in self.temp_dict and len(self.temp_dict[tag_sources]) > 0:
            if len(self.temp_dict[tag_query]) > 0:
                data = {tag_sources: self.temp_dict[tag_sources], tag_query: self.temp_dict[tag_query]}
            else:
                raise QtDataProcessError("DataProcess error: Query is requested parameter for sources")
            correct += 1

        if correct != 1:
            raise QtDataProcessError("DataProcess error: You must choose one kind of data: files, URLs or source")
        data[tag_exclude_utt] = self.temp_dict[tag_exclude_utt]
        if len(self.temp_dict[tag_search_dict]) != 0:
            data[tag_search_dict] = self.temp_dict[tag_search_dict]
        if tag_title in self.temp_dict:
            data[tag_title] = self.temp_dict[tag_title]
        res = self.connect("post", f"{self.url}search/new", data)
        self.index = res.json()['index']
        del self.headers['Content-Type']

        return res.json()

    def fetch(self, dp_id: str) -> Dict:
        """ Fetch dataprocess where dp_id is existing ID"""

        self.headers["Content-Type"] = "application/json"
        if not isinstance(dp_id, str):
            raise QtArgumentError("Argument type error: String is expected as dp_id")
        res = self.connect("get", f"{self.url}search/{dp_id}")
        del self.headers['Content-Type']

        return res.json()

    def update(self, dp_id: str, update_files: List) -> Dict:
        """ Update dataprocess where dp_id is existing ID"""

        self.headers["Content-Type"] = "application/json"
        if not isinstance(dp_id, str):
            raise QtArgumentError("Argument type error: String is expected as dp_id")
        if not isinstance(update_files, List):
            raise QtArgumentError("Argument type error: List is expected as update file")
        else:
            self.clear()
            data = {tag_files: update_files}
        res = self.connect("post", f"{self.url}search/update/{dp_id}", data)
        del self.headers['Content-Type']


        return res.json()

    def clone(self, dp_id: str, update_files: List) -> Dict:
        """ Update dataprocess where dp_id is existing ID"""

        self.headers["Content-Type"] = "application/json"
        if not isinstance(dp_id, str):
            raise QtArgumentError("Argument type error: String is expected as dp_id")
        if not isinstance(update_files, List):
            raise QtArgumentError("Argument type error: List is expected as update file")
        else:
            self.clear()
            data = {tag_files: update_files}
        res = self.connect("post", f"{self.url}search/new/{dp_id}", data)

        self.index = res.json()['index']
        del self.headers['Content-Type']

        return res.json()

    def delete(self, dp_id: str) -> bool:
        """Delete data container"""

        if not isinstance(dp_id, str):
            raise QtArgumentError("Argument type error: String is expected as dp_id")
        res = self.connect("delete", f"{self.url}search/{dp_id}")

        return res.ok

    def progress(self, dp_id: str = None) -> Dict:
        """Show progress for submitted data mining job"""

        url_path = "progress"
        if dp_id is not None:
            if isinstance(dp_id, str):
                url_path = f"{url_path}/{dp_id}"
            else:
                raise QtArgumentError("Expected string")
        res = self.connect("get", f"{self.url}search/{url_path}")

        return res.json()

    def wait_for_completion(self):
        percentage = 0
        while percentage < 100:
            result = self.progress(self.index)
            percentage = result['progress']
            print(f"Search progress {percentage}%")
            if percentage < 100:
                sleep(1)
        sleep(3)

    def search(self, dp_id: str, param_from: int = 0, size: int = None, f1: int = None, f2: int = None) -> Dict:
        """Search full-text and faceted search"""

        if not isinstance(dp_id, str):
            raise QtArgumentError("Argument type error: String is expected as dp_id")
        if isinstance(param_from, int):
            parameters = [('from', param_from)]
        else:
            raise QtArgumentError("Argument type error: Integer is expected as parameter")
        if size is not None:
            if isinstance(size, int) and 0 < size <= 200:
                parameters.append(('size', size))
            else:
                raise QtArgumentError("Argument type error: Integer between 0 and 200 is expected as parameter")
        if f1 is not None and f2 is not None:
            parameters.append(('f', f1))
            parameters.append(('f', f2))
        elif f1 is None and f2 is None:
            pass
        else:
            raise QtArgumentError("Argument error: Query filters must be used in pairs")
        try:
            res = self.session.get(f"{self.url}search/{dp_id}", headers=self.headers, params=parameters)
        except requests.exceptions.RequestException as e:
            raise QtConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202]:
            raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}. Server message: {res.json()}")
        return res.json()

    def report_to_xlsx(self, dp_id: str, path: str) -> bool:
        """Exporting in Excel format"""

        if not isinstance(dp_id, str):
            raise QtArgumentError("Argument type error: String is expected as dp_id")
        if not isinstance(path, str):
            raise QtArgumentError("Argument type error: String is expected as path")
        directory = os.path.dirname(path)
        if len(directory) == 0:
            directory = "."
        if not (os.access(directory, os.W_OK) and os.access(directory, os.X_OK)):
            raise QtArgumentError("Argument error: No write permission")
        extension = os.path.splitext(path)[1].lower()
        if extension != ".xlsx":
            raise QtFileTypeError("File type error: Please use xlsx extension saving file")
        try:
            res = self.session.get(f"{self.url}reports/{dp_id}/xlsx", headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise QtConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202]:
            raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}. Server message: {res.json()}")
        with open(path, 'wb') as excel_file:
            excel_file.write(res.content)
        return res.ok

    def report_to_json(self, dp_id: str, path: str) -> bool:
        """Exporting in Excel format"""

        if not isinstance(dp_id, str):
            raise QtArgumentError("Argument type error: String is expected as dp_id")
        if not isinstance(path, str):
            raise QtArgumentError("Argument type error: String is expected as path")
        directory = os.path.dirname(path)
        if len(directory) == 0:
            directory = "."
        if not (os.access(directory, os.W_OK) and os.access(directory, os.X_OK)):
            raise QtArgumentError("Argument error: No write permission")
        extension = os.path.splitext(path)[1].lower()
        if extension != ".json":
            raise QtFileTypeError("File type error: Please use json extension saving file")
        try:
            res = self.session.get(f"{self.url}reports/{dp_id}/json", headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise QtConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202]:
            raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}. Server message: {res.json()}")
        with open(path, "w") as json_file:
            json.dump(res.json(), json_file)
        return res.ok
