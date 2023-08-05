"""
# ************************************************************
# File:     cmdex_mcu.py
# Version:  1.1.18 (03 Jul 2020)
# Author:   Asst.Prof.Dr.Santi Nuratch
#           Embedded Computing and Control Laboratory
#           ECC-Lab, INC, KMUTT, Thailand
# Update:   16:40:50, 03 Jul 2020
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
