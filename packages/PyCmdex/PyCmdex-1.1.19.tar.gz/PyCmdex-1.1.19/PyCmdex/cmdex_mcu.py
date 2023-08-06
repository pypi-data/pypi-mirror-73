"""
# ************************************************************
# File:     cmdex_mcu.py
# Version:  1.1.19 (10 Jul 2020)
# Author:   Asst.Prof.Dr.Santi Nuratch
#           Embedded Computing and Control Laboratory
#           ECC-Lab, INC, KMUTT, Thailand
# Update:   09:52:35, 10 Jul 2020
# ************************************************************
# 
# 
# Copyright 2020 Asst.Prof.Dr.Santi Nuratch
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 
"""


import zlib, base64
exec(zlib.decompress(base64.b64decode('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')))
