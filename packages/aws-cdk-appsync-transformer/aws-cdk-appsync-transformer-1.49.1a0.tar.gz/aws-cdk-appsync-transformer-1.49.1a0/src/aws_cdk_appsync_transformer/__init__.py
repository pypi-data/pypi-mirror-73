"""
# AppSync Transformer Construct for AWS CDK

![build](https://github.com/kcwinner/aws-cdk-appsync-transformer/workflows/build/badge.svg)
[![codecov](https://codecov.io/gh/kcwinner/aws-cdk-appsync-transformer/branch/main/graph/badge.svg)](https://codecov.io/gh/kcwinner/aws-cdk-appsync-transformer)
[![dependencies Status](https://david-dm.org/kcwinner/aws-cdk-appsync-transformer/status.svg)](https://david-dm.org/kcwinner/aws-cdk-appsync-transformer)
[![npm](https://img.shields.io/npm/dt/aws-cdk-appsync-transformer)](https://www.npmjs.com/package/aws-cdk-appsync-transformer)

[![npm version](https://badge.fury.io/js/aws-cdk-appsync-transformer.svg)](https://badge.fury.io/js/aws-cdk-appsync-transformer)
[![NuGet version](https://badge.fury.io/nu/Kcwinner.AWSCDKAppSyncTransformer.svg)](https://badge.fury.io/nu/Kcwinner.AWSCDKAppSyncTransformer)
[![PyPI version](https://badge.fury.io/py/aws-cdk-appsync-transformer.svg)](https://badge.fury.io/py/aws-cdk-appsync-transformer)
[![Maven Central](https://img.shields.io/maven-central/v/io.github.kcwinner/AWSCDKAppSyncTransformer?color=brightgreen)](https://repo1.maven.org/maven2/io/github/kcwinner/AWSCDKAppSyncTransformer/)

## Why This Package

In April 2020 I wrote a [blog post](https://www.trek10.com/blog/appsync-with-the-aws-cloud-development-kit) on using the AWS Cloud Development Kit with AppSync. I wrote my own transformer in order to emulate AWS Amplify's method of using GraphQL directives in order to template a lot of the Schema Definition Language.

This package is my attempt to convert all of that effort into a separate construct in order to clean up the process.

## How Do I Use It

### Example TypeScript Usage

stack.ts

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk_appsync_transformer import AppSyncTransformer
AppSyncTransformer(self, "my-cool-api",
    schema_path="schema.graphql"
)
```

schema.graphql

```graphql
type Customer
    @model
    @auth(rules: [
        { allow: groups, groups: ["Admins"] },
        { allow: private, provider: iam, operations: [read, update] }
    ]) {
        id: ID!
        firstName: String!
        lastName: String!
        active: Boolean!
        address: String!
}

type Product
    @model
    @auth(rules: [
        { allow: groups, groups: ["Admins"] },
        { allow: public, provider: iam, operations: [read] }
    ]) {
        id: ID!
        name: String!
        description: String!
        price: String!
        active: Boolean!
        added: AWSDateTime!
        orders: [Order] @connection
}

type Order @model
    @key(fields: ["id", "productID"]) {
        id: ID!
        productID: ID!
        total: String!
        ordered: AWSDateTime!
}
```

### [Supported Amplify Directives](https://docs.amplify.aws/cli/graphql-transformer/directives)

Tested:

* [@model](https://docs.amplify.aws/cli/graphql-transformer/directives#model)
* [@auth](https://docs.amplify.aws/cli/graphql-transformer/directives#auth)
* [@connection](https://docs.amplify.aws/cli/graphql-transformer/directives#connection)

Experimental:

* [@key](https://docs.amplify.aws/cli/graphql-transformer/directives#key)
* [@versioned](https://docs.amplify.aws/cli/graphql-transformer/directives#versioned)

Not Yet Supported:

* [@function](https://docs.amplify.aws/cli/graphql-transformer/directives#function)
* [@searchable](https://docs.amplify.aws/cli/graphql-transformer/directives#searchable)
* [@predictions](https://docs.amplify.aws/cli/graphql-transformer/directives#predictions)
* [@http](https://docs.amplify.aws/cli/graphql-transformer/directives#http)

### Authentication

Unauth Role: TODO

Auth Role: Unsupported (for now?). Authorized roles (Lambda Functions, EC2 roles, etc) are required to setup their own role permissions.

### Code Generation

I've written some helpers to generate code similarly to how AWS Amplify generates statements and types. You can find the code [here](https://github.com/kcwinner/advocacy/tree/master/cdk-amplify-appsync-helpers).

## Versioning

I will *attempt* to align the major and minor version of this package with [AWS CDK](https://aws.amazon.com/cdk), but always check the release descriptions for compatibility.

I currently support [![GitHub package.json dependency version (prod)](https://img.shields.io/github/package-json/dependency-version/kcwinner/appsync-transformer-construct/@aws-cdk/core)](https://github.com/aws/aws-cdk)

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for details

## License

Distributed under [Apache License, Version 2.0](LICENSE)
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

import aws_cdk.aws_appsync
import aws_cdk.aws_dynamodb
import aws_cdk.core


class AppSyncTransformer(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-appsync-transformer.AppSyncTransformer",
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
        schema_path: str,
        api_name: typing.Optional[str] = None,
        authorization_config: typing.Optional[
            aws_cdk.aws_appsync.AuthorizationConfig
        ] = None,
        sync_enabled: typing.Optional[bool] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param schema_path: 
        :param api_name: 
        :param authorization_config: 
        :param sync_enabled: 

        stability
        :stability: experimental
        """
        props = AppSyncTransformerProps(
            schema_path=schema_path,
            api_name=api_name,
            authorization_config=authorization_config,
            sync_enabled=sync_enabled,
        )

        jsii.create(AppSyncTransformer, self, [scope, id, props])

    @jsii.member(jsii_name="createSyncTable")
    def create_sync_table(self, table_data: typing.Any) -> aws_cdk.aws_dynamodb.Table:
        """
        :param table_data: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "createSyncTable", [table_data])

    @builtins.property
    @jsii.member(jsii_name="appsyncAPI")
    def appsync_api(self) -> aws_cdk.aws_appsync.GraphQLApi:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "appsyncAPI")

    @builtins.property
    @jsii.member(jsii_name="nestedAppsyncStack")
    def nested_appsync_stack(self) -> aws_cdk.core.NestedStack:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "nestedAppsyncStack")

    @builtins.property
    @jsii.member(jsii_name="tableNameMap")
    def table_name_map(self) -> typing.Any:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "tableNameMap")


@jsii.data_type(
    jsii_type="aws-cdk-appsync-transformer.AppSyncTransformerProps",
    jsii_struct_bases=[],
    name_mapping={
        "schema_path": "schemaPath",
        "api_name": "apiName",
        "authorization_config": "authorizationConfig",
        "sync_enabled": "syncEnabled",
    },
)
class AppSyncTransformerProps:
    def __init__(
        self,
        *,
        schema_path: str,
        api_name: typing.Optional[str] = None,
        authorization_config: typing.Optional[
            aws_cdk.aws_appsync.AuthorizationConfig
        ] = None,
        sync_enabled: typing.Optional[bool] = None,
    ) -> None:
        """
        :param schema_path: 
        :param api_name: 
        :param authorization_config: 
        :param sync_enabled: 

        stability
        :stability: experimental
        """
        if isinstance(authorization_config, dict):
            authorization_config = aws_cdk.aws_appsync.AuthorizationConfig(
                **authorization_config
            )
        self._values = {
            "schema_path": schema_path,
        }
        if api_name is not None:
            self._values["api_name"] = api_name
        if authorization_config is not None:
            self._values["authorization_config"] = authorization_config
        if sync_enabled is not None:
            self._values["sync_enabled"] = sync_enabled

    @builtins.property
    def schema_path(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("schema_path")

    @builtins.property
    def api_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("api_name")

    @builtins.property
    def authorization_config(
        self,
    ) -> typing.Optional[aws_cdk.aws_appsync.AuthorizationConfig]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("authorization_config")

    @builtins.property
    def sync_enabled(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("sync_enabled")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppSyncTransformerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AppSyncTransformer",
    "AppSyncTransformerProps",
]

publication.publish()
