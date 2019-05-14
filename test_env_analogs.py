#!/usr/bin/env python

import sys
import time
import requests
from datetime import datetime
from envirophat import light, weather, motion, analog


print(analog.read(0))
print(analog.read(1))