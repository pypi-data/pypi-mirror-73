"""
# cdktf

cdktf is a framework for defining cloud infrastructure using Terraform providers and modules. It allows for
users to define infrastructure resources using higher-level programming languages.

## Build

Install dependencies

```bash
yarn install
```

Build the package

```bash
yarn build
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

import constructs


class App(constructs.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdktf.App"):
    """Represents a cdktf application.

    stability
    :stability: experimental
    """
    def __init__(self, *, outdir: typing.Optional[str]=None, stack_traces: typing.Optional[bool]=None) -> None:
        """Defines an app.

        :param outdir: The directory to output Terraform resources. Default: - CDKTF_OUTDIR if defined, otherwise "cdktf.out"
        :param stack_traces: 

        stability
        :stability: experimental
        """
        options = AppOptions(outdir=outdir, stack_traces=stack_traces)

        jsii.create(App, self, [options])

    @jsii.member(jsii_name="synth")
    def synth(self) -> None:
        """Synthesizes all resources to the output directory.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synth", [])

    @builtins.property
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> str:
        """The output directory into which resources will be synthesized.

        stability
        :stability: experimental
        """
        return jsii.get(self, "outdir")


@jsii.data_type(jsii_type="cdktf.AppOptions", jsii_struct_bases=[], name_mapping={'outdir': 'outdir', 'stack_traces': 'stackTraces'})
class AppOptions():
    def __init__(self, *, outdir: typing.Optional[str]=None, stack_traces: typing.Optional[bool]=None) -> None:
        """
        :param outdir: The directory to output Terraform resources. Default: - CDKTF_OUTDIR if defined, otherwise "cdktf.out"
        :param stack_traces: 

        stability
        :stability: experimental
        """
        self._values = {
        }
        if outdir is not None: self._values["outdir"] = outdir
        if stack_traces is not None: self._values["stack_traces"] = stack_traces

    @builtins.property
    def outdir(self) -> typing.Optional[str]:
        """The directory to output Terraform resources.

        default
        :default: - CDKTF_OUTDIR if defined, otherwise "cdktf.out"

        stability
        :stability: experimental
        """
        return self._values.get('outdir')

    @builtins.property
    def stack_traces(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('stack_traces')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AppOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class BooleanMap(metaclass=jsii.JSIIMeta, jsii_type="cdktf.BooleanMap"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, terraform_resource: "ITerraformResource", terraform_attribute: str) -> None:
        """
        :param terraform_resource: -
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        jsii.create(BooleanMap, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="lookup")
    def lookup(self, key: str) -> bool:
        """
        :param key: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "lookup", [key])

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformAttribute")

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: str) -> None:
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> "ITerraformResource":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformResource")

    @_terraform_resource.setter
    def _terraform_resource(self, value: "ITerraformResource") -> None:
        jsii.set(self, "terraformResource", value)


class ComplexComputedList(metaclass=jsii.JSIIMeta, jsii_type="cdktf.ComplexComputedList"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, terraform_resource: "ITerraformResource", terraform_attribute: str, index: str) -> None:
        """
        :param terraform_resource: -
        :param terraform_attribute: -
        :param index: -

        stability
        :stability: experimental
        """
        jsii.create(ComplexComputedList, self, [terraform_resource, terraform_attribute, index])

    @jsii.member(jsii_name="getBooleanAttribute")
    def get_boolean_attribute(self, terraform_attribute: str) -> bool:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getBooleanAttribute", [terraform_attribute])

    @jsii.member(jsii_name="getListAttribute")
    def get_list_attribute(self, terraform_attribute: str) -> typing.List[str]:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getListAttribute", [terraform_attribute])

    @jsii.member(jsii_name="getNumberAttribute")
    def get_number_attribute(self, terraform_attribute: str) -> jsii.Number:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getNumberAttribute", [terraform_attribute])

    @jsii.member(jsii_name="getStringAttribute")
    def get_string_attribute(self, terraform_attribute: str) -> str:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getStringAttribute", [terraform_attribute])

    @jsii.member(jsii_name="interpolationForAttribute")
    def _interpolation_for_attribute(self, property: str) -> str:
        """
        :param property: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "interpolationForAttribute", [property])

    @builtins.property
    @jsii.member(jsii_name="index")
    def _index(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "index")

    @_index.setter
    def _index(self, value: str) -> None:
        jsii.set(self, "index", value)

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformAttribute")

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: str) -> None:
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> "ITerraformResource":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformResource")

    @_terraform_resource.setter
    def _terraform_resource(self, value: "ITerraformResource") -> None:
        jsii.set(self, "terraformResource", value)


@jsii.data_type(jsii_type="cdktf.EncodingOptions", jsii_struct_bases=[], name_mapping={'display_hint': 'displayHint'})
class EncodingOptions():
    def __init__(self, *, display_hint: typing.Optional[str]=None) -> None:
        """Properties to string encodings.

        :param display_hint: A hint for the Token's purpose when stringifying it. Default: - no display hint

        stability
        :stability: experimental
        """
        self._values = {
        }
        if display_hint is not None: self._values["display_hint"] = display_hint

    @builtins.property
    def display_hint(self) -> typing.Optional[str]:
        """A hint for the Token's purpose when stringifying it.

        default
        :default: - no display hint

        stability
        :stability: experimental
        """
        return self._values.get('display_hint')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EncodingOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="cdktf.IAnyProducer")
class IAnyProducer(jsii.compat.Protocol):
    """Interface for lazy untyped value producers.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAnyProducerProxy

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Any:
        """Produce the value.

        :param context: -

        stability
        :stability: experimental
        """
        ...


class _IAnyProducerProxy():
    """Interface for lazy untyped value producers.

    stability
    :stability: experimental
    """
    __jsii_type__ = "cdktf.IAnyProducer"
    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Any:
        """Produce the value.

        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "produce", [context])


@jsii.interface(jsii_type="cdktf.IFragmentConcatenator")
class IFragmentConcatenator(jsii.compat.Protocol):
    """Function used to concatenate symbols in the target document language.

    Interface so it could potentially be exposed over jsii.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IFragmentConcatenatorProxy

    @jsii.member(jsii_name="join")
    def join(self, left: typing.Any, right: typing.Any) -> typing.Any:
        """Join the fragment on the left and on the right.

        :param left: -
        :param right: -

        stability
        :stability: experimental
        """
        ...


class _IFragmentConcatenatorProxy():
    """Function used to concatenate symbols in the target document language.

    Interface so it could potentially be exposed over jsii.

    stability
    :stability: experimental
    """
    __jsii_type__ = "cdktf.IFragmentConcatenator"
    @jsii.member(jsii_name="join")
    def join(self, left: typing.Any, right: typing.Any) -> typing.Any:
        """Join the fragment on the left and on the right.

        :param left: -
        :param right: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "join", [left, right])


@jsii.interface(jsii_type="cdktf.IListProducer")
class IListProducer(jsii.compat.Protocol):
    """Interface for lazy list producers.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IListProducerProxy

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[typing.List[str]]:
        """Produce the list value.

        :param context: -

        stability
        :stability: experimental
        """
        ...


class _IListProducerProxy():
    """Interface for lazy list producers.

    stability
    :stability: experimental
    """
    __jsii_type__ = "cdktf.IListProducer"
    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[typing.List[str]]:
        """Produce the list value.

        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "produce", [context])


@jsii.interface(jsii_type="cdktf.INumberProducer")
class INumberProducer(jsii.compat.Protocol):
    """Interface for lazy number producers.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _INumberProducerProxy

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[jsii.Number]:
        """Produce the number value.

        :param context: -

        stability
        :stability: experimental
        """
        ...


