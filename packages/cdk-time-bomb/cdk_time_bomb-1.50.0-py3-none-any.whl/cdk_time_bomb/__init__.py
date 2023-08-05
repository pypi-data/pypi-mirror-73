"""
# cdk-time-bomb

[![npm version](https://badge.fury.io/js/cdk-time-bomb.svg)](https://badge.fury.io/js/cdk-time-bomb)
[![PyPI Version](https://badge.fury.io/py/cdk-time-bomb.svg)](https://badge.fury.io/py/cdk-time-bomb)

Implode your AWS CDK Stack after set amount of time, save money, be happy!

## Usage

In your Typescipt / Javascript AWS CDK project, add the `cdk-time-bomb` module:

```bash
npm install cdk-time-bomb
```

Import the module and instantiate in your CDK Stack class.  Specify a TTL Duration after which time the entire CloudFormation stack will self destroy:

```javascript
import { SelfDestruct} from 'cdk-time-bomb';
const selfDestruct = new SelfDestruct(this, "selfDestructor", {
  timeToLive: Duration.minutes(60)
});
```

## Build and Deploy

Due to the large amount of dependencies required by jsii, use the docker image `udondan/jsii-publish` to reliably and consistenly build this CDK construct.

```bash
docker run -it \
    --workdir /workdir \
    --volume $(pwd):/workdir \
    --env VERSION=0.3.0 \
    --env BUILD_SOURCE=true \
    --env BUILD_PACKAGES=true \
    --env NPM_TOKEN \
    --env PYPI_TOKEN \
    --env NUGET_TOKEN \
    --env GITHUB_TOKEN \
    --env GITHUB_REPOSITORY="${OWNER}/${REPOSITORY}" \
    udondan/jsii-publish:0.8.3
```
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *

import aws_cdk.core


class SelfDestruct(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-time-bomb.SelfDestruct",
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        time_to_live: aws_cdk.core.Duration,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param time_to_live: 

        stability
        :stability: experimental
        """
        props = SelfDestructProps(time_to_live=time_to_live)

        jsii.create(SelfDestruct, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-time-bomb.SelfDestructProps",
    jsii_struct_bases=[],
    name_mapping={"time_to_live": "timeToLive"},
)
class SelfDestructProps:
    def __init__(self, *, time_to_live: aws_cdk.core.Duration) -> None:
        """
        :param time_to_live: 

        stability
        :stability: experimental
        """
        self._values = {
            "time_to_live": time_to_live,
        }

    @builtins.property
    def time_to_live(self) -> aws_cdk.core.Duration:
        """
        stability
        :stability: experimental
        """
        return self._values.get("time_to_live")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SelfDestructProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SelfDestruct",
    "SelfDestructProps",
]

publication.publish()
