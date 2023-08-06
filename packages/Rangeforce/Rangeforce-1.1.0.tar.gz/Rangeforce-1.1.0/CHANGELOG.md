Changelog
===============================================================================

All notable changes to this project will be documented in this file.

The format is based on 
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to 
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).


[1.1.0] - 2020-07-08
----------------------------------------

### Added

- `exactly(value, expected)` checking if a value is equal to the expected one.
  This behaves similarly to `assertEqual()`. It also evaluates NaN == NaN
  as True for practical reasons (details in function docs). 
- Parameter `ex` to all functions to customise the exception type.
  Defaults to `RangeError`, thus keeping backwards compatibility, but the user
  can choose to use `ValueError`, `OverflowError`, `FileNotFoundError`
  or any other custom exception class.



[1.0.0] - 2019-04-20
----------------------------------------

Initial version.