class _INumberProducerProxy():
    """Interface for lazy number producers.

    stability
    :stability: experimental
    """
    __jsii_type__ = "cdktf.INumberProducer"
    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[jsii.Number]:
        """Produce the number value.

        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "produce", [context])


@jsii.interface(jsii_type="cdktf.IPostProcessor")
class IPostProcessor(jsii.compat.Protocol):
    """A Token that can post-process the complete resolved value, after resolve() has recursed over it.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IPostProcessorProxy

    @jsii.member(jsii_name="postProcess")
    def post_process(self, input: typing.Any, context: "IResolveContext") -> typing.Any:
        """Process the completely resolved value, after full recursion/resolution has happened.

        :param input: -
        :param context: -

        stability
        :stability: experimental
        """
        ...


class _IPostProcessorProxy():
    """A Token that can post-process the complete resolved value, after resolve() has recursed over it.

    stability
    :stability: experimental
    """
    __jsii_type__ = "cdktf.IPostProcessor"
    @jsii.member(jsii_name="postProcess")
    def post_process(self, input: typing.Any, context: "IResolveContext") -> typing.Any:
        """Process the completely resolved value, after full recursion/resolution has happened.

        :param input: -
        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "postProcess", [input, context])


@jsii.interface(jsii_type="cdktf.IResolvable")
class IResolvable(jsii.compat.Protocol):
    """Interface for values that can be resolvable later.

    Tokens are special objects that participate in synthesis.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IResolvableProxy

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[str]:
        """The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="resolve")
    def resolve(self, context: "IResolveContext") -> typing.Any:
        """Produce the Token's value at resolution time.

        :param context: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Return a string representation of this resolvable object.

        Returns a reversible string representation.

        stability
        :stability: experimental
        """
        ...


class _IResolvableProxy():
    """Interface for values that can be resolvable later.

    Tokens are special objects that participate in synthesis.

    stability
    :stability: experimental
    """
    __jsii_type__ = "cdktf.IResolvable"
    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[str]:
        """The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.

        stability
        :stability: experimental
        """
        return jsii.get(self, "creationStack")

    @jsii.member(jsii_name="resolve")
    def resolve(self, context: "IResolveContext") -> typing.Any:
        """Produce the Token's value at resolution time.

        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolve", [context])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Return a string representation of this resolvable object.

        Returns a reversible string representation.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toString", [])


@jsii.interface(jsii_type="cdktf.IResolveContext")
class IResolveContext(jsii.compat.Protocol):
    """Current resolution context for tokens.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IResolveContextProxy

    @builtins.property
    @jsii.member(jsii_name="preparing")
    def preparing(self) -> bool:
        """True when we are still preparing, false if we're rendering the final output.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> constructs.IConstruct:
        """The scope from which resolution has been initiated.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="registerPostProcessor")
    def register_post_processor(self, post_processor: "IPostProcessor") -> None:
        """Use this postprocessor after the entire token structure has been resolved.

        :param post_processor: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="resolve")
    def resolve(self, x: typing.Any) -> typing.Any:
        """Resolve an inner object.

        :param x: -

        stability
        :stability: experimental
        """
        ...


class _IResolveContextProxy():
    """Current resolution context for tokens.

    stability
    :stability: experimental
    """
    __jsii_type__ = "cdktf.IResolveContext"
    @builtins.property
    @jsii.member(jsii_name="preparing")
    def preparing(self) -> bool:
        """True when we are still preparing, false if we're rendering the final output.

        stability
        :stability: experimental
        """
        return jsii.get(self, "preparing")

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> constructs.IConstruct:
        """The scope from which resolution has been initiated.

        stability
        :stability: experimental
        """
        return jsii.get(self, "scope")

    @jsii.member(jsii_name="registerPostProcessor")
    def register_post_processor(self, post_processor: "IPostProcessor") -> None:
        """Use this postprocessor after the entire token structure has been resolved.

        :param post_processor: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "registerPostProcessor", [post_processor])

    @jsii.member(jsii_name="resolve")
    def resolve(self, x: typing.Any) -> typing.Any:
        """Resolve an inner object.

        :param x: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolve", [x])


@jsii.interface(jsii_type="cdktf.IResource")
class IResource(constructs.IConstruct, jsii.compat.Protocol):
    """
    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IResourceProxy

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> "TerraformStack":
        """The stack in which this resource is defined.

        stability
        :stability: experimental
        """
        ...


class _IResourceProxy(jsii.proxy_for(constructs.IConstruct)):
    """
    stability
    :stability: experimental
    """
    __jsii_type__ = "cdktf.IResource"
    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> "TerraformStack":
        """The stack in which this resource is defined.

        stability
        :stability: experimental
        """
        return jsii.get(self, "stack")


@jsii.interface(jsii_type="cdktf.IStringProducer")
class IStringProducer(jsii.compat.Protocol):
    """Interface for lazy string producers.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IStringProducerProxy

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[str]:
        """Produce the string value.

        :param context: -

        stability
        :stability: experimental
        """
        ...


class _IStringProducerProxy():
    """Interface for lazy string producers.

    stability
    :stability: experimental
    """
    __jsii_type__ = "cdktf.IStringProducer"
    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[str]:
        """Produce the string value.

        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "produce", [context])


@jsii.interface(jsii_type="cdktf.ITerraformResource")
class ITerraformResource(jsii.compat.Protocol):
    """
    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITerraformResourceProxy

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> str:
        """
        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="friendlyUniqueId")
    def friendly_unique_id(self) -> str:
        """
        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="terraformResourceType")
    def terraform_resource_type(self) -> str:
        """
        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        ...

    @count.setter
    def count(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.Optional[typing.List[str]]:
        """
        stability
        :stability: experimental
        """
        ...

    @depends_on.setter
    def depends_on(self, value: typing.Optional[typing.List[str]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="lifecycle")
    def lifecycle(self) -> typing.Optional["TerraformResourceLifecycle"]:
        """
        stability
        :stability: experimental
        """
        ...

    @lifecycle.setter
    def lifecycle(self, value: typing.Optional["TerraformResourceLifecycle"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> typing.Optional["TerraformProvider"]:
        """
        stability
        :stability: experimental
        """
        ...

    @provider.setter
    def provider(self, value: typing.Optional["TerraformProvider"]) -> None:
        ...


class _ITerraformResourceProxy():
    """
    stability
    :stability: experimental
    """
    __jsii_type__ = "cdktf.ITerraformResource"
    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "fqn")

    @builtins.property
    @jsii.member(jsii_name="friendlyUniqueId")
    def friendly_unique_id(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "friendlyUniqueId")

    @builtins.property
    @jsii.member(jsii_name="terraformResourceType")
    def terraform_resource_type(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformResourceType")

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "count")

    @count.setter
    def count(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.Optional[typing.List[str]]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "dependsOn")

    @depends_on.setter
    def depends_on(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "dependsOn", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycle")
    def lifecycle(self) -> typing.Optional["TerraformResourceLifecycle"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "lifecycle")

    @lifecycle.setter
    def lifecycle(self, value: typing.Optional["TerraformResourceLifecycle"]) -> None:
        jsii.set(self, "lifecycle", value)

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> typing.Optional["TerraformProvider"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "provider")

    @provider.setter
    def provider(self, value: typing.Optional["TerraformProvider"]) -> None:
        jsii.set(self, "provider", value)


@jsii.interface(jsii_type="cdktf.ITokenMapper")
class ITokenMapper(jsii.compat.Protocol):
    """Interface to apply operation to tokens in a string.

    Interface so it can be exported via jsii.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITokenMapperProxy

    @jsii.member(jsii_name="mapToken")
    def map_token(self, t: "IResolvable") -> typing.Any:
        """Replace a single token.

        :param t: -

        stability
        :stability: experimental
        """
        ...


