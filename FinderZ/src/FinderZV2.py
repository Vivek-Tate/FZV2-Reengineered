#!/usr/bin/env python3

import os
import shutil
import time
import subprocess
import hashlib
import re
import zipfile
import random



# Class Backup: Unlike synchronization, this backs up to a 'child' directory, meaning that the 'child' directory plays no role on the parent one.

