"""
## AWS Web Application Firewall Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.
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


@jsii.implements(aws_cdk.core.IInspectable)
class CfnByteMatchSet(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-waf.CfnByteMatchSet"):
    """A CloudFormation ``AWS::WAF::ByteMatchSet``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-bytematchset.html
    cloudformationResource:
    :cloudformationResource:: AWS::WAF::ByteMatchSet
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, name: str, byte_match_tuples: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "ByteMatchTupleProperty"]]]]=None) -> None:
        """Create a new ``AWS::WAF::ByteMatchSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::WAF::ByteMatchSet.Name``.
        :param byte_match_tuples: ``AWS::WAF::ByteMatchSet.ByteMatchTuples``.
        """
        props = CfnByteMatchSetProps(name=name, byte_match_tuples=byte_match_tuples)

        jsii.create(CfnByteMatchSet, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnByteMatchSet":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::WAF::ByteMatchSet.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-bytematchset.html#cfn-waf-bytematchset-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="byteMatchTuples")
    def byte_match_tuples(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "ByteMatchTupleProperty"]]]]:
        """``AWS::WAF::ByteMatchSet.ByteMatchTuples``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-bytematchset.html#cfn-waf-bytematchset-bytematchtuples
        """
        return jsii.get(self, "byteMatchTuples")

    @byte_match_tuples.setter
    def byte_match_tuples(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "ByteMatchTupleProperty"]]]]) -> None:
        jsii.set(self, "byteMatchTuples", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnByteMatchSet.ByteMatchTupleProperty", jsii_struct_bases=[], name_mapping={'field_to_match': 'fieldToMatch', 'positional_constraint': 'positionalConstraint', 'text_transformation': 'textTransformation', 'target_string': 'targetString', 'target_string_base64': 'targetStringBase64'})
    class ByteMatchTupleProperty():
        def __init__(self, *, field_to_match: typing.Union[aws_cdk.core.IResolvable, "CfnByteMatchSet.FieldToMatchProperty"], positional_constraint: str, text_transformation: str, target_string: typing.Optional[str]=None, target_string_base64: typing.Optional[str]=None) -> None:
            """
            :param field_to_match: ``CfnByteMatchSet.ByteMatchTupleProperty.FieldToMatch``.
            :param positional_constraint: ``CfnByteMatchSet.ByteMatchTupleProperty.PositionalConstraint``.
            :param text_transformation: ``CfnByteMatchSet.ByteMatchTupleProperty.TextTransformation``.
            :param target_string: ``CfnByteMatchSet.ByteMatchTupleProperty.TargetString``.
            :param target_string_base64: ``CfnByteMatchSet.ByteMatchTupleProperty.TargetStringBase64``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples.html
            """
            self._values = {
                'field_to_match': field_to_match,
                'positional_constraint': positional_constraint,
                'text_transformation': text_transformation,
            }
            if target_string is not None: self._values["target_string"] = target_string
            if target_string_base64 is not None: self._values["target_string_base64"] = target_string_base64

        @builtins.property
        def field_to_match(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnByteMatchSet.FieldToMatchProperty"]:
            """``CfnByteMatchSet.ByteMatchTupleProperty.FieldToMatch``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples.html#cfn-waf-bytematchset-bytematchtuples-fieldtomatch
            """
            return self._values.get('field_to_match')

        @builtins.property
        def positional_constraint(self) -> str:
            """``CfnByteMatchSet.ByteMatchTupleProperty.PositionalConstraint``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples.html#cfn-waf-bytematchset-bytematchtuples-positionalconstraint
            """
            return self._values.get('positional_constraint')

        @builtins.property
        def text_transformation(self) -> str:
            """``CfnByteMatchSet.ByteMatchTupleProperty.TextTransformation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples.html#cfn-waf-bytematchset-bytematchtuples-texttransformation
            """
            return self._values.get('text_transformation')

        @builtins.property
        def target_string(self) -> typing.Optional[str]:
            """``CfnByteMatchSet.ByteMatchTupleProperty.TargetString``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples.html#cfn-waf-bytematchset-bytematchtuples-targetstring
            """
            return self._values.get('target_string')

        @builtins.property
        def target_string_base64(self) -> typing.Optional[str]:
            """``CfnByteMatchSet.ByteMatchTupleProperty.TargetStringBase64``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples.html#cfn-waf-bytematchset-bytematchtuples-targetstringbase64
            """
            return self._values.get('target_string_base64')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ByteMatchTupleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnByteMatchSet.FieldToMatchProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'data': 'data'})
    class FieldToMatchProperty():
        def __init__(self, *, type: str, data: typing.Optional[str]=None) -> None:
            """
            :param type: ``CfnByteMatchSet.FieldToMatchProperty.Type``.
            :param data: ``CfnByteMatchSet.FieldToMatchProperty.Data``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples-fieldtomatch.html
            """
            self._values = {
                'type': type,
            }
            if data is not None: self._values["data"] = data

        @builtins.property
        def type(self) -> str:
            """``CfnByteMatchSet.FieldToMatchProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples-fieldtomatch.html#cfn-waf-bytematchset-bytematchtuples-fieldtomatch-type
            """
            return self._values.get('type')

        @builtins.property
        def data(self) -> typing.Optional[str]:
            """``CfnByteMatchSet.FieldToMatchProperty.Data``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples-fieldtomatch.html#cfn-waf-bytematchset-bytematchtuples-fieldtomatch-data
            """
            return self._values.get('data')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'FieldToMatchProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnByteMatchSetProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'byte_match_tuples': 'byteMatchTuples'})