class _ITokenMapperProxy():
    """Interface to apply operation to tokens in a string.

    Interface so it can be exported via jsii.

    stability
    :stability: experimental
    """
    __jsii_type__ = "cdktf.ITokenMapper"
    @jsii.member(jsii_name="mapToken")
    def map_token(self, t: "IResolvable") -> typing.Any:
        """Replace a single token.

        :param t: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "mapToken", [t])


@jsii.interface(jsii_type="cdktf.ITokenResolver")
class ITokenResolver(jsii.compat.Protocol):
    """How to resolve tokens.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITokenResolverProxy

    @jsii.member(jsii_name="resolveList")
    def resolve_list(self, l: typing.List[str], context: "IResolveContext") -> typing.Any:
        """Resolve a tokenized list.

        :param l: -
        :param context: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="resolveString")
    def resolve_string(self, s: "TokenizedStringFragments", context: "IResolveContext") -> typing.Any:
        """Resolve a string with at least one stringified token in it.

        (May use concatenation)

        :param s: -
        :param context: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="resolveToken")
    def resolve_token(self, t: "IResolvable", context: "IResolveContext", post_processor: "IPostProcessor") -> typing.Any:
        """Resolve a single token.

        :param t: -
        :param context: -
        :param post_processor: -

        stability
        :stability: experimental
        """
        ...


class _ITokenResolverProxy():
    """How to resolve tokens.

    stability
    :stability: experimental
    """
    __jsii_type__ = "cdktf.ITokenResolver"
    @jsii.member(jsii_name="resolveList")
    def resolve_list(self, l: typing.List[str], context: "IResolveContext") -> typing.Any:
        """Resolve a tokenized list.

        :param l: -
        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveList", [l, context])

    @jsii.member(jsii_name="resolveString")
    def resolve_string(self, s: "TokenizedStringFragments", context: "IResolveContext") -> typing.Any:
        """Resolve a string with at least one stringified token in it.

        (May use concatenation)

        :param s: -
        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveString", [s, context])

    @jsii.member(jsii_name="resolveToken")
    def resolve_token(self, t: "IResolvable", context: "IResolveContext", post_processor: "IPostProcessor") -> typing.Any:
        """Resolve a single token.

        :param t: -
        :param context: -
        :param post_processor: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveToken", [t, context, post_processor])


class Lazy(metaclass=jsii.JSIIMeta, jsii_type="cdktf.Lazy"):
    """Lazily produce a value.

    Can be used to return a string, list or numeric value whose actual value
    will only be calculated later, during synthesis.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(Lazy, self, [])

    @jsii.member(jsii_name="anyValue")
    @builtins.classmethod
    def any_value(cls, producer: "IAnyProducer", *, display_hint: typing.Optional[str]=None, omit_empty_array: typing.Optional[bool]=None) -> "IResolvable":
        """Produces a lazy token from an untyped value.

        :param producer: The lazy producer.
        :param display_hint: Use the given name as a display hint. Default: - No hint
        :param omit_empty_array: If the produced value is an array and it is empty, return 'undefined' instead. Default: false

        stability
        :stability: experimental
        """
        options = LazyAnyValueOptions(display_hint=display_hint, omit_empty_array=omit_empty_array)

        return jsii.sinvoke(cls, "anyValue", [producer, options])

    @jsii.member(jsii_name="listValue")
    @builtins.classmethod
    def list_value(cls, producer: "IListProducer", *, display_hint: typing.Optional[str]=None, omit_empty: typing.Optional[bool]=None) -> typing.List[str]:
        """Returns a list-ified token for a lazy value.

        :param producer: The producer.
        :param display_hint: Use the given name as a display hint. Default: - No hint
        :param omit_empty: If the produced list is empty, return 'undefined' instead. Default: false

        stability
        :stability: experimental
        """
        options = LazyListValueOptions(display_hint=display_hint, omit_empty=omit_empty)

        return jsii.sinvoke(cls, "listValue", [producer, options])

    @jsii.member(jsii_name="numberValue")
    @builtins.classmethod
    def number_value(cls, producer: "INumberProducer") -> jsii.Number:
        """Returns a numberified token for a lazy value.

        :param producer: The producer.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "numberValue", [producer])

    @jsii.member(jsii_name="stringValue")
    @builtins.classmethod
    def string_value(cls, producer: "IStringProducer", *, display_hint: typing.Optional[str]=None) -> str:
        """Returns a stringified token for a lazy value.

        :param producer: The producer.
        :param display_hint: Use the given name as a display hint. Default: - No hint

        stability
        :stability: experimental
        """
        options = LazyStringValueOptions(display_hint=display_hint)

        return jsii.sinvoke(cls, "stringValue", [producer, options])


@jsii.data_type(jsii_type="cdktf.LazyAnyValueOptions", jsii_struct_bases=[], name_mapping={'display_hint': 'displayHint', 'omit_empty_array': 'omitEmptyArray'})
class LazyAnyValueOptions():
    def __init__(self, *, display_hint: typing.Optional[str]=None, omit_empty_array: typing.Optional[bool]=None) -> None:
        """Options for creating lazy untyped tokens.

        :param display_hint: Use the given name as a display hint. Default: - No hint
        :param omit_empty_array: If the produced value is an array and it is empty, return 'undefined' instead. Default: false

        stability
        :stability: experimental
        """
        self._values = {
        }
        if display_hint is not None: self._values["display_hint"] = display_hint
        if omit_empty_array is not None: self._values["omit_empty_array"] = omit_empty_array

    @builtins.property
    def display_hint(self) -> typing.Optional[str]:
        """Use the given name as a display hint.

        default
        :default: - No hint

        stability
        :stability: experimental
        """
        return self._values.get('display_hint')

    @builtins.property
    def omit_empty_array(self) -> typing.Optional[bool]:
        """If the produced value is an array and it is empty, return 'undefined' instead.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('omit_empty_array')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LazyAnyValueOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="cdktf.LazyListValueOptions", jsii_struct_bases=[], name_mapping={'display_hint': 'displayHint', 'omit_empty': 'omitEmpty'})
