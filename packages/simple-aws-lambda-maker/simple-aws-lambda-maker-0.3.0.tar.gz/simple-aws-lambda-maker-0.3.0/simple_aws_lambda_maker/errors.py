from delfick_project.errors import DelfickError, ProgrammerError
from delfick_project.norms import BadSpec, BadSpecValue


class SalmError(DelfickError):
    pass


# Explicitly make these errors in this context
BadSpec = BadSpec
BadSpecValue = BadSpecValue
ProgrammerError = ProgrammerError


class BadYaml(SalmError):
    desc = "Invalid yaml file"


class BadConfiguration(SalmError):
    desc = "Bad configuration"


class BadOptionFormat(SalmError):
    desc = "Bad option format"


class NoSuchTask(SalmError):
    desc = "No such task"


class NoFunctionsSpecified(SalmError):
    desc = "No functions were found in the configuration"


class NoSuchGroup(SalmError):
    desc = "Couldn't find specified group"


class GroupNotSpecified(SalmError):
    desc = "Please specify a group with --group"
