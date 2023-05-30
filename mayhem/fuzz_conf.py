#!/usr/bin/env python3
import atheris
import sys

from pyparsing import ParseSyntaxException, ParseException

import fuzz_helpers

with atheris.instrument_imports():
    from pyhocon import ConfigFactory, ConfigWrongTypeException, ConfigSubstitutionException

def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    choice = fdp.ConsumeIntInRange(0,2)
    try:
        if choice == 0:
            ConfigFactory.parse_string(fdp.ConsumeRemainingString())
        elif choice == 1:
            ConfigFactory.parse_URL(fdp.ConsumeRemainingString())
        else:
            with fdp.ConsumeTemporaryFile(suffix='.conf') as f:
                ConfigFactory.parse_file(f)
    except (ValueError, ParseSyntaxException, ParseException,ConfigWrongTypeException, ConfigSubstitutionException):
        return -1
def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
