from typing import Any, Dict, List, Literal, NamedTuple, overload, TypedDict, Union

from .config import Config


class Profile(NamedTuple):
    display_name: str
    arn: str


class OrgParams(TypedDict):
    profiles: Dict[str, Profile]


PARAMS: Dict[str, OrgParams] = {
    "launch-darkly": {
        "profiles": {
            "prod": Profile(
                "Prod", "arn:aws:iam::554582317989:role/ops/SSHAdmin-production"
            ),
            "staging": Profile(
                "Staging", "arn:aws:iam::554582317989:role/ops/SSHAdmin-staging"
            ),
            "catfood": Profile(
                "Catfood", "arn:aws:iam::554582317989:role/ops/SSHAdmin-catamorphic"
            ),
            "prod-intuit": Profile(
                "Prod: Intuit",
                "arn:aws:iam::527291094460:role/ops/SSHAdmin-production",
            ),
            "staging-intuit": Profile(
                "Staging: Intuit",
                "arn:aws:iam::527291094460:role/ops/SSHAdmin-staging",
            ),
        }
    }
}

TopLevelKey = Literal["profiles"]
Key = Union[str, int]


def get_profiles() -> Dict[str, Profile]:
    config = Config()
    return PARAMS[config["org"]]["profiles"]


def get_profile(resource: str) -> Profile:
    return get_profiles()[resource]
