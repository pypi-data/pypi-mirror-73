__author__ = "SherpDaWerp (Andrew Brown)"
__version__ = "0.1"
API_VERSION = "11"

from .nspy_wrapper_parser import *

from warnings import warn
from xml.parsers.expat import ExpatError
from urllib3 import ProxyManager, PoolManager, make_headers
from time import time, sleep


class nsRequests:
    def __init__(self, agent, delay=0, proxy_user=None, proxy_pass=None, proxy_ip=None, proxy_port=None):
        if agent == "":
            raise RuntimeError("UserAgent must be set!")

        self.userAgent = agent + ", using SherpDaWerp's nspy-wrapper tool."
        self.apiNormalDelay = 600 + delay
        self.apiTGDelay = 30000 + delay
        self.apiRecruitDelay = 180000 + delay
        self.lastRequestTime = 0

        self._auth = ["", "", ""]
        # Default authentication array. auth[0] is the password, auth[1] is the X-Autologin and auth[2] is the X-Pin

        if (proxy_user is not None) & (proxy_pass is not None) & (proxy_ip is not None) & (proxy_port is not None):
            proxy_headers = make_headers(proxy_basic_auth=proxy_user+":"+proxy_pass)
            self.request_manager = ProxyManager(proxy_ip+":"+proxy_port, headers=proxy_headers)
        else:
            self.request_manager = PoolManager()

    def auth_set(self, header):
        """ Adds the X-Autologin and the X-Pin to self.auth

        :param header: the header of the request
        :return None
        """

        try:
            xautologin = header["X-autologin"]
            xpin = header["X-pin"]

            newAuth = [self._auth[0], xautologin, xpin]

            self._auth = newAuth
        except KeyError:
            warn("Unable to find X-Pin and/or X-Autologin", MissingHeaders)

            self._auth = self._auth

    def make_request(self, url: str, headers: dict, delay: int = 600):
        """ makes the request to the API

        :param url: the url to make the request to
        :param headers: the headers to be supplied with the request
        :param delay: the delay before making the request
        :return: the response of the request
        """
        url += "&v="+API_VERSION
        
        millis = int(round(time() * 1000))
        # read the current time in milliseconds

        if millis > (self.lastRequestTime + delay):
            # if the current time is more than self.apiDelay milliseconds after the last request, make the request
            response = self.request_manager.request(method="GET", url=url, headers=headers)
            self.lastRequestTime = millis
        else:
            # if the current time is not more than self.apiDelay milliseconds after the last request, wait until it is
            time_dif = delay - (millis - self.lastRequestTime)
            # work out how much more time the program needs to wait to fulfil the apiDelay, then wait that long
            sleep(time_dif / 1000)

            # make the request, then reset lastRequestTime
            response = self.request_manager.request(method="GET", url=url, headers=headers)

            self.lastRequestTime = millis + delay

        return response

    def interpret(self, response, url):
        """ interprets the API Data as xml and headers

        :param response: the data to be interpreted
        :param url: the url of the page being accessed (used for error logging)
        :return: the content and headers from the response
        """
        resp_header = response.headers

        if response.status == 200:
            try:
                resp_dict = APIParser.data_to_dict(response.data)

                response = (resp_header, resp_dict)

                self.auth_set(resp_header)
                return response
            except ExpatError:
                warn("Malformed XML returned accessing page "+url, MalformedXML)

                resp_data = response.data
                response = (resp_header, resp_data)

                self.auth_set(resp_header)
                return response
        else:
            warn("Unsuccessful API Request: Error "+response.status, FailedRequest)

            resp_data = response.data
            response = (resp_header, resp_data)

            self.auth_set(resp_header)
            return response

    def world(self, shards: str or list, parameters: dict = None):
        """ Makes a request to the NationStates API of a World shard

        :param shards: The shards to be requested
        :param parameters: The parameters for the shards

        :return: the response data from the api
        """
        url = "https://www.nationstates.net/cgi-bin/api.cgi?"
        headers = {'User-Agent': self.userAgent}
        # sets the base URL, and sets the useragent in the headers

        if shards:
            # if shards were given
            url += "q="

            if isinstance(shards, list):
                # if shards is an array of multiple elements, then put the full list of shards in the url
                for shard in shards:
                    url += shard + "+"
                url = url[:-1]
            else:
                # if shards is not an array, or if shards has only one element, then put the single shard in the url
                url += shards

        if parameters:
            # if parameters were given
            param_list = [key+"="+parameters[key] for key in parameters]
            url += ";"
            for param in param_list:
                url += param + ";"
            url = url[:-1]

        data = self.make_request(url, headers, self.apiNormalDelay)

        response = self.interpret(data, url)
        return response

    def nation(self, nation: str, shards: str or list = None, parameters: dict = None, auth: tuple = ("", "", "")):
        """ Makes a request to the NationStates API of a Nation shard

        :param nation: The nation to be requested
        :param shards: The shards to be requested
        :param parameters: The parameters for the shards
        :param auth: optional authentication for private commands

        :return: the response data from the api
        """
        url = "https://www.nationstates.net/cgi-bin/api.cgi?nation="
        # sets the base URL

        nation_url = nation.replace(" ", "_")
        url += nation_url+"&"

        if (self._auth[0] == auth[0]) and (auth[0] != ""):
            headers = {'User-Agent': self.userAgent,
                       'X-Password': self._auth[0],
                       'X-Autologin': self._auth[1],
                       'X-Pin': self._auth[2]}
        elif auth[0] != "":
            headers = {'User-Agent': self.userAgent,
                       'X-Password': auth[0],
                       'X-Autologin': auth[1],
                       'X-Pin': auth[2]}
        else:
            headers = {'User-Agent': self.userAgent}

        if shards:
            # if shards were given
            url += "q="

            if isinstance(shards, list):
                # if shards is an array of multiple elements, then put the full list of shards in the url
                for shard in shards:
                    url += shard + "+"
                url = url[:-1]
            else:
                # if shards is not an array, or if shards has only one element, then put the single shard in the url
                url += shards

        if parameters:
            # if parameters were given
            param_list = [key + "=" + parameters[key] for key in parameters]
            url += ";"
            for param in param_list:
                url += param + ";"
            url = url[:-1]

        data = self.make_request(url, headers, self.apiNormalDelay)

        response = self.interpret(data, url)
        return response

    def telegram(self, client: str, tgid: str, key: str, recipient: str, recruitment: bool = False):
        """ Makes a request to the NationStates API to send a Telegram

        :param client: the API client key
        :param tgid: the ID of the telegram to be sent
        :param key: the Key of the telegram to be sent
        :param recipient: the nation to send the Telegram to
        :param recruitment: whether the TG is recruitment or not. Defaults to False.

        :return tuple: the response data from the api
        """

        url = "https://www.nationstates.net/cgi-bin/api.cgi?"
        headers = {'User-Agent': self.userAgent}

        nation_url = recipient.replace(" ", "_")

        url = url + "a=sendTG&client=" + client + "&tgid=" + tgid + "&key=" + key + "&to=" + nation_url

        if recruitment:
            data = self.make_request(url, headers, self.apiRecruitDelay)
        else:
            data = self.make_request(url, headers, self.apiTGDelay)

        response = self.interpret(data, url)
        return response

    def command(self, nation: str, command: str, parameters: dict, auth: tuple = ("", "", "")):
        """ Sends a command to the NS Api

        :param nation: the nation that the command is executed on
        :param command: the command to be issued to the API
        :param parameters: the shards issued alongside said command
        :param auth: authentication for the nation that the command is executed onn

        :return tuple: the response data from the api
        """
        nation_url = nation.replace(" ", "_")
        url = "https://www.nationstates.net/cgi-bin/api.cgi?nation=" + nation_url

        if (self._auth[0] == auth[0]) and (auth[0] != ""):
            headers = {'User-Agent': self.userAgent,
                       'X-Password': self._auth[0],
                       'X-Autologin': self._auth[1],
                       'X-Pin': self._auth[2]}
        elif auth[0] != "":
            headers = {'User-Agent': self.userAgent,
                       'X-Password': auth[0],
                       'X-Autologin': auth[1],
                       'X-Pin': auth[2]}
        else:
            headers = {'User-Agent': self.userAgent}

        url = url + "&c=" + command

        if parameters:
            # if parameters were given
            param_list = [key + "=" + parameters[key] for key in parameters]
            url += "&"
            for param in param_list:
                url += param + "&"
            url = url[:-1]

        data = self.make_request(url, headers, self.apiNormalDelay)

        response = self.interpret(data, url)
        return response

    def region(self, region: str, shards: str or list = None, parameters: dict = None):
        """ Makes a request to the NationStates API of a Region shard

            :param region: the region to be requested
            :param shards: The shards to be requested
            :param parameters: The parameters for the shards

            :return: the response data from the api
        """
        region_url = region.replace(" ", "_")
        url = "https://www.nationstates.net/cgi-bin/api.cgi?region="+region_url+"&"
        headers = {'User-Agent': self.userAgent}
        # sets the base URL, and sets the useragent in the headers

        if shards:
            # if shards were given
            url += "q="

            if isinstance(shards, list):
                # if shards is an array of multiple elements, then put the full list of shards in the url
                for shard in shards:
                    url += shard + "+"
                url = url[:-1]
            else:
                # if shards is not an array, or if shards has only one element, then put the single shard in the url
                url += shards

        if parameters:
            # if parameters were given
            param_list = [key + "=" + parameters[key] for key in parameters]
            url += ";"
            for param in param_list:
                url += param + ";"
            url = url[:-1]

        data = self.make_request(url, headers, self.apiNormalDelay)

        response = self.interpret(data, url)
        return response

    def world_assembly(self, council: int = 1, shards: str or list = None, parameters: dict = None):
        """ Makes a request to the NationStates API of a World shard

        :param council: the id of the council to ask about (1 is ga or 2 is sc)
        :param shards: the shards to ask about
        :param parameters: the parameters of the resolution to ask about

        :return: the response data from the api
        """
        url = "https://www.nationstates.net/cgi-bin/api.cgi?wa="+str(council)
        headers = {'User-Agent': self.userAgent}
        # sets the base URL, and sets the useragent in the headers

        if shards is not None:
            # if shards were given
            url += "&q="

            if isinstance(shards, list):
                # if shards is an array of multiple elements, then put the full list of shards in the url
                for shard in shards:
                    url += shard + "+"
                url = url[:-1]
            else:
                # if shards is not an array, or if shards has only one element, then put the single shard in the url
                url += shards

        if parameters:
            # if parameters were given
            param_list = [key + "=" + parameters[key] for key in parameters]
            url += ";"
            for param in param_list:
                url += param + ";"
            url = url[:-1]

        data = self.make_request(url, headers, self.apiNormalDelay)

        response = self.interpret(data, url)
        return response

    def verify(self, nation: str, checksum: str, token: str or list = ""):
        """ Makes an authentication request to the NS API with the given token.
            Note the "verbose" flag - this allows the user to see all headers instead of just the success header.
        
        :param nation: the nation being verified
        :param checksum: the checksum provided by the user
        :param token: optional site-specific token for verification

        :return: the response data from the api
        """
        url = "https://www.nationstates.net/cgi-bin/api.cgi?a=verify&nation="
        headers = {'User-Agent': self.userAgent}
        # sets the base URL, and sets the useragent in the headers

        url += nation + "&checksum=" + checksum

        if token != "":
            url += "&token="+token

        data = self.make_request(url, headers, self.apiNormalDelay)

        response = self.interpret(data, url)
        return response