class LazyListValueOptions():
    def __init__(self, *, display_hint: typing.Optional[str]=None, omit_empty: typing.Optional[bool]=None) -> None:
        """Options for creating a lazy list token.

        :param display_hint: Use the given name as a display hint. Default: - No hint
        :param omit_empty: If the produced list is empty, return 'undefined' instead. Default: false

        stability
        :stability: experimental
        """
        self._values = {
        }
        if display_hint is not None: self._values["display_hint"] = display_hint
        if omit_empty is not None: self._values["omit_empty"] = omit_empty

    @builtins.property
    def display_hint(self) -> typing.Optional[str]:
        """Use the given name as a display hint.

        default
        :default: - No hint

        stability
        :stability: experimental
        """
        return self._values.get('display_hint')

    @builtins.property
    def omit_empty(self) -> typing.Optional[bool]:
        """If the produced list is empty, return 'undefined' instead.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('omit_empty')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LazyListValueOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="cdktf.LazyStringValueOptions", jsii_struct_bases=[], name_mapping={'display_hint': 'displayHint'})
class LazyStringValueOptions():
    def __init__(self, *, display_hint: typing.Optional[str]=None) -> None:
        """Options for creating a lazy string token.

        :param display_hint: Use the given name as a display hint. Default: - No hint

        stability
        :stability: experimental
        """
        self._values = {
        }
        if display_hint is not None: self._values["display_hint"] = display_hint

    @builtins.property
    def display_hint(self) -> typing.Optional[str]:
        """Use the given name as a display hint.

        default
        :default: - No hint

        stability
        :stability: experimental
        """
        return self._values.get('display_hint')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LazyStringValueOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class NumberMap(metaclass=jsii.JSIIMeta, jsii_type="cdktf.NumberMap"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, terraform_resource: "ITerraformResource", terraform_attribute: str) -> None:
        """
        :param terraform_resource: -
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        jsii.create(NumberMap, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="lookup")
    def lookup(self, key: str) -> jsii.Number:
        """
        :param key: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "lookup", [key])

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformAttribute")

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: str) -> None:
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> "ITerraformResource":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformResource")

    @_terraform_resource.setter
    def _terraform_resource(self, value: "ITerraformResource") -> None:
        jsii.set(self, "terraformResource", value)


@jsii.data_type(jsii_type="cdktf.ResolveOptions", jsii_struct_bases=[], name_mapping={'resolver': 'resolver', 'scope': 'scope', 'preparing': 'preparing'})
class ResolveOptions():
    def __init__(self, *, resolver: "ITokenResolver", scope: constructs.IConstruct, preparing: typing.Optional[bool]=None) -> None:
        """Options to the resolve() operation.

        NOT the same as the ResolveContext; ResolveContext is exposed to Token
        implementors and resolution hooks, whereas this struct is just to bundle
        a number of things that would otherwise be arguments to resolve() in a
        readable way.

        :param resolver: The resolver to apply to any resolvable tokens found.
        :param scope: The scope from which resolution is performed.
        :param preparing: Whether the resolution is being executed during the prepare phase or not. Default: false

        stability
        :stability: experimental
        """
        self._values = {
            'resolver': resolver,
            'scope': scope,
        }
        if preparing is not None: self._values["preparing"] = preparing

    @builtins.property
    def resolver(self) -> "ITokenResolver":
        """The resolver to apply to any resolvable tokens found.

        stability
        :stability: experimental
        """
        return self._values.get('resolver')

    @builtins.property
    def scope(self) -> constructs.IConstruct:
        """The scope from which resolution is performed.

        stability
        :stability: experimental
        """
        return self._values.get('scope')

    @builtins.property
    def preparing(self) -> typing.Optional[bool]:
        """Whether the resolution is being executed during the prepare phase or not.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('preparing')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ResolveOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IResource)
class Resource(constructs.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="cdktf.Resource"):
    """A construct which represents a resource.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ResourceProxy

    def __init__(self, scope: constructs.Construct, id: str) -> None:
        """
        :param scope: -
        :param id: -

        stability
        :stability: experimental
        """
        jsii.create(Resource, self, [scope, id])

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> "TerraformStack":
        """The stack in which this resource is defined.

        stability
        :stability: experimental
        """
        return jsii.get(self, "stack")


class _ResourceProxy(Resource):
    pass

@jsii.implements(IFragmentConcatenator)
class StringConcat(metaclass=jsii.JSIIMeta, jsii_type="cdktf.StringConcat"):
    """Converts all fragments to strings and concats those.

    Drops 'undefined's.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(StringConcat, self, [])

    @jsii.member(jsii_name="join")
    def join(self, left: typing.Any, right: typing.Any) -> typing.Any:
        """Join the fragment on the left and on the right.

        :param left: -
        :param right: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "join", [left, right])


class StringMap(metaclass=jsii.JSIIMeta, jsii_type="cdktf.StringMap"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, terraform_resource: "ITerraformResource", terraform_attribute: str) -> None:
        """
        :param terraform_resource: -
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        jsii.create(StringMap, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="lookup")
    def lookup(self, key: str) -> str:
        """
        :param key: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "lookup", [key])

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformAttribute")

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: str) -> None:
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> "ITerraformResource":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformResource")

    @_terraform_resource.setter
    def _terraform_resource(self, value: "ITerraformResource") -> None:
        jsii.set(self, "terraformResource", value)


class TerraformElement(constructs.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdktf.TerraformElement"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: constructs.Construct, id: str) -> None:
        """
        :param scope: -
        :param id: -

        stability
        :stability: experimental
        """
        jsii.create(TerraformElement, self, [scope, id])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toTerraform", [])

    @builtins.property
    @jsii.member(jsii_name="friendlyUniqueId")
    def friendly_unique_id(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "friendlyUniqueId")

    @builtins.property
    @jsii.member(jsii_name="node")
    def node(self) -> constructs.Node:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "node")

    @builtins.property
    @jsii.member(jsii_name="nodeMetadata")
    def _node_metadata(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "nodeMetadata")

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> "TerraformStack":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "stack")


@jsii.data_type(jsii_type="cdktf.TerraformElementMetadata", jsii_struct_bases=[], name_mapping={'path': 'path', 'stack_trace': 'stackTrace', 'unique_id': 'uniqueId'})
class TerraformElementMetadata():
    def __init__(self, *, path: str, stack_trace: typing.List[str], unique_id: str) -> None:
        """
        :param path: 
        :param stack_trace: 
        :param unique_id: 

        stability
        :stability: experimental
        """
        self._values = {
            'path': path,
            'stack_trace': stack_trace,
            'unique_id': unique_id,
        }

    @builtins.property
    def path(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('path')

    @builtins.property
    def stack_trace(self) -> typing.List[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('stack_trace')

    @builtins.property
    def unique_id(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('unique_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TerraformElementMetadata(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="cdktf.TerraformGeneratorMetadata", jsii_struct_bases=[], name_mapping={'provider_name': 'providerName', 'provider_version_constraint': 'providerVersionConstraint'})
class TerraformGeneratorMetadata():
    def __init__(self, *, provider_name: str, provider_version_constraint: typing.Optional[str]=None) -> None:
        """
        :param provider_name: 
        :param provider_version_constraint: 

        stability
        :stability: experimental
        """
        self._values = {
            'provider_name': provider_name,
        }
        if provider_version_constraint is not None: self._values["provider_version_constraint"] = provider_version_constraint

    @builtins.property
    def provider_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('provider_name')

    @builtins.property
    def provider_version_constraint(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('provider_version_constraint')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TerraformGeneratorMetadata(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="cdktf.TerraformMetaArguments", jsii_struct_bases=[], name_mapping={'count': 'count', 'depends_on': 'dependsOn', 'lifecycle': 'lifecycle', 'provider': 'provider'})
class TerraformMetaArguments():
    def __init__(self, *, count: typing.Optional[jsii.Number]=None, depends_on: typing.Optional[typing.List["TerraformResource"]]=None, lifecycle: typing.Optional["TerraformResourceLifecycle"]=None, provider: typing.Optional["TerraformProvider"]=None) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 

        stability
        :stability: experimental
        """
        if isinstance(lifecycle, dict): lifecycle = TerraformResourceLifecycle(**lifecycle)
        self._values = {
        }
        if count is not None: self._values["count"] = count
        if depends_on is not None: self._values["depends_on"] = depends_on
        if lifecycle is not None: self._values["lifecycle"] = lifecycle
        if provider is not None: self._values["provider"] = provider

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('count')

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List["TerraformResource"]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('depends_on')

    @builtins.property
    def lifecycle(self) -> typing.Optional["TerraformResourceLifecycle"]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('lifecycle')

    @builtins.property
    def provider(self) -> typing.Optional["TerraformProvider"]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('provider')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TerraformMetaArguments(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class TerraformModule(TerraformElement, metaclass=jsii.JSIIAbstractClass, jsii_type="cdktf.TerraformModule"):
    """
    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _TerraformModuleProxy

    def __init__(self, scope: constructs.Construct, id: str, *, source: str, version: str) -> None:
        """
        :param scope: -
        :param id: -
        :param source: 
        :param version: 

        stability
        :stability: experimental
        """
        options = TerraformModuleOptions(source=source, version=version)

        jsii.create(TerraformModule, self, [scope, id, options])

    @jsii.member(jsii_name="interpolationForOutput")
    def interpolation_for_output(self, module_output: str) -> typing.Any:
        """
        :param module_output: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "interpolationForOutput", [module_output])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toTerraform", [])

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "source")

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "version")