class CfnByteMatchSetProps():
    def __init__(self, *, name: str, byte_match_tuples: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnByteMatchSet.ByteMatchTupleProperty"]]]]=None) -> None:
        """Properties for defining a ``AWS::WAF::ByteMatchSet``.

        :param name: ``AWS::WAF::ByteMatchSet.Name``.
        :param byte_match_tuples: ``AWS::WAF::ByteMatchSet.ByteMatchTuples``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-bytematchset.html
        """
        self._values = {
            'name': name,
        }
        if byte_match_tuples is not None: self._values["byte_match_tuples"] = byte_match_tuples

    @builtins.property
    def name(self) -> str:
        """``AWS::WAF::ByteMatchSet.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-bytematchset.html#cfn-waf-bytematchset-name
        """
        return self._values.get('name')

    @builtins.property
    def byte_match_tuples(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnByteMatchSet.ByteMatchTupleProperty"]]]]:
        """``AWS::WAF::ByteMatchSet.ByteMatchTuples``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-bytematchset.html#cfn-waf-bytematchset-bytematchtuples
        """
        return self._values.get('byte_match_tuples')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnByteMatchSetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnIPSet(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-waf.CfnIPSet"):
    """A CloudFormation ``AWS::WAF::IPSet``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-ipset.html
    cloudformationResource:
    :cloudformationResource:: AWS::WAF::IPSet
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, name: str, ip_set_descriptors: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "IPSetDescriptorProperty"]]]]=None) -> None:
        """Create a new ``AWS::WAF::IPSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::WAF::IPSet.Name``.
        :param ip_set_descriptors: ``AWS::WAF::IPSet.IPSetDescriptors``.
        """
        props = CfnIPSetProps(name=name, ip_set_descriptors=ip_set_descriptors)

        jsii.create(CfnIPSet, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnIPSet":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::WAF::IPSet.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-ipset.html#cfn-waf-ipset-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="ipSetDescriptors")
    def ip_set_descriptors(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "IPSetDescriptorProperty"]]]]:
        """``AWS::WAF::IPSet.IPSetDescriptors``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-ipset.html#cfn-waf-ipset-ipsetdescriptors
        """
        return jsii.get(self, "ipSetDescriptors")

    @ip_set_descriptors.setter
    def ip_set_descriptors(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "IPSetDescriptorProperty"]]]]) -> None:
        jsii.set(self, "ipSetDescriptors", value)

    @jsii.interface(jsii_type="@aws-cdk/aws-waf.CfnIPSet.IPSetDescriptorProperty")
    class IPSetDescriptorProperty(jsii.compat.Protocol):
        """
        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-ipset-ipsetdescriptors.html
        """
        @builtins.staticmethod
        def __jsii_proxy_class__():
            return _IPSetDescriptorPropertyProxy

        @builtins.property
        @jsii.member(jsii_name="type")
        def type(self) -> str:
            """``CfnIPSet.IPSetDescriptorProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-ipset-ipsetdescriptors.html#cfn-waf-ipset-ipsetdescriptors-type
            """
            ...

        @builtins.property
        @jsii.member(jsii_name="value")
        def value(self) -> str:
            """``CfnIPSet.IPSetDescriptorProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-ipset-ipsetdescriptors.html#cfn-waf-ipset-ipsetdescriptors-value
            """
            ...


    class _IPSetDescriptorPropertyProxy():
        """
        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-ipset-ipsetdescriptors.html
        """
        __jsii_type__ = "@aws-cdk/aws-waf.CfnIPSet.IPSetDescriptorProperty"
        @builtins.property
        @jsii.member(jsii_name="type")
        def type(self) -> str:
            """``CfnIPSet.IPSetDescriptorProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-ipset-ipsetdescriptors.html#cfn-waf-ipset-ipsetdescriptors-type
            """
            return jsii.get(self, "type")

        @builtins.property
        @jsii.member(jsii_name="value")
        def value(self) -> str:
            """``CfnIPSet.IPSetDescriptorProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-ipset-ipsetdescriptors.html#cfn-waf-ipset-ipsetdescriptors-value
            """
            return jsii.get(self, "value")



@jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnIPSetProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'ip_set_descriptors': 'ipSetDescriptors'})
class CfnIPSetProps():
    def __init__(self, *, name: str, ip_set_descriptors: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnIPSet.IPSetDescriptorProperty"]]]]=None) -> None:
        """Properties for defining a ``AWS::WAF::IPSet``.

        :param name: ``AWS::WAF::IPSet.Name``.
        :param ip_set_descriptors: ``AWS::WAF::IPSet.IPSetDescriptors``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-ipset.html
        """
        self._values = {
            'name': name,
        }
        if ip_set_descriptors is not None: self._values["ip_set_descriptors"] = ip_set_descriptors

    @builtins.property
    def name(self) -> str:
        """``AWS::WAF::IPSet.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-ipset.html#cfn-waf-ipset-name
        """
        return self._values.get('name')

    @builtins.property
    def ip_set_descriptors(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnIPSet.IPSetDescriptorProperty"]]]]:
        """``AWS::WAF::IPSet.IPSetDescriptors``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-ipset.html#cfn-waf-ipset-ipsetdescriptors
        """
        return self._values.get('ip_set_descriptors')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnIPSetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRule(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-waf.CfnRule"):
    """A CloudFormation ``AWS::WAF::Rule``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-rule.html
    cloudformationResource:
    :cloudformationResource:: AWS::WAF::Rule
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, metric_name: str, name: str, predicates: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "PredicateProperty"]]]]=None) -> None:
        """Create a new ``AWS::WAF::Rule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param metric_name: ``AWS::WAF::Rule.MetricName``.
        :param name: ``AWS::WAF::Rule.Name``.
        :param predicates: ``AWS::WAF::Rule.Predicates``.
        """
        props = CfnRuleProps(metric_name=metric_name, name=name, predicates=predicates)

        jsii.create(CfnRule, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnRule":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> str:
        """``AWS::WAF::Rule.MetricName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-rule.html#cfn-waf-rule-metricname
        """
        return jsii.get(self, "metricName")

    @metric_name.setter
    def metric_name(self, value: str) -> None:
        jsii.set(self, "metricName", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::WAF::Rule.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-rule.html#cfn-waf-rule-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="predicates")
    def predicates(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "PredicateProperty"]]]]:
        """``AWS::WAF::Rule.Predicates``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-rule.html#cfn-waf-rule-predicates
        """
        return jsii.get(self, "predicates")

    @predicates.setter
    def predicates(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "PredicateProperty"]]]]) -> None:
        jsii.set(self, "predicates", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnRule.PredicateProperty", jsii_struct_bases=[], name_mapping={'data_id': 'dataId', 'negated': 'negated', 'type': 'type'})
    class PredicateProperty():
        def __init__(self, *, data_id: str, negated: typing.Union[bool, aws_cdk.core.IResolvable], type: str) -> None:
            """
            :param data_id: ``CfnRule.PredicateProperty.DataId``.
            :param negated: ``CfnRule.PredicateProperty.Negated``.
            :param type: ``CfnRule.PredicateProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-rule-predicates.html
            """
            self._values = {
                'data_id': data_id,
                'negated': negated,
                'type': type,
            }

        @builtins.property
        def data_id(self) -> str:
            """``CfnRule.PredicateProperty.DataId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-rule-predicates.html#cfn-waf-rule-predicates-dataid
            """
            return self._values.get('data_id')

        @builtins.property
        def negated(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
            """``CfnRule.PredicateProperty.Negated``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-rule-predicates.html#cfn-waf-rule-predicates-negated
            """
            return self._values.get('negated')

        @builtins.property
        def type(self) -> str:
            """``CfnRule.PredicateProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-rule-predicates.html#cfn-waf-rule-predicates-type
            """
            return self._values.get('type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PredicateProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnRuleProps", jsii_struct_bases=[], name_mapping={'metric_name': 'metricName', 'name': 'name', 'predicates': 'predicates'})
class CfnRuleProps():
    def __init__(self, *, metric_name: str, name: str, predicates: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRule.PredicateProperty"]]]]=None) -> None:
        """Properties for defining a ``AWS::WAF::Rule``.

        :param metric_name: ``AWS::WAF::Rule.MetricName``.
        :param name: ``AWS::WAF::Rule.Name``.
        :param predicates: ``AWS::WAF::Rule.Predicates``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-rule.html
        """
        self._values = {
            'metric_name': metric_name,
            'name': name,
        }
        if predicates is not None: self._values["predicates"] = predicates

    @builtins.property
    def metric_name(self) -> str:
        """``AWS::WAF::Rule.MetricName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-rule.html#cfn-waf-rule-metricname
        """
        return self._values.get('metric_name')

    @builtins.property
    def name(self) -> str:
        """``AWS::WAF::Rule.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-rule.html#cfn-waf-rule-name
        """
        return self._values.get('name')

    @builtins.property
    def predicates(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnRule.PredicateProperty"]]]]:
        """``AWS::WAF::Rule.Predicates``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-rule.html#cfn-waf-rule-predicates
        """
        return self._values.get('predicates')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRuleProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnSizeConstraintSet(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-waf.CfnSizeConstraintSet"):
    """A CloudFormation ``AWS::WAF::SizeConstraintSet``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sizeconstraintset.html
    cloudformationResource:
    :cloudformationResource:: AWS::WAF::SizeConstraintSet
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, name: str, size_constraints: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "SizeConstraintProperty"]]]) -> None:
        """Create a new ``AWS::WAF::SizeConstraintSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::WAF::SizeConstraintSet.Name``.
        :param size_constraints: ``AWS::WAF::SizeConstraintSet.SizeConstraints``.
        """
        props = CfnSizeConstraintSetProps(name=name, size_constraints=size_constraints)

        jsii.create(CfnSizeConstraintSet, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnSizeConstraintSet":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::WAF::SizeConstraintSet.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sizeconstraintset.html#cfn-waf-sizeconstraintset-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="sizeConstraints")
    def size_constraints(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "SizeConstraintProperty"]]]:
        """``AWS::WAF::SizeConstraintSet.SizeConstraints``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sizeconstraintset.html#cfn-waf-sizeconstraintset-sizeconstraints
        """
        return jsii.get(self, "sizeConstraints")

    @size_constraints.setter
    def size_constraints(self, value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "SizeConstraintProperty"]]]) -> None:
        jsii.set(self, "sizeConstraints", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnSizeConstraintSet.FieldToMatchProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'data': 'data'})
    class FieldToMatchProperty():
        def __init__(self, *, type: str, data: typing.Optional[str]=None) -> None:
            """
            :param type: ``CfnSizeConstraintSet.FieldToMatchProperty.Type``.
            :param data: ``CfnSizeConstraintSet.FieldToMatchProperty.Data``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint-fieldtomatch.html
            """
            self._values = {
                'type': type,
            }
            if data is not None: self._values["data"] = data

        @builtins.property
        def type(self) -> str:
            """``CfnSizeConstraintSet.FieldToMatchProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint-fieldtomatch.html#cfn-waf-sizeconstraintset-sizeconstraint-fieldtomatch-type
            """
            return self._values.get('type')

        @builtins.property
        def data(self) -> typing.Optional[str]:
            """``CfnSizeConstraintSet.FieldToMatchProperty.Data``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint-fieldtomatch.html#cfn-waf-sizeconstraintset-sizeconstraint-fieldtomatch-data
            """
            return self._values.get('data')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'FieldToMatchProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnSizeConstraintSet.SizeConstraintProperty", jsii_struct_bases=[], name_mapping={'comparison_operator': 'comparisonOperator', 'field_to_match': 'fieldToMatch', 'size': 'size', 'text_transformation': 'textTransformation'})
    class SizeConstraintProperty():
        def __init__(self, *, comparison_operator: str, field_to_match: typing.Union[aws_cdk.core.IResolvable, "CfnSizeConstraintSet.FieldToMatchProperty"], size: jsii.Number, text_transformation: str) -> None:
            """
            :param comparison_operator: ``CfnSizeConstraintSet.SizeConstraintProperty.ComparisonOperator``.
            :param field_to_match: ``CfnSizeConstraintSet.SizeConstraintProperty.FieldToMatch``.
            :param size: ``CfnSizeConstraintSet.SizeConstraintProperty.Size``.
            :param text_transformation: ``CfnSizeConstraintSet.SizeConstraintProperty.TextTransformation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint.html
            """
            self._values = {
                'comparison_operator': comparison_operator,
                'field_to_match': field_to_match,
                'size': size,
                'text_transformation': text_transformation,
            }

        @builtins.property
        def comparison_operator(self) -> str:
            """``CfnSizeConstraintSet.SizeConstraintProperty.ComparisonOperator``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint.html#cfn-waf-sizeconstraintset-sizeconstraint-comparisonoperator
            """
            return self._values.get('comparison_operator')

        @builtins.property
        def field_to_match(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnSizeConstraintSet.FieldToMatchProperty"]:
            """``CfnSizeConstraintSet.SizeConstraintProperty.FieldToMatch``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint.html#cfn-waf-sizeconstraintset-sizeconstraint-fieldtomatch
            """
            return self._values.get('field_to_match')

        @builtins.property
        def size(self) -> jsii.Number:
            """``CfnSizeConstraintSet.SizeConstraintProperty.Size``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint.html#cfn-waf-sizeconstraintset-sizeconstraint-size
            """
            return self._values.get('size')

        @builtins.property
        def text_transformation(self) -> str:
            """``CfnSizeConstraintSet.SizeConstraintProperty.TextTransformation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint.html#cfn-waf-sizeconstraintset-sizeconstraint-texttransformation
            """
            return self._values.get('text_transformation')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SizeConstraintProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnSizeConstraintSetProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'size_constraints': 'sizeConstraints'})
class CfnSizeConstraintSetProps():
    def __init__(self, *, name: str, size_constraints: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnSizeConstraintSet.SizeConstraintProperty"]]]) -> None:
        """Properties for defining a ``AWS::WAF::SizeConstraintSet``.

        :param name: ``AWS::WAF::SizeConstraintSet.Name``.
        :param size_constraints: ``AWS::WAF::SizeConstraintSet.SizeConstraints``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sizeconstraintset.html
        """
        self._values = {
            'name': name,
            'size_constraints': size_constraints,
        }

    @builtins.property
    def name(self) -> str:
        """``AWS::WAF::SizeConstraintSet.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sizeconstraintset.html#cfn-waf-sizeconstraintset-name
        """
        return self._values.get('name')

    @builtins.property
    def size_constraints(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnSizeConstraintSet.SizeConstraintProperty"]]]:
        """``AWS::WAF::SizeConstraintSet.SizeConstraints``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sizeconstraintset.html#cfn-waf-sizeconstraintset-sizeconstraints
        """
        return self._values.get('size_constraints')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnSizeConstraintSetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnSqlInjectionMatchSet(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-waf.CfnSqlInjectionMatchSet"):
    """A CloudFormation ``AWS::WAF::SqlInjectionMatchSet``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sqlinjectionmatchset.html
    cloudformationResource:
    :cloudformationResource:: AWS::WAF::SqlInjectionMatchSet
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, name: str, sql_injection_match_tuples: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "SqlInjectionMatchTupleProperty"]]]]=None) -> None:
        """Create a new ``AWS::WAF::SqlInjectionMatchSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::WAF::SqlInjectionMatchSet.Name``.
        :param sql_injection_match_tuples: ``AWS::WAF::SqlInjectionMatchSet.SqlInjectionMatchTuples``.
        """
        props = CfnSqlInjectionMatchSetProps(name=name, sql_injection_match_tuples=sql_injection_match_tuples)

        jsii.create(CfnSqlInjectionMatchSet, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnSqlInjectionMatchSet":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::WAF::SqlInjectionMatchSet.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sqlinjectionmatchset.html#cfn-waf-sqlinjectionmatchset-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="sqlInjectionMatchTuples")
    def sql_injection_match_tuples(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "SqlInjectionMatchTupleProperty"]]]]:
        """``AWS::WAF::SqlInjectionMatchSet.SqlInjectionMatchTuples``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sqlinjectionmatchset.html#cfn-waf-sqlinjectionmatchset-sqlinjectionmatchtuples
        """
        return jsii.get(self, "sqlInjectionMatchTuples")

    @sql_injection_match_tuples.setter
    def sql_injection_match_tuples(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "SqlInjectionMatchTupleProperty"]]]]) -> None:
        jsii.set(self, "sqlInjectionMatchTuples", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnSqlInjectionMatchSet.FieldToMatchProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'data': 'data'})
    class FieldToMatchProperty():
        def __init__(self, *, type: str, data: typing.Optional[str]=None) -> None:
            """
            :param type: ``CfnSqlInjectionMatchSet.FieldToMatchProperty.Type``.
            :param data: ``CfnSqlInjectionMatchSet.FieldToMatchProperty.Data``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples-fieldtomatch.html
            """
            self._values = {
                'type': type,
            }
            if data is not None: self._values["data"] = data

        @builtins.property
        def type(self) -> str:
            """``CfnSqlInjectionMatchSet.FieldToMatchProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples-fieldtomatch.html#cfn-waf-sizeconstraintset-sizeconstraint-fieldtomatch-type
            """
            return self._values.get('type')

        @builtins.property
        def data(self) -> typing.Optional[str]:
            """``CfnSqlInjectionMatchSet.FieldToMatchProperty.Data``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples-fieldtomatch.html#cfn-waf-sizeconstraintset-sizeconstraint-fieldtomatch-data
            """
            return self._values.get('data')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'FieldToMatchProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty", jsii_struct_bases=[], name_mapping={'field_to_match': 'fieldToMatch', 'text_transformation': 'textTransformation'})
    class SqlInjectionMatchTupleProperty():
        def __init__(self, *, field_to_match: typing.Union[aws_cdk.core.IResolvable, "CfnSqlInjectionMatchSet.FieldToMatchProperty"], text_transformation: str) -> None:
            """
            :param field_to_match: ``CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty.FieldToMatch``.
            :param text_transformation: ``CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty.TextTransformation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sqlinjectionmatchset-sqlinjectionmatchtuples.html
            """
            self._values = {
                'field_to_match': field_to_match,
                'text_transformation': text_transformation,
            }

        @builtins.property
        def field_to_match(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnSqlInjectionMatchSet.FieldToMatchProperty"]:
            """``CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty.FieldToMatch``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sqlinjectionmatchset-sqlinjectionmatchtuples.html#cfn-waf-sqlinjectionmatchset-sqlinjectionmatchtuples-fieldtomatch
            """
            return self._values.get('field_to_match')

        @builtins.property
        def text_transformation(self) -> str:
            """``CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty.TextTransformation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sqlinjectionmatchset-sqlinjectionmatchtuples.html#cfn-waf-sqlinjectionmatchset-sqlinjectionmatchtuples-texttransformation
            """
            return self._values.get('text_transformation')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SqlInjectionMatchTupleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnSqlInjectionMatchSetProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'sql_injection_match_tuples': 'sqlInjectionMatchTuples'})
