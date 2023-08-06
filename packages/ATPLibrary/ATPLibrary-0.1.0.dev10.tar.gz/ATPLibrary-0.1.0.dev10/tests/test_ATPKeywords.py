import pytest
from ctypes import windll, Structure, c_long, byref
import base64
import os
import pathlib
import time

thisDir = pathlib.Path(__file__).parent
INVALID_RESPONSE = "Invalid Response"

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def getMousePos():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return { "x": pt.x, "y": pt.y}

def readImage(filename):
    filepath = pathlib.Path(filename)
    if not filepath.is_absolute() and not filepath.exists():
        filepath = thisDir.joinpath(filename)

    with open(filepath.absolute(), "rb") as imgFile:
        imgBytes = imgFile.read()

    base64Bytes = base64.b64encode(imgBytes).decode('utf-8')
    return str(base64Bytes)

@pytest.fixture
def keywords():
    from ATPLibrary.ATPKeywords import ATPKeywords
    return ATPKeywords('http://localhost:9090/', 'local')

def test_atp_ping(keywords):
    response = keywords.atp_ping()
    assert response, INVALID_RESPONSE

def test_atp_delay(keywords):
    response = keywords.atp_delay(duration=2000)
    assert response, INVALID_RESPONSE

def test_atp_click_offset(keywords):
    response = keywords.atp_click(offset="0,0")
    assert response, INVALID_RESPONSE
    mouse = getMousePos()
    print(mouse)
    assert mouse['x'] == 0, 'Mouse X not at 0'
    assert mouse['y'] == 0, 'Mouse Y not at 0'

    response = keywords.atp_click(offset="100,50")
    assert response, INVALID_RESPONSE
    mouse = getMousePos()
    print(mouse)
    assert mouse['x'] == 100, 'Mouse X not at 100'
    assert mouse['y'] == 50, 'Mouse Y not at 50'

    response = keywords.atp_click(offset="2*,2*")
    assert response, INVALID_RESPONSE
    mouse = getMousePos()
    print(mouse)
    #assert mouse['x'] == 100, 'Mouse X not at 100'
    #assert mouse['y'] == 50, 'Mouse Y not at 50'

def test_atp_click_image(keywords):
    #make sure mouse is at 0,0
    response = keywords.atp_click(offset="0,0")
    assert response, INVALID_RESPONSE

    #Click based on image LEFTSINGLE
    response = keywords.atp_click(image="tests/start.png")
    assert response, INVALID_RESPONSE

    keywords.atp_delay(duration=1000)
    keywords.atp_keyPressSequence(keys='{Escape}')

    response = keywords.atp_click(offset="0,0")
    assert response, INVALID_RESPONSE

    response = keywords.atp_click(image="tests/start.png", type="RIGHTSINGLE")
    assert response, INVALID_RESPONSE

    keywords.atp_delay(duration=1000)
    keywords.atp_keyPressSequence(keys='{Escape}')

def test_atp_click_preDelay(keywords):
    #make sure mouse is at 0,0
    response = keywords.atp_click(offset="0,0")
    assert response, INVALID_RESPONSE

    start = time.time()

    response = keywords.atp_click(offset="100,100", preDelay=1000)
    assert response, INVALID_RESPONSE

    end = time.time()

    assert (end - start) * 1000 >= 1000, 'Expected elapsed time >= 1000'

def test_atp_click_postDelay(keywords):
    #make sure mouse is at 0,0
    response = keywords.atp_click(offset="0,0")
    assert response, INVALID_RESPONSE

    start = time.time()

    response = keywords.atp_click(offset="100,100", postDelay=1000)
    assert response, INVALID_RESPONSE

    end = time.time()

    assert (end - start) * 1000 >= 1000, 'Expected elapsed time >= 1000'
    
def test_atp_sendkeySequenceWithNamedKey(keywords):
    response = keywords.atp_keyPressSequence(keys='{Windows+r}')
    assert response, INVALID_RESPONSE

    response = keywords.atp_keyPressSequence(keys='notepad{Enter}')
    assert response, INVALID_RESPONSE

    response = keywords.atp_keyPressSequence(keys='Hello')
    assert response, INVALID_RESPONSE

    response = keywords.atp_keyPressSequence(keys='{Backspace}{Backspace}{Backspace}{Backspace}{Backspace}')
    assert response, INVALID_RESPONSE

    response = keywords.atp_keyPressSequence(keys='{Alt+F4}')
    assert response, INVALID_RESPONSE

def test_atp_assert(keywords):
    response = keywords.atp_assert(image='tests/start.png', timeout=5000)
    assert response, INVALID_RESPONSE
    assert response['Result']['AssertValid'] == True, 'Assert True Expected'
    assert response['Result']['TimedOut'] == False, 'Assert TimedOut False Expected'

    response = keywords.atp_assert(image='tests/calc.png', timeout=5000)
    assert response, INVALID_RESPONSE
    assert response['Result']['AssertValid'] == False, 'Assert False Expected'
    assert response['Result']['TimedOut'] == True, 'Assert TimedOut True Expected'

def test_atp_openApp(keywords):
    response = keywords.atp_openApp(command=r'C:\Windows\System32\notepad.exe')
    assert response, INVALID_RESPONSE
    
    #WV: 10/07 - Need to investigate why this is not working!
    #response = keywords.atp_assert(image='tests/notepad_title.png', timeout=5000)
    #assert response, INVALID_RESPONSE
    #assert response['Result']['AssertValid'] == True, 'Assert True Expected'
    #assert response['Result']['TimedOut'] == True, 'Assert TimedOut False Expected'

def test_atp_closeApp(keywords):
    response = keywords.atp_openApp(command=r'C:\Windows\System32\notepad.exe')
    assert response, INVALID_RESPONSE
    
    #response = keywords.atp_assert(image='tests/notepad_icon.png', timeout=5000)
    #assert response, INVALID_RESPONSE
    #assert response['Result']['AssertValid'] == True, 'Assert True Expected'
    #assert response['Result']['TimedOut'] == True, 'Assert TimedOut False Expected'

    response = keywords.atp_closeApp(appName='notepad.exe')
    assert response, INVALID_RESPONSE

def test_atp_waitUntil(keywords):
    response = keywords.atp_openApp(command=r'C:\Windows\System32\notepad.exe')
    assert response, INVALID_RESPONSE

    response = keywords.atp_waitUntil(image=r'tests/notepad_title.png')
    assert response, INVALID_RESPONSE

    response = keywords.atp_closeApp(appName='notepad.exe')
    assert response, INVALID_RESPONSE
    
    #response = keywords.atp_assert(image='tests/notepad_title.png', timeout=5000)
    #assert response, INVALID_RESPONSE
    #assert response['Result']['AssertValid'] == True, 'Assert True Expected'
    #assert response['Result']['TimedOut'] == True, 'Assert TimedOut False Expected'
