import requests
import json
import logging
import uuid
import base64
from urllib.parse import urljoin
from pathlib import Path
import os
import re
from xml.dom import minidom
from string import Template, Formatter

cwdPath = Path.cwd()
thisPath = Path(__file__).parent

#from robot.api import logger
#from robot.libraries.BuiltIn import BuiltIn
#from robot.utils.asserts import assert_equal
#from robot.api.deco import keyword

"""
ATP Keywords Library for RobotFramework
"""
class ATPKeywords(object):
    ROBOT_LIBRARY_SCOPE = 'Global'

    ATP_DEFAULT_IMAGEPROCESSOR = 'local'
    ATP_DEFAULT_RELAYATPURL = 'http://localhost:9090/'
    ATP_DEFAULT_KEYMAP = "USKeyboard"

    def __init__(self, atpUrl, imageProcessor=ATP_DEFAULT_IMAGEPROCESSOR, relayAtpUrl=ATP_DEFAULT_RELAYATPURL, keyMap=ATP_DEFAULT_KEYMAP, keyMapPath=None):

        self._atpUrl = atpUrl
        self._imageProcessor = imageProcessor
        self._relayAtpUrl = relayAtpUrl
        self._keyMapName = keyMap

        #use internal keymappings
        if keyMapPath is None:
            self._keyMapDoc = minidom.parse(str(thisPath.joinpath("KeyMappings.xml")))
        else:
            if os.path.isabs(keyMapPath):
                self._keyMapDoc = minidom.parse(keyMapPath)
            else:
                self._keyMapDoc = minidom.parse(str(cwdPath.joinpath(keyMapPath)))

        self._keyMap = self._getKeyMapping(self._keyMapName)

        if self._imageProcessor == 'relay':
            pingResponse = self._call(self._getRelayAtpUrl('v3'), 'performPing')
            if pingResponse['Successful'] == False:
                raise Exception('Relay ATP instance not available!')

        if self._keyMap:
            keyMapResponse = self._call(self._getAtpUrl('v2'), 'setKeyMappings', [self._keyMap])
            if keyMapResponse['Successful'] == False:
                raise Exception('Unable to set ATP KeyMapping!')

    # Gets the ATP Url endpoint based on version (default v3)
    def _getAtpUrl(self, version='v3'):
        return urljoin(self._atpUrl, 'ATP/' + version)

    # Gets the ATP Relay Url endpoint based on version (default v3)
    def _getRelayAtpUrl(self, version='v3'):
        return urljoin(self._relayAtpUrl, 'ATP/' + version)

    # Gets KeyMapping by name
    def _getKeyMapping(self, name):
        items = self._keyMapDoc.getElementsByTagName('KeyMapping')
        i = None
        for item in items:
            if item.attributes['name'].value == self._keyMapName:
                i = item
                break

        keyMapping = {
                "keyMappings": []
        }

        if i != None:
            keys = i.getElementsByTagName('Key')
            for key in keys:
                keyMapping['keyMappings'].append({ 
                    "id": key.attributes['id'].value,
                    "keyCode": key.attributes['keycode'].value,
                    "name": key.attributes['name'].value
                })

        return keyMapping

    # Gets Key from set KeyMapping by name
    def _getKeyByName(self, name):
        for key in self._keyMap['keyMappings']:
            if key['name'] == name:
                return key
        return None

    # Gets Key from set KeyMapping by id
    def _getKeyById(self, id):
        for key in self._keyMap['keyMappings']:
            if key['id'] == id:
                return key
        return None

    # Gets Key from set KeyMapping by keyCode
    def _getKeyByCode(self, code):
        for key in self._keyMap['keyMappings']:
            if key['keyCode'] == code:
                return key
        return None

    # Creates a KeyAction (used within a KeySequence) from a Key object
    def _createKeyAction(self, key, press=True, release=True, preDelay=0, postDelay=0):
        return {
            "key": key,
            "press": press,
            "release": release,
            "preDelay": preDelay,
            "postDelay": postDelay,
            "returnScreenBuffer": False
        }

    # Gets a KeySequence (list of KeyActions) from a string. This decodes Tokens '{}' as Keys from Key Mapping
    # Otherwise decodes each character within string as a key.
    def _getKeySequenceFromString(self, keys):
        keySeq = []
        tokens = [el[1] for el in Formatter().parse(keys) if el[1] is not None]
        
        inToken = False
        tokenAdded = False

        for i in range(len(keys)):
            c = keys[i]

            #Start of a token
            if not inToken and c == "{":
                inToken = True
                tokenAdded = False

                for token in tokens:
                    if keys[i+1:i+1+len(token)] == token:
                        tokenItems = token.split('+')
                        tokenSeq = []

                        for t in range(len(tokenItems)):
                            tokenItem = tokenItems[t]
                            lastTokenItem = t == len(tokenItems)-1
                            tokenSuffixLen = 0
                            release = True

                            if not lastTokenItem:
                                tokenSuffixLen = 1
                                release = False

                            k = self._getKeyByName(tokenItem)
                            if k is not None:
                                keySeq.append(self._createKeyAction(k, release=release))
                                tokenAdded=True
                                i+=len(tokenItem) + tokenSuffixLen
                            else:
                                k = self._getKeyByCode(tokenItem)
                                if k is not None:
                                    keySeq.append(self._createKeyAction(k, release=release))
                                    tokenAdded=True
                                    i+=len(tokenItem) + tokenSuffixLen
                                else:
                                    k = self._getKeyById(tokenItem)
                                    if k is not None:
                                        keySeq.append(self._createKeyAction(k, release=release))
                                        tokenAdded=True
                                        i+=len(tokenItem) + tokenSuffixLen

                            if k is not None and not lastTokenItem:
                                tokenSeq.append(k)

                        if len(tokenSeq) > 0:
                            tokenSeq.reverse()
                            for k in tokenSeq:
                                keySeq.append(self._createKeyAction(k, press=False, release=True))

            if inToken and c == "}":
                inToken = False
                tokenAdded = False
            elif not tokenAdded:
                k = self._getKeyByName(c)
                if k is not None:
                    keySeq.append(self._createKeyAction(k))

        return keySeq


    # Validates an ATPResponse object.
    # If result = True - Validate a 'result' object was returned in the ATP Response, and that response was successful
    # If errors = True - Validate response does not have errors reported aswell
    def _validateResponse(self, response, result=True, errors=True):

        try:
            logging.debug('ATP:validateResponse')
            logging.debug(json.dumps(response, indent=4))

            if result == True:
                if response['result']:
                    assert response['result'], 'Invalid ATP Response'
                    assert response['result']['Successful'] == True, 'ATP Response was not successful'
                    #assert response['result']['Result'], 'ATP Response has no result'
                    if errors == True:
                        assert len(response['result']['Errors']) == 0, 'ATP Response contains errors'
                else:
                    assert response != None, 'Invalid ATP Response'
            if response['result']:        
                return response['result']
            else:
                return response
        except Exception as error:
            logging.error(error)
            assert error, error

    # Performs an ATP Call using HTTP Post against ATP Server, via a JSON RPC payload.
    def _call(self, url, method, params=[{}], validateResult=True, validateErrors=True):
        try:
            logging.debug('ATP:call ' + method + ' @ ' + url)

            payload = {
                "method": method,
                "params": params,
                "jsonrpc": "2.0",
                "id": str(uuid.uuid4())
            }

            response = requests.post(url, json=payload)

            logging.debug(response.text)
            
            return self._validateResponse(response.json(), validateResult, validateErrors)
        except Exception as error:
            logging.error(error)

    # Calls the ATP Ping method. Used to ping the ATP Server
    def atp_ping(self):
        """ ATP Ping: Pings ATP server """
        return self._call(self._getAtpUrl('v3'), 'performPing',[{}], True)

    # Calls the ATP Kill method. Kills the remote ATP Server process
    def atp_kill(self):
        """ ATP Kill: Kills ATP server """
        return self._call(self._getAtpUrl('v2'), 'kill', [], False)

    # Calls the ATP Delay method. Performs a Thread delay with the ATP server process.
    def atp_delay(self, duration):
        """ ATP Delay: Delays X milliseconds """
        return self._call(self._getAtpUrl('v2'), 'delay', [duration], False)

    # Calls the ATP Take Screen Capture method. Takes a remote screen shot of the machine running 
    # the ATP Server component, and returns image (PNG) as a Base64 String
    def atp_take_screen_capture(self):
        """ ATP Take Screen Capture: Takes Screen capture on ATP server """
        return self._call(self._getAtpUrl('v2'), 'takeScreenCapture',[], True)

    # Calls the ATP Take Screen Capture method and saves to local file. Takes Screen Shot on remote ATP server
    # and saves to local file
    def atp_save_screen_capture(self, filename):
        """ ATP Save Screen Capture: Takes and Saves screen capture from ATP server to file """
        response = self.atp_take_screen_capture()
        data = base64.b64decode(response['Result'])
        with open(filename, 'wb') as f:
            f.write(data)

    # Reads a local image file, and returns as a Base64 String. (To be used when sending within ATP Requests)
    def _read_image(self, filename):
        filepath = self._parse_filepath(filename)

        with open(filepath.absolute(), "rb") as imgFile:
            imgBytes = imgFile.read()

        base64Bytes = base64.b64encode(imgBytes).decode('utf-8')
        return str(base64Bytes)

    # Parses a filename string. Either will check if absolute and exists, otherwise
    # resolves based on Command Working Directory and returns the absolute path
    def _parse_filepath(self, filepath):
        filepath = Path(filepath)
        if not filepath.is_absolute() and not filepath.exists():
            filepath = cwdPath.joinpath(filepath)
        return filepath.absolute()


    # Checks if a string is base64 encoded.
    def _is_base64(self, s):
        pattern = re.compile("^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$")
        if not s or len(s) < 1:
            return False
        else:
            return pattern.match(s)

    # Calls the ATP Find Image In method. Uses a ATP Server to find a image within another image.
    # This is normally used within a Relay setup, where host does not support Sikuli, and hence takes
    # screen shot, and uses another host to perform find image in, to get results (location of image) within
    # other image.
    def atp_find_image_in(self, findImage, targetImage, findText=None, tolerance=0.95):
        """ ATP Find Image In: Finds image inside another image """

        findInPayload = {
            "tolerance": tolerance,
            "findText": findText,
            "findImage": findImage,
            "targetImage": targetImage
        }

        if self._imageProcessor == 'relay':
            return self._call(self._getRelayAtpUrl('v3'), 'performFindImageIn',[findInPayload], True)
        else:
            return self._call(self._getAtpUrl('v3'), 'performFindImageIn', [findInPayload], True)

    # Calls the ATP Click method. Used to perform a mouse click based on:
    # Image location
    # Offset (either offset of entire screen, when no image defined, or offset from where the image was found)
    def atp_click(self, type='LEFTSINGLE', image=None, offset=None, highlight=True, preDelay=0, postDelay=0, tolerance=0.95):
        """ ATP Click: Mouse moves and clicks where an image is found """

        calcOffset = None
        clickPayload = {
            "clickType": type,
            "highlight": highlight,
            "preDelay": preDelay,
            "postDelay": postDelay
        }

        if image is not None:
            if self._imageProcessor == "relay":
                
                imageData = self._read_image(image)
                logging.debug('Find: ' + imageData)

                findImage = {
                    "imageData": imageData,
                    "imagePath": image
                }

                targetResponse = self.atp_take_screen_capture()
                logging.debug('Target: ' + targetResponse['Result'])

                targetImage = {
                    "imageData": targetResponse['Result']
                }

                findImageInResponse = self.atp_find_image_in(findImage, targetImage, tolerance=tolerance)

                #need to validate response matches
                match = findImageInResponse['Result']['Matches'][0]

                if offset is not None:
                    #Offset the found image location
                    offsetSplit = offset.split(",")
                    offsetX = offsetSplit[0].trim()
                    offsetY = offsetSplit[1].trim()
                    calcOffset = str(match['x'] + int(offsetX)) + ',' + str(match['y'] + int(offsetY))
                else:
                    #Calc middle of found region
                    calcOffset = str(match['x'] + int(match['width'] / 2)) + ',' + str(match['y'] + int(match['height'] / 2))

            else:
                if self._is_base64(image):
                    clickPayload['image'] = {
                        "imageData": image
                    }
                else:
                    clickPayload['image'] = {
                        "imageData": self._read_image(image),
                        "imagePath": image
                    }

                calcOffset = offset
        else:
            calcOffset = offset
            
        clickPayload['clickOffset'] = calcOffset
        
        try:
            clickResponse = self._call(self._getAtpUrl('v3'), 'performClick', [clickPayload], True)
        except Exception as err:
            print(err)
        
        return clickResponse

    # Calls the ATP KeyPress method. Performs a single KeyAction (with press = True) based on a Key element
    def atp_keyPress(self, key, release=True, preDelay=0, postDelay=0):
        """ ATP KeyPress: Press a single key (default to not release) """

        if isinstance(key, str):
            key = self._getKeySequenceFromString(key)
            if len(key) != 1:
                raise Exception('Inavlid key value specified for keyPress!')

        payload = {
            "key": key[0],
            "press": True,
            "release": release,
            "preDelay": preDelay,
            "postDelay": postDelay,
            "returnScreenBuffer": False
        }
        
        try:
            response = self._call(self._getAtpUrl('v3'), 'keyPress', [payload], True)
        except Exception as err:
            print(err)
        
        return response

    # Calls the ATP KeyRelease method. Performs a single KeyAction (with press = False, Release = True) based on a Key element
    def atp_keyRelease(self, key, preDelay=0, postDelay=0):
        """ ATP KeyRelease: Release previously pressed key """

        if isinstance(key, str):
            key = self._getKeySequenceFromString(key)
            if len(key) != 1:
                raise Exception('Inavlid key value specified for keyPress!')

        payload = {
            "key": key[0],
            "press": False,
            "release": True,
            "preDelay": preDelay,
            "postDelay": postDelay,
            "returnScreenBuffer": False
        }
        
        try:
            response = self._call(self._getAtpUrl('v3'), 'keyRelease', [payload], True)
        except Exception as err:
            print(err)
        
        return response

    # Calls the ATP KeyPress Sequence method. This takes in a string and decodes this into a key sequence (collection of Key Actions)
    # String is decoded by tokens {..} that if match a Key within the current Key Mapping, otherwise decodes each character within the string
    def atp_keyPressSequence(self, keys, preDelay=0, postDelay=0):
        """ ATP KeyPressSequence: Press and release numerious keys """

        if isinstance(keys, str):
            keys = self._getKeySequenceFromString(keys)

        payload = {
            "sequence": keys,
            "preDelay": preDelay,
            "postDelay": postDelay,
            "detectScreenChange": False,
            "screenChangeTimeout": 30000,
            "screenChangeArea": "0,0,*,*",
            "actionDelay": 250,
            "returnScreenBuffer": False
        }
        
        try:
            response = self._call(self._getAtpUrl('v3'), 'keyPressSequence', [payload], True)
        except Exception as err:
            print(err)
        
        return response

    def atp_getSettings(self):
        """ ATP Get Settings: Retrieves Proxy Settings from ATP Server """
        return self._call(self._getAtpUrl('v2'), 'getSettings',[], True)

    def atp_setSettings(self, settings):
        """ ATP Set Settings: Sets Proxy Settings for ATP Server """
        return self._call(self._getAtpUrl('v2'), 'setSettings',[settings], True)

    def atp_openApp(self, command):
        """ ATP Open App: Sends command to open application using Sikuli """

        payload = {
            "command": command,
        }

        return self._call(self._getAtpUrl('v3'), 'performOpenApp', [payload], True)

    def atp_closeApp(self, appName):
        """ ATP Open App: Sends command to open application using Sikuli """

        payload = {
            "appName": appName,
        }

        return self._call(self._getAtpUrl('v3'), 'performCloseApp', [payload], True)

    # Calls the ATP Assert method. Validates image exists on the screen
    # type = 'SCREENIMAGE' (default) | 'SCREENTEXT'
    # image = Base64 String of image | Path to image file
    # relative = **Not implemented yet
    # relativeLength = **Not implemented yet
    # tolerance = Tolerance level for asserted (found) image (default 0.95)
    # timeout = Timeout to wait for image to be asserted (default 20000 ms)
    def atp_assert(self, image, type="SCREENIMAGE", relative=None, relativeLength=0, tolerance=0.95, timeout=20000):
        """ ATP Assert: Performs an image assert on the remote ATP Server """

        payload = {
            "assertType": type,
            "tolerance": tolerance,
            "timeout": timeout,
            "relative": relative,
            "relativeLength": relativeLength
        }

        if self._is_base64(image):
            payload['image'] = {
                "imageData": image
            }
        else:
            payload['image'] = {
                "imageData": self._read_image(image),
                "imagePath": image
            }
            
        return self._call(self._getAtpUrl('v3'), 'performAssert', [payload], True)

    # Calls the ATP Wait Until method. Waits until text or image, appears or vanishes.
    # image = | Base64 String of Image | path to image file
    # text = Text to be detected or vanish (depends on type)
    # textRegEx = True if text is a regular expression, default = False
    # type = 'IMAGEAPPEARS' | 'IMAGEVANISHES' (when image property providedd) | 'TEXTAPPEARS' | 'TEXTVANISHES' (when text property provided)
    # region = 'SCREEN' (default) to use screen to detect | 'WINDOW' to use open application (when open app method call) as detection region
    def atp_waitUntil(self, image=None, text=None, textRegEx=False, type="IMAGEAPPEARS", region="SCREEN", tolerance=0.95, timeout=30000):
        """ ATP Wait Until: Waits until 'IMAGEAPPEARS', 'IMAGEVANISHES', 'TEXTAPPEARS' or 'TEXTVANISHES' """

        payload = {
            "timeout": timeout,
            "tolerance": tolerance,
            "waitUntilType": type,
            "waitUntilRegion": region
        }

        if image is not None:
            if self._is_base64(image):
                payload['image'] = {
                    "imageData": image
                }
            else:
                payload['image'] = {
                    "imageData": self._read_image(image),
                    "imagePath": image
                }
        elif text is not None:
            payload['text'] = text
            payload['textIsRegEx'] = textRegEx

        return self._call(self._getAtpUrl('v3'), 'performWaitUntil', [payload], True)
            