class _TerraformModuleProxy(TerraformModule):
    pass

@jsii.data_type(jsii_type="cdktf.TerraformModuleOptions", jsii_struct_bases=[], name_mapping={'source': 'source', 'version': 'version'})
class TerraformModuleOptions():
    def __init__(self, *, source: str, version: str) -> None:
        """
        :param source: 
        :param version: 

        stability
        :stability: experimental
        """
        self._values = {
            'source': source,
            'version': version,
        }

    @builtins.property
    def source(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('source')

    @builtins.property
    def version(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TerraformModuleOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class TerraformOutput(TerraformElement, metaclass=jsii.JSIIMeta, jsii_type="cdktf.TerraformOutput"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: constructs.Construct, id: str, *, depends_on: typing.Optional[typing.List["TerraformResource"]]=None, description: typing.Optional[str]=None, sensitive: typing.Optional[bool]=None, value: typing.Optional[typing.Union[str, jsii.Number, bool, typing.List[typing.Any], typing.Mapping[str, typing.Any]]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param depends_on: 
        :param description: 
        :param sensitive: 
        :param value: 

        stability
        :stability: experimental
        """
        config = TerraformOutputConfig(depends_on=depends_on, description=description, sensitive=sensitive, value=value)

        jsii.create(TerraformOutput, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toTerraform", [])

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.Optional[typing.List["TerraformResource"]]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "dependsOn")

    @depends_on.setter
    def depends_on(self, value: typing.Optional[typing.List["TerraformResource"]]) -> None:
        jsii.set(self, "dependsOn", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="sensitive")
    def sensitive(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "sensitive")

    @sensitive.setter
    def sensitive(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "sensitive", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Optional[typing.Union[str, jsii.Number, bool, typing.List[typing.Any], typing.Mapping[str, typing.Any]]]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "value")

    @value.setter
    def value(self, value: typing.Optional[typing.Union[str, jsii.Number, bool, typing.List[typing.Any], typing.Mapping[str, typing.Any]]]) -> None:
        jsii.set(self, "value", value)


@jsii.data_type(jsii_type="cdktf.TerraformOutputConfig", jsii_struct_bases=[], name_mapping={'depends_on': 'dependsOn', 'description': 'description', 'sensitive': 'sensitive', 'value': 'value'})
class TerraformOutputConfig():
    def __init__(self, *, depends_on: typing.Optional[typing.List["TerraformResource"]]=None, description: typing.Optional[str]=None, sensitive: typing.Optional[bool]=None, value: typing.Optional[typing.Union[str, jsii.Number, bool, typing.List[typing.Any], typing.Mapping[str, typing.Any]]]=None) -> None:
        """
        :param depends_on: 
        :param description: 
        :param sensitive: 
        :param value: 

        stability
        :stability: experimental
        """
        self._values = {
        }
        if depends_on is not None: self._values["depends_on"] = depends_on
        if description is not None: self._values["description"] = description
        if sensitive is not None: self._values["sensitive"] = sensitive
        if value is not None: self._values["value"] = value

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List["TerraformResource"]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('depends_on')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('description')

    @builtins.property
    def sensitive(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('sensitive')

    @builtins.property
    def value(self) -> typing.Optional[typing.Union[str, jsii.Number, bool, typing.List[typing.Any], typing.Mapping[str, typing.Any]]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('value')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TerraformOutputConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class TerraformProvider(TerraformElement, metaclass=jsii.JSIIAbstractClass, jsii_type="cdktf.TerraformProvider"):
    """
    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _TerraformProviderProxy

    def __init__(self, scope: constructs.Construct, id: str, *, terraform_resource_type: str, terraform_generator_metadata: typing.Optional["TerraformGeneratorMetadata"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param terraform_resource_type: 
        :param terraform_generator_metadata: 

        stability
        :stability: experimental
        """
        config = TerraformProviderConfig(terraform_resource_type=terraform_resource_type, terraform_generator_metadata=terraform_generator_metadata)

        jsii.create(TerraformProvider, self, [scope, id, config])

    @jsii.member(jsii_name="addOverride")
    def add_override(self, path: str, value: typing.Any) -> None:
        """
        :param path: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addOverride", [path, value])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        """Adds this resource to the terraform JSON output.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toTerraform", [])

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "fqn")

    @builtins.property
    @jsii.member(jsii_name="metaAttributes")
    def meta_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "metaAttributes")

    @builtins.property
    @jsii.member(jsii_name="terraformResourceType")
    def terraform_resource_type(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformResourceType")

    @builtins.property
    @jsii.member(jsii_name="terraformGeneratorMetadata")
    def terraform_generator_metadata(self) -> typing.Optional["TerraformGeneratorMetadata"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformGeneratorMetadata")

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "alias")

    @alias.setter
    def alias(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "alias", value)


class _TerraformProviderProxy(TerraformProvider):
    pass

@jsii.data_type(jsii_type="cdktf.TerraformProviderConfig", jsii_struct_bases=[], name_mapping={'terraform_resource_type': 'terraformResourceType', 'terraform_generator_metadata': 'terraformGeneratorMetadata'})
class TerraformProviderConfig():
    def __init__(self, *, terraform_resource_type: str, terraform_generator_metadata: typing.Optional["TerraformGeneratorMetadata"]=None) -> None:
        """
        :param terraform_resource_type: 
        :param terraform_generator_metadata: 

        stability
        :stability: experimental
        """
        if isinstance(terraform_generator_metadata, dict): terraform_generator_metadata = TerraformGeneratorMetadata(**terraform_generator_metadata)
        self._values = {
            'terraform_resource_type': terraform_resource_type,
        }
        if terraform_generator_metadata is not None: self._values["terraform_generator_metadata"] = terraform_generator_metadata

    @builtins.property
    def terraform_resource_type(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('terraform_resource_type')

    @builtins.property
    def terraform_generator_metadata(self) -> typing.Optional["TerraformGeneratorMetadata"]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('terraform_generator_metadata')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TerraformProviderConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(ITerraformResource)
class TerraformResource(TerraformElement, metaclass=jsii.JSIIMeta, jsii_type="cdktf.TerraformResource"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: constructs.Construct, id: str, *, terraform_resource_type: str, terraform_generator_metadata: typing.Optional["TerraformGeneratorMetadata"]=None, count: typing.Optional[jsii.Number]=None, depends_on: typing.Optional[typing.List["TerraformResource"]]=None, lifecycle: typing.Optional["TerraformResourceLifecycle"]=None, provider: typing.Optional["TerraformProvider"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param terraform_resource_type: 
        :param terraform_generator_metadata: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 

        stability
        :stability: experimental
        """
        config = TerraformResourceConfig(terraform_resource_type=terraform_resource_type, terraform_generator_metadata=terraform_generator_metadata, count=count, depends_on=depends_on, lifecycle=lifecycle, provider=provider)

        jsii.create(TerraformResource, self, [scope, id, config])

    @jsii.member(jsii_name="addOverride")
    def add_override(self, path: str, value: typing.Any) -> None:
        """
        :param path: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addOverride", [path, value])

    @jsii.member(jsii_name="getBooleanAttribute")
    def get_boolean_attribute(self, terraform_attribute: str) -> bool:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getBooleanAttribute", [terraform_attribute])

    @jsii.member(jsii_name="getListAttribute")
    def get_list_attribute(self, terraform_attribute: str) -> typing.List[str]:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getListAttribute", [terraform_attribute])

    @jsii.member(jsii_name="getNumberAttribute")
    def get_number_attribute(self, terraform_attribute: str) -> jsii.Number:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getNumberAttribute", [terraform_attribute])

    @jsii.member(jsii_name="getStringAttribute")
    def get_string_attribute(self, terraform_attribute: str) -> str:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getStringAttribute", [terraform_attribute])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        """Adds this resource to the terraform JSON output.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toTerraform", [])

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "fqn")

    @builtins.property
    @jsii.member(jsii_name="terraformMetaArguments")
    def terraform_meta_arguments(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformMetaArguments")

    @builtins.property
    @jsii.member(jsii_name="terraformResourceType")
    def terraform_resource_type(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformResourceType")

    @builtins.property
    @jsii.member(jsii_name="terraformGeneratorMetadata")
    def terraform_generator_metadata(self) -> typing.Optional["TerraformGeneratorMetadata"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformGeneratorMetadata")

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "count")

    @count.setter
    def count(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.Optional[typing.List[str]]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "dependsOn")

    @depends_on.setter
    def depends_on(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "dependsOn", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycle")
    def lifecycle(self) -> typing.Optional["TerraformResourceLifecycle"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "lifecycle")

    @lifecycle.setter
    def lifecycle(self, value: typing.Optional["TerraformResourceLifecycle"]) -> None:
        jsii.set(self, "lifecycle", value)

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> typing.Optional["TerraformProvider"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "provider")

    @provider.setter
    def provider(self, value: typing.Optional["TerraformProvider"]) -> None:
        jsii.set(self, "provider", value)


@jsii.data_type(jsii_type="cdktf.TerraformResourceConfig", jsii_struct_bases=[TerraformMetaArguments], name_mapping={'count': 'count', 'depends_on': 'dependsOn', 'lifecycle': 'lifecycle', 'provider': 'provider', 'terraform_resource_type': 'terraformResourceType', 'terraform_generator_metadata': 'terraformGeneratorMetadata'})
class TerraformResourceConfig(TerraformMetaArguments):
    def __init__(self, *, count: typing.Optional[jsii.Number]=None, depends_on: typing.Optional[typing.List["TerraformResource"]]=None, lifecycle: typing.Optional["TerraformResourceLifecycle"]=None, provider: typing.Optional["TerraformProvider"]=None, terraform_resource_type: str, terraform_generator_metadata: typing.Optional["TerraformGeneratorMetadata"]=None) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param terraform_resource_type: 
        :param terraform_generator_metadata: 

        stability
        :stability: experimental
        """
        if isinstance(lifecycle, dict): lifecycle = TerraformResourceLifecycle(**lifecycle)
        if isinstance(terraform_generator_metadata, dict): terraform_generator_metadata = TerraformGeneratorMetadata(**terraform_generator_metadata)
        self._values = {
            'terraform_resource_type': terraform_resource_type,
        }
        if count is not None: self._values["count"] = count
        if depends_on is not None: self._values["depends_on"] = depends_on
        if lifecycle is not None: self._values["lifecycle"] = lifecycle
        if provider is not None: self._values["provider"] = provider
        if terraform_generator_metadata is not None: self._values["terraform_generator_metadata"] = terraform_generator_metadata

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('count')

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List["TerraformResource"]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('depends_on')

    @builtins.property
    def lifecycle(self) -> typing.Optional["TerraformResourceLifecycle"]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('lifecycle')

    @builtins.property
    def provider(self) -> typing.Optional["TerraformProvider"]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('provider')

    @builtins.property
    def terraform_resource_type(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('terraform_resource_type')

    @builtins.property
    def terraform_generator_metadata(self) -> typing.Optional["TerraformGeneratorMetadata"]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('terraform_generator_metadata')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TerraformResourceConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="cdktf.TerraformResourceLifecycle", jsii_struct_bases=[], name_mapping={'create_before_destroy': 'createBeforeDestroy', 'ignore_changes': 'ignoreChanges', 'prevent_destroy': 'preventDestroy'})
class TerraformResourceLifecycle():
    def __init__(self, *, create_before_destroy: typing.Optional[bool]=None, ignore_changes: typing.Optional[typing.List[str]]=None, prevent_destroy: typing.Optional[bool]=None) -> None:
        """
        :param create_before_destroy: 
        :param ignore_changes: 
        :param prevent_destroy: 

        stability
        :stability: experimental
        """
        self._values = {
        }
        if create_before_destroy is not None: self._values["create_before_destroy"] = create_before_destroy
        if ignore_changes is not None: self._values["ignore_changes"] = ignore_changes
        if prevent_destroy is not None: self._values["prevent_destroy"] = prevent_destroy

    @builtins.property
    def create_before_destroy(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('create_before_destroy')

    @builtins.property
    def ignore_changes(self) -> typing.Optional[typing.List[str]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('ignore_changes')

    @builtins.property
    def prevent_destroy(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('prevent_destroy')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TerraformResourceLifecycle(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class TerraformStack(constructs.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdktf.TerraformStack"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: constructs.Construct, id: str) -> None:
        """
        :param scope: -
        :param id: -

        stability
        :stability: experimental
        """
        jsii.create(TerraformStack, self, [scope, id])

    @jsii.member(jsii_name="isStack")
    @builtins.classmethod
    def is_stack(cls, x: typing.Any) -> bool:
        """
        :param x: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "isStack", [x])

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, construct: constructs.IConstruct) -> "TerraformStack":
        """
        :param construct: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "of", [construct])

    @jsii.member(jsii_name="addOverride")
    def add_override(self, path: str, value: typing.Any) -> None:
        """
        :param path: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addOverride", [path, value])

    @jsii.member(jsii_name="allProviders")
    def all_providers(self) -> typing.List["TerraformProvider"]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "allProviders", [])

    @jsii.member(jsii_name="onSynthesize")
    def on_synthesize(self, session: constructs.ISynthesisSession) -> None:
        """Allows this construct to emit artifacts into the cloud assembly during synthesis.

        This method is usually implemented by framework-level constructs such as ``Stack`` and ``Asset``
        as they participate in synthesizing the cloud assembly.

        :param session: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "onSynthesize", [session])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toTerraform", [])

    @builtins.property
    @jsii.member(jsii_name="artifactFile")
    def artifact_file(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "artifactFile")


@jsii.data_type(jsii_type="cdktf.TerraformStackMetadata", jsii_struct_bases=[], name_mapping={'stack_name': 'stackName', 'version': 'version'})
class TerraformStackMetadata():
    def __init__(self, *, stack_name: str, version: str) -> None:
        """
        :param stack_name: 
        :param version: 

        stability
        :stability: experimental
        """
        self._values = {
            'stack_name': stack_name,
            'version': version,
        }

    @builtins.property
    def stack_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('stack_name')

    @builtins.property
    def version(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TerraformStackMetadata(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Testing(metaclass=jsii.JSIIMeta, jsii_type="cdktf.Testing"):
    """Testing utilities for cdktf applications.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="app")
    @builtins.classmethod
    def app(cls) -> "App":
        """Returns an app for testing with the following properties: - Output directory is a temp dir.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "app", [])

    @jsii.member(jsii_name="stubVersion")
    @builtins.classmethod
    def stub_version(cls, app: "App") -> "App":
        """
        :param app: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "stubVersion", [app])

    @jsii.member(jsii_name="synth")
    @builtins.classmethod
    def synth(cls, stack: "TerraformStack") -> str:
        """Returns the Terraform synthesized JSON.

        :param stack: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "synth", [stack])


class Token(metaclass=jsii.JSIIMeta, jsii_type="cdktf.Token"):
    """Represents a special or lazily-evaluated value.

    Can be used to delay evaluation of a certain value in case, for example,
    that it requires some context or late-bound data. Can also be used to
    mark values that need special processing at document rendering time.

    Tokens can be embedded into strings while retaining their original
    semantics.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(Token, self, [])

    @jsii.member(jsii_name="asAny")
    @builtins.classmethod
    def as_any(cls, value: typing.Any) -> "IResolvable":
        """Return a resolvable representation of the given value.

        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "asAny", [value])

    @jsii.member(jsii_name="asList")
    @builtins.classmethod
    def as_list(cls, value: typing.Any, *, display_hint: typing.Optional[str]=None) -> typing.List[str]:
        """Return a reversible list representation of this token.

        :param value: -
        :param display_hint: A hint for the Token's purpose when stringifying it. Default: - no display hint

        stability
        :stability: experimental
        """
        options = EncodingOptions(display_hint=display_hint)

        return jsii.sinvoke(cls, "asList", [value, options])

    @jsii.member(jsii_name="asNumber")
    @builtins.classmethod
    def as_number(cls, value: typing.Any) -> jsii.Number:
        """Return a reversible number representation of this token.

        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "asNumber", [value])

    @jsii.member(jsii_name="asString")
    @builtins.classmethod
    def as_string(cls, value: typing.Any, *, display_hint: typing.Optional[str]=None) -> str:
        """Return a reversible string representation of this token.

        If the Token is initialized with a literal, the stringified value of the
        literal is returned. Otherwise, a special quoted string representation
        of the Token is returned that can be embedded into other strings.

        Strings with quoted Tokens in them can be restored back into
        complex values with the Tokens restored by calling ``resolve()``
        on the string.

        :param value: -
        :param display_hint: A hint for the Token's purpose when stringifying it. Default: - no display hint

        stability
        :stability: experimental
        """
        options = EncodingOptions(display_hint=display_hint)

        return jsii.sinvoke(cls, "asString", [value, options])

    @jsii.member(jsii_name="isUnresolved")
    @builtins.classmethod
    def is_unresolved(cls, obj: typing.Any) -> bool:
        """Returns true if obj represents an unresolved value.

        One of these must be true:

        - ``obj`` is an IResolvable
        - ``obj`` is a string containing at least one encoded ``IResolvable``
        - ``obj`` is either an encoded number or list

        This does NOT recurse into lists or objects to see if they
        containing resolvables.

        :param obj: The object to test.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "isUnresolved", [obj])


class Tokenization(metaclass=jsii.JSIIMeta, jsii_type="cdktf.Tokenization"):
    """Less oft-needed functions to manipulate Tokens.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(Tokenization, self, [])

    @jsii.member(jsii_name="isResolvable")
    @builtins.classmethod
    def is_resolvable(cls, obj: typing.Any) -> bool:
        """Return whether the given object is an IResolvable object.

        This is different from Token.isUnresolved() which will also check for
        encoded Tokens, whereas this method will only do a type check on the given
        object.

        :param obj: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "isResolvable", [obj])

    @jsii.member(jsii_name="resolve")
    @builtins.classmethod
    def resolve(cls, obj: typing.Any, *, resolver: "ITokenResolver", scope: constructs.IConstruct, preparing: typing.Optional[bool]=None) -> typing.Any:
        """Resolves an object by evaluating all tokens and removing any undefined or empty objects or arrays.

        Values can only be primitives, arrays or tokens. Other objects (i.e. with methods) will be rejected.

        :param obj: The object to resolve.
        :param resolver: The resolver to apply to any resolvable tokens found.
        :param scope: The scope from which resolution is performed.
        :param preparing: Whether the resolution is being executed during the prepare phase or not. Default: false

        stability
        :stability: experimental
        """
        options = ResolveOptions(resolver=resolver, scope=scope, preparing=preparing)

        return jsii.sinvoke(cls, "resolve", [obj, options])

    @jsii.member(jsii_name="reverseList")
    @builtins.classmethod
    def reverse_list(cls, l: typing.List[str]) -> typing.Optional["IResolvable"]:
        """Un-encode a Tokenized value from a list.

        :param l: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "reverseList", [l])

    @jsii.member(jsii_name="reverseNumber")
    @builtins.classmethod
    def reverse_number(cls, n: jsii.Number) -> typing.Optional["IResolvable"]:
        """Un-encode a Tokenized value from a number.

        :param n: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "reverseNumber", [n])

    @jsii.member(jsii_name="reverseString")
    @builtins.classmethod
    def reverse_string(cls, s: str) -> "TokenizedStringFragments":
        """Un-encode a string potentially containing encoded tokens.

        :param s: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "reverseString", [s])

    @jsii.member(jsii_name="stringifyNumber")
    @builtins.classmethod
    def stringify_number(cls, x: jsii.Number) -> str:
        """Stringify a number directly or lazily if it's a Token.

        If it is an object (i.e., { Ref: 'SomeLogicalId' }), return it as-is.

        :param x: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "stringifyNumber", [x])


class TokenizedStringFragments(metaclass=jsii.JSIIMeta, jsii_type="cdktf.TokenizedStringFragments"):
    """Fragments of a concatenated string containing stringified Tokens.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(TokenizedStringFragments, self, [])

    @jsii.member(jsii_name="addIntrinsic")
    def add_intrinsic(self, value: typing.Any) -> None:
        """Adds an intrinsic fragment.

        :param value: the intrinsic value to add.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addIntrinsic", [value])

    @jsii.member(jsii_name="addLiteral")
    def add_literal(self, lit: typing.Any) -> None:
        """Adds a literal fragment.

        :param lit: the literal to add.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addLiteral", [lit])

    @jsii.member(jsii_name="addToken")
    def add_token(self, token: "IResolvable") -> None:
        """Adds a token fragment.

        :param token: the token to add.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToken", [token])

    @jsii.member(jsii_name="join")
    def join(self, concat: "IFragmentConcatenator") -> typing.Any:
        """Combine the string fragments using the given joiner.

        If there are any

        :param concat: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "join", [concat])

    @jsii.member(jsii_name="mapTokens")
    def map_tokens(self, mapper: "ITokenMapper") -> "TokenizedStringFragments":
        """Apply a transformation function to all tokens in the string.

        :param mapper: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "mapTokens", [mapper])

    @builtins.property
    @jsii.member(jsii_name="firstValue")
    def first_value(self) -> typing.Any:
        """Returns the first value.

        stability
        :stability: experimental
        """
        return jsii.get(self, "firstValue")

    @builtins.property
    @jsii.member(jsii_name="length")
    def length(self) -> jsii.Number:
        """Returns the number of fragments.

        stability
        :stability: experimental
        """
        return jsii.get(self, "length")

    @builtins.property
    @jsii.member(jsii_name="tokens")
    def tokens(self) -> typing.List["IResolvable"]:
        """Return all Tokens from this string.

        stability
        :stability: experimental
        """
        return jsii.get(self, "tokens")

    @builtins.property
    @jsii.member(jsii_name="firstToken")
    def first_token(self) -> typing.Optional["IResolvable"]:
        """Returns the first token.

        stability
        :stability: experimental
        """
        return jsii.get(self, "firstToken")


@jsii.implements(ITokenResolver)
class DefaultTokenResolver(metaclass=jsii.JSIIMeta, jsii_type="cdktf.DefaultTokenResolver"):
    """Default resolver implementation.

    stability
    :stability: experimental
    """
    def __init__(self, concat: "IFragmentConcatenator") -> None:
        """
        :param concat: -

        stability
        :stability: experimental
        """
        jsii.create(DefaultTokenResolver, self, [concat])

    @jsii.member(jsii_name="resolveList")
    def resolve_list(self, xs: typing.List[str], context: "IResolveContext") -> typing.Any:
        """Resolve a tokenized list.

        :param xs: -
        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveList", [xs, context])

    @jsii.member(jsii_name="resolveString")
    def resolve_string(self, fragments: "TokenizedStringFragments", context: "IResolveContext") -> typing.Any:
        """Resolve string fragments to Tokens.

        :param fragments: -
        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveString", [fragments, context])

    @jsii.member(jsii_name="resolveToken")
    def resolve_token(self, t: "IResolvable", context: "IResolveContext", post_processor: "IPostProcessor") -> typing.Any:
        """Default Token resolution.

        Resolve the Token, recurse into whatever it returns,
        then finally post-process it.

        :param t: -
        :param context: -
        :param post_processor: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveToken", [t, context, post_processor])


@jsii.implements(ITerraformResource)
class TerraformDataSource(TerraformElement, metaclass=jsii.JSIIMeta, jsii_type="cdktf.TerraformDataSource"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: constructs.Construct, id: str, *, terraform_resource_type: str, terraform_generator_metadata: typing.Optional["TerraformGeneratorMetadata"]=None, count: typing.Optional[jsii.Number]=None, depends_on: typing.Optional[typing.List["TerraformResource"]]=None, lifecycle: typing.Optional["TerraformResourceLifecycle"]=None, provider: typing.Optional["TerraformProvider"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param terraform_resource_type: 
        :param terraform_generator_metadata: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 

        stability
        :stability: experimental
        """
        config = TerraformResourceConfig(terraform_resource_type=terraform_resource_type, terraform_generator_metadata=terraform_generator_metadata, count=count, depends_on=depends_on, lifecycle=lifecycle, provider=provider)

        jsii.create(TerraformDataSource, self, [scope, id, config])

    @jsii.member(jsii_name="addOverride")
    def add_override(self, path: str, value: typing.Any) -> None:
        """
        :param path: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addOverride", [path, value])

    @jsii.member(jsii_name="getBooleanAttribute")
    def get_boolean_attribute(self, terraform_attribute: str) -> bool:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getBooleanAttribute", [terraform_attribute])

    @jsii.member(jsii_name="getListAttribute")
    def get_list_attribute(self, terraform_attribute: str) -> typing.List[str]:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getListAttribute", [terraform_attribute])

    @jsii.member(jsii_name="getNumberAttribute")
    def get_number_attribute(self, terraform_attribute: str) -> jsii.Number:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getNumberAttribute", [terraform_attribute])

    @jsii.member(jsii_name="getStringAttribute")
    def get_string_attribute(self, terraform_attribute: str) -> str:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getStringAttribute", [terraform_attribute])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        """Adds this resource to the terraform JSON output.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toTerraform", [])

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "fqn")

    @builtins.property
    @jsii.member(jsii_name="terraformMetaArguments")
    def terraform_meta_arguments(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformMetaArguments")

    @builtins.property
    @jsii.member(jsii_name="terraformResourceType")
    def terraform_resource_type(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformResourceType")

    @builtins.property
    @jsii.member(jsii_name="terraformGeneratorMetadata")
    def terraform_generator_metadata(self) -> typing.Optional["TerraformGeneratorMetadata"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformGeneratorMetadata")

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "count")

    @count.setter
    def count(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.Optional[typing.List[str]]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "dependsOn")

    @depends_on.setter
    def depends_on(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "dependsOn", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycle")
    def lifecycle(self) -> typing.Optional["TerraformResourceLifecycle"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "lifecycle")

    @lifecycle.setter
    def lifecycle(self, value: typing.Optional["TerraformResourceLifecycle"]) -> None:
        jsii.set(self, "lifecycle", value)

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> typing.Optional["TerraformProvider"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "provider")

    @provider.setter
    def provider(self, value: typing.Optional["TerraformProvider"]) -> None:
        jsii.set(self, "provider", value)


__all__ = [
    "App",
    "AppOptions",
    "BooleanMap",
    "ComplexComputedList",
    "DefaultTokenResolver",
    "EncodingOptions",
    "IAnyProducer",
    "IFragmentConcatenator",
    "IListProducer",
    "INumberProducer",
    "IPostProcessor",
    "IResolvable",
    "IResolveContext",
    "IResource",
    "IStringProducer",
    "ITerraformResource",
    "ITokenMapper",
    "ITokenResolver",
    "Lazy",
    "LazyAnyValueOptions",
    "LazyListValueOptions",
    "LazyStringValueOptions",
    "NumberMap",
    "ResolveOptions",
    "Resource",
    "StringConcat",
    "StringMap",
    "TerraformDataSource",
    "TerraformElement",
    "TerraformElementMetadata",
    "TerraformGeneratorMetadata",
    "TerraformMetaArguments",
    "TerraformModule",
    "TerraformModuleOptions",
    "TerraformOutput",
    "TerraformOutputConfig",
    "TerraformProvider",
    "TerraformProviderConfig",
    "TerraformResource",
    "TerraformResourceConfig",
    "TerraformResourceLifecycle",
    "TerraformStack",
    "TerraformStackMetadata",
    "Testing",
    "Token",
    "Tokenization",
    "TokenizedStringFragments",
]

publication.publish()