class CfnSqlInjectionMatchSetProps():
    def __init__(self, *, name: str, sql_injection_match_tuples: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty"]]]]=None) -> None:
        """Properties for defining a ``AWS::WAF::SqlInjectionMatchSet``.

        :param name: ``AWS::WAF::SqlInjectionMatchSet.Name``.
        :param sql_injection_match_tuples: ``AWS::WAF::SqlInjectionMatchSet.SqlInjectionMatchTuples``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sqlinjectionmatchset.html
        """
        self._values = {
            'name': name,
        }
        if sql_injection_match_tuples is not None: self._values["sql_injection_match_tuples"] = sql_injection_match_tuples

    @builtins.property
    def name(self) -> str:
        """``AWS::WAF::SqlInjectionMatchSet.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sqlinjectionmatchset.html#cfn-waf-sqlinjectionmatchset-name
        """
        return self._values.get('name')

    @builtins.property
    def sql_injection_match_tuples(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty"]]]]:
        """``AWS::WAF::SqlInjectionMatchSet.SqlInjectionMatchTuples``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sqlinjectionmatchset.html#cfn-waf-sqlinjectionmatchset-sqlinjectionmatchtuples
        """
        return self._values.get('sql_injection_match_tuples')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnSqlInjectionMatchSetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnWebACL(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-waf.CfnWebACL"):
    """A CloudFormation ``AWS::WAF::WebACL``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html
    cloudformationResource:
    :cloudformationResource:: AWS::WAF::WebACL
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, default_action: typing.Union["WafActionProperty", aws_cdk.core.IResolvable], metric_name: str, name: str, rules: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "ActivatedRuleProperty"]]]]=None) -> None:
        """Create a new ``AWS::WAF::WebACL``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param default_action: ``AWS::WAF::WebACL.DefaultAction``.
        :param metric_name: ``AWS::WAF::WebACL.MetricName``.
        :param name: ``AWS::WAF::WebACL.Name``.
        :param rules: ``AWS::WAF::WebACL.Rules``.
        """
        props = CfnWebACLProps(default_action=default_action, metric_name=metric_name, name=name, rules=rules)

        jsii.create(CfnWebACL, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnWebACL":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="defaultAction")
    def default_action(self) -> typing.Union["WafActionProperty", aws_cdk.core.IResolvable]:
        """``AWS::WAF::WebACL.DefaultAction``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html#cfn-waf-webacl-defaultaction
        """
        return jsii.get(self, "defaultAction")

    @default_action.setter
    def default_action(self, value: typing.Union["WafActionProperty", aws_cdk.core.IResolvable]) -> None:
        jsii.set(self, "defaultAction", value)

    @builtins.property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> str:
        """``AWS::WAF::WebACL.MetricName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html#cfn-waf-webacl-metricname
        """
        return jsii.get(self, "metricName")

    @metric_name.setter
    def metric_name(self, value: str) -> None:
        jsii.set(self, "metricName", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::WAF::WebACL.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html#cfn-waf-webacl-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "ActivatedRuleProperty"]]]]:
        """``AWS::WAF::WebACL.Rules``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html#cfn-waf-webacl-rules
        """
        return jsii.get(self, "rules")

    @rules.setter
    def rules(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "ActivatedRuleProperty"]]]]) -> None:
        jsii.set(self, "rules", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnWebACL.ActivatedRuleProperty", jsii_struct_bases=[], name_mapping={'priority': 'priority', 'rule_id': 'ruleId', 'action': 'action'})
    class ActivatedRuleProperty():
        def __init__(self, *, priority: jsii.Number, rule_id: str, action: typing.Optional[typing.Union["CfnWebACL.WafActionProperty", aws_cdk.core.IResolvable]]=None) -> None:
            """
            :param priority: ``CfnWebACL.ActivatedRuleProperty.Priority``.
            :param rule_id: ``CfnWebACL.ActivatedRuleProperty.RuleId``.
            :param action: ``CfnWebACL.ActivatedRuleProperty.Action``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-webacl-rules.html
            """
            self._values = {
                'priority': priority,
                'rule_id': rule_id,
            }
            if action is not None: self._values["action"] = action

        @builtins.property
        def priority(self) -> jsii.Number:
            """``CfnWebACL.ActivatedRuleProperty.Priority``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-webacl-rules.html#cfn-waf-webacl-rules-priority
            """
            return self._values.get('priority')

        @builtins.property
        def rule_id(self) -> str:
            """``CfnWebACL.ActivatedRuleProperty.RuleId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-webacl-rules.html#cfn-waf-webacl-rules-ruleid
            """
            return self._values.get('rule_id')

        @builtins.property
        def action(self) -> typing.Optional[typing.Union["CfnWebACL.WafActionProperty", aws_cdk.core.IResolvable]]:
            """``CfnWebACL.ActivatedRuleProperty.Action``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-webacl-rules.html#cfn-waf-webacl-rules-action
            """
            return self._values.get('action')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ActivatedRuleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnWebACL.WafActionProperty", jsii_struct_bases=[], name_mapping={'type': 'type'})
    class WafActionProperty():
        def __init__(self, *, type: str) -> None:
            """
            :param type: ``CfnWebACL.WafActionProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-webacl-action.html
            """
            self._values = {
                'type': type,
            }

        @builtins.property
        def type(self) -> str:
            """``CfnWebACL.WafActionProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-webacl-action.html#cfn-waf-webacl-action-type
            """
            return self._values.get('type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'WafActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnWebACLProps", jsii_struct_bases=[], name_mapping={'default_action': 'defaultAction', 'metric_name': 'metricName', 'name': 'name', 'rules': 'rules'})
class CfnWebACLProps():
    def __init__(self, *, default_action: typing.Union["CfnWebACL.WafActionProperty", aws_cdk.core.IResolvable], metric_name: str, name: str, rules: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnWebACL.ActivatedRuleProperty"]]]]=None) -> None:
        """Properties for defining a ``AWS::WAF::WebACL``.

        :param default_action: ``AWS::WAF::WebACL.DefaultAction``.
        :param metric_name: ``AWS::WAF::WebACL.MetricName``.
        :param name: ``AWS::WAF::WebACL.Name``.
        :param rules: ``AWS::WAF::WebACL.Rules``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html
        """
        self._values = {
            'default_action': default_action,
            'metric_name': metric_name,
            'name': name,
        }
        if rules is not None: self._values["rules"] = rules

    @builtins.property
    def default_action(self) -> typing.Union["CfnWebACL.WafActionProperty", aws_cdk.core.IResolvable]:
        """``AWS::WAF::WebACL.DefaultAction``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html#cfn-waf-webacl-defaultaction
        """
        return self._values.get('default_action')

    @builtins.property
    def metric_name(self) -> str:
        """``AWS::WAF::WebACL.MetricName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html#cfn-waf-webacl-metricname
        """
        return self._values.get('metric_name')

    @builtins.property
    def name(self) -> str:
        """``AWS::WAF::WebACL.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html#cfn-waf-webacl-name
        """
        return self._values.get('name')

    @builtins.property
    def rules(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnWebACL.ActivatedRuleProperty"]]]]:
        """``AWS::WAF::WebACL.Rules``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html#cfn-waf-webacl-rules
        """
        return self._values.get('rules')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnWebACLProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnXssMatchSet(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-waf.CfnXssMatchSet"):
    """A CloudFormation ``AWS::WAF::XssMatchSet``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-xssmatchset.html
    cloudformationResource:
    :cloudformationResource:: AWS::WAF::XssMatchSet
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, name: str, xss_match_tuples: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "XssMatchTupleProperty"]]]) -> None:
        """Create a new ``AWS::WAF::XssMatchSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::WAF::XssMatchSet.Name``.
        :param xss_match_tuples: ``AWS::WAF::XssMatchSet.XssMatchTuples``.
        """
        props = CfnXssMatchSetProps(name=name, xss_match_tuples=xss_match_tuples)

        jsii.create(CfnXssMatchSet, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnXssMatchSet":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::WAF::XssMatchSet.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-xssmatchset.html#cfn-waf-xssmatchset-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="xssMatchTuples")
    def xss_match_tuples(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "XssMatchTupleProperty"]]]:
        """``AWS::WAF::XssMatchSet.XssMatchTuples``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-xssmatchset.html#cfn-waf-xssmatchset-xssmatchtuples
        """
        return jsii.get(self, "xssMatchTuples")

    @xss_match_tuples.setter
    def xss_match_tuples(self, value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "XssMatchTupleProperty"]]]) -> None:
        jsii.set(self, "xssMatchTuples", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnXssMatchSet.FieldToMatchProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'data': 'data'})
    class FieldToMatchProperty():
        def __init__(self, *, type: str, data: typing.Optional[str]=None) -> None:
            """
            :param type: ``CfnXssMatchSet.FieldToMatchProperty.Type``.
            :param data: ``CfnXssMatchSet.FieldToMatchProperty.Data``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-xssmatchset-xssmatchtuple-fieldtomatch.html
            """
            self._values = {
                'type': type,
            }
            if data is not None: self._values["data"] = data

        @builtins.property
        def type(self) -> str:
            """``CfnXssMatchSet.FieldToMatchProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-xssmatchset-xssmatchtuple-fieldtomatch.html#cfn-waf-xssmatchset-xssmatchtuple-fieldtomatch-type
            """
            return self._values.get('type')

        @builtins.property
        def data(self) -> typing.Optional[str]:
            """``CfnXssMatchSet.FieldToMatchProperty.Data``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-xssmatchset-xssmatchtuple-fieldtomatch.html#cfn-waf-xssmatchset-xssmatchtuple-fieldtomatch-data
            """
            return self._values.get('data')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'FieldToMatchProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnXssMatchSet.XssMatchTupleProperty", jsii_struct_bases=[], name_mapping={'field_to_match': 'fieldToMatch', 'text_transformation': 'textTransformation'})
    class XssMatchTupleProperty():
        def __init__(self, *, field_to_match: typing.Union[aws_cdk.core.IResolvable, "CfnXssMatchSet.FieldToMatchProperty"], text_transformation: str) -> None:
            """
            :param field_to_match: ``CfnXssMatchSet.XssMatchTupleProperty.FieldToMatch``.
            :param text_transformation: ``CfnXssMatchSet.XssMatchTupleProperty.TextTransformation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-xssmatchset-xssmatchtuple.html
            """
            self._values = {
                'field_to_match': field_to_match,
                'text_transformation': text_transformation,
            }

        @builtins.property
        def field_to_match(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnXssMatchSet.FieldToMatchProperty"]:
            """``CfnXssMatchSet.XssMatchTupleProperty.FieldToMatch``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-xssmatchset-xssmatchtuple.html#cfn-waf-xssmatchset-xssmatchtuple-fieldtomatch
            """
            return self._values.get('field_to_match')

        @builtins.property
        def text_transformation(self) -> str:
            """``CfnXssMatchSet.XssMatchTupleProperty.TextTransformation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-xssmatchset-xssmatchtuple.html#cfn-waf-xssmatchset-xssmatchtuple-texttransformation
            """
            return self._values.get('text_transformation')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'XssMatchTupleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-waf.CfnXssMatchSetProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'xss_match_tuples': 'xssMatchTuples'})
class CfnXssMatchSetProps():
    def __init__(self, *, name: str, xss_match_tuples: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnXssMatchSet.XssMatchTupleProperty"]]]) -> None:
        """Properties for defining a ``AWS::WAF::XssMatchSet``.

        :param name: ``AWS::WAF::XssMatchSet.Name``.
        :param xss_match_tuples: ``AWS::WAF::XssMatchSet.XssMatchTuples``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-xssmatchset.html
        """
        self._values = {
            'name': name,
            'xss_match_tuples': xss_match_tuples,
        }

    @builtins.property
    def name(self) -> str:
        """``AWS::WAF::XssMatchSet.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-xssmatchset.html#cfn-waf-xssmatchset-name
        """
        return self._values.get('name')

    @builtins.property
    def xss_match_tuples(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnXssMatchSet.XssMatchTupleProperty"]]]:
        """``AWS::WAF::XssMatchSet.XssMatchTuples``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-xssmatchset.html#cfn-waf-xssmatchset-xssmatchtuples
        """
        return self._values.get('xss_match_tuples')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnXssMatchSetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnByteMatchSet",
    "CfnByteMatchSetProps",
    "CfnIPSet",
    "CfnIPSetProps",
    "CfnRule",
    "CfnRuleProps",
    "CfnSizeConstraintSet",
    "CfnSizeConstraintSetProps",
    "CfnSqlInjectionMatchSet",
    "CfnSqlInjectionMatchSetProps",
    "CfnWebACL",
    "CfnWebACLProps",
    "CfnXssMatchSet",
    "CfnXssMatchSetProps",
]

publication.publish()
