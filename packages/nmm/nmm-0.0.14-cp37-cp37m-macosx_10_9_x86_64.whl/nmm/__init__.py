from ._alphabet import (
    AlphabetType,
    AminoAlphabet,
    BaseAlphabet,
    DNAAlphabet,
    IUPACAminoAlphabet,
    RNAAlphabet,
)
from ._cdata import CData
from ._codon import Codon, codon_iter
from ._codon_prob import CodonProb
from ._input import Input
from ._model import Model
from ._output import Output
from ._state import CodonState, FrameState, StateType
from ._table import AminoTable, BaseTable, CodonTable
from ._testit import test
from ._translator import NTTranslator, NullTranslator, Translator

try:
    from ._ffi import lib
except Exception as e:
    _ffi_err = """
It is likely caused by a broken installation of this package.
Please, make sure you have a C compiler and try to uninstall
and reinstall the package again."""

    raise RuntimeError(str(e) + _ffi_err)

__version__ = "0.0.14"

__all__ = [
    "AlphabetType",
    "AminoAlphabet",
    "AminoTable",
    "BaseAlphabet",
    "BaseTable",
    "CData",
    "Codon",
    "CodonProb",
    "CodonState",
    "CodonTable",
    "DNAAlphabet",
    "FrameState",
    "IUPACAminoAlphabet",
    "Input",
    "Model",
    "NTTranslator",
    "NullTranslator",
    "Output",
    "RNAAlphabet",
    "StateType",
    "Translator",
    "__version__",
    "codon_iter",
    "lib",
    "test",
]
