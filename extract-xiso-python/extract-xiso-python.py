from ctypes import cdll, POINTER, c_char_p
import pathlib
import os
from enum import Enum

class Modes(Enum):
  GENERATE_AV1 = 0
  EXTRACT = 1
  LIST = 2
  REWRITE = 3

def extract_xiso(in_xiso, optimized):
  shared_object = os.path.join(os.path.dirname(__file__), "extract-xiso", "libextract-xiso.so")
  extract_xiso = cdll.LoadLibrary(shared_object)
  in_xiso_bytes = c_char_p(in_xiso.encode('utf-8'))
  print(in_xiso)
  return extract_xiso.decode_xiso(in_xiso_bytes, None, Modes.EXTRACT.value, None, optimized)

extract_xiso(os.path.join(os.path.dirname(__file__),"Quantum Redshift (USA).iso"), False)
