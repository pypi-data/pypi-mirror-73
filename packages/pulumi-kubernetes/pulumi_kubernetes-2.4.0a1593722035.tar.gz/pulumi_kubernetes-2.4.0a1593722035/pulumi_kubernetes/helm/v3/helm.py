# *** WARNING: this file was generated by the Pulumi Kubernetes codegen tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import os.path
import shutil
import subprocess
import re
from tempfile import mkdtemp, mkstemp
from typing import Any, Callable, List, Optional, TextIO, Tuple, Union

import pulumi.runtime
from ...utilities import get_version
from pulumi_kubernetes.yaml import _parse_yaml_document


class FetchOpts:
    """
    FetchOpts is a bag of configuration options to customize the fetching of the Helm chart.
    """

    version: Optional[pulumi.Input[str]]
    """
    Specific version of a chart. If unset, the latest version is fetched.
    """

    ca_file: Optional[pulumi.Input[str]]
    """
    Verify certificates of HTTPS-enabled servers using this CA bundle.
    """

    cert_file: Optional[pulumi.Input[str]]
    """
    Identify HTTPS client using this SSL certificate file.
    """

    key_file: Optional[pulumi.Input[str]]
    """
    Identify HTTPS client using this SSL key file.
    """

    destination: Optional[pulumi.Input[str]]
    """
    Location to write the chart. If this and [tardir] are specified, tardir is appended
    to this (default ".").
    """

    keyring: Optional[pulumi.Input[str]]
    """
    Keyring containing public keys (default "/Users/alex/.gnupg/pubring.gpg").
    """

    password: Optional[pulumi.Input[str]]
    """
    Chart repository password.
    """

    repo: Optional[pulumi.Input[str]]
    """
    Chart repository url where to locate the requested chart.
    """

    untar_dir: Optional[pulumi.Input[str]]
    """
    If [untar] is specified, this flag specifies the name of the directory into which
    the chart is expanded (default ".").
    """

    username: Optional[pulumi.Input[str]]
    """
    Chart repository username.
    """

    home: Optional[pulumi.Input[str]]
    """
    Location of your Helm config. Overrides $HELM_HOME (default "/Users/alex/.helm").
    """

    devel: Optional[pulumi.Input[bool]]
    """
    Use development versions, too. Equivalent to version '>0.0.0-0'. If [version] is set,
    this is ignored.
    """

    prov: Optional[pulumi.Input[bool]]
    """
    Fetch the provenance file, but don't perform verification.
    """

    untar: Optional[pulumi.Input[bool]]
    """
    If set to false, will leave the chart as a tarball after downloading.
    """

    verify: Optional[pulumi.Input[bool]]
    """
    Verify the package against its signature.
    """

    def __init__(self, version=None, ca_file=None, cert_file=None, key_file=None, destination=None, keyring=None,
                 password=None, repo=None, untar_dir=None, username=None, home=None, devel=None, prov=None,
                 untar=None, verify=None):
        """
        :param Optional[pulumi.Input[str]] version: Specific version of a chart. If unset,
               the latest version is fetched.
        :param Optional[pulumi.Input[str]] ca_file: Verify certificates of HTTPS-enabled
               servers using this CA bundle.
        :param Optional[pulumi.Input[str]] cert_file: Identify HTTPS client using this SSL
               certificate file.
        :param Optional[pulumi.Input[str]] key_file: Identify HTTPS client using this SSL
               key file.
        :param Optional[pulumi.Input[str]] destination: Location to write the chart.
               If this and [tardir] are specified, tardir is appended to this (default ".").
        :param Optional[pulumi.Input[str]] keyring: Keyring containing public keys
               (default "/Users/<user>/.gnupg/pubring.gpg").
        :param Optional[pulumi.Input[str]] password: Chart repository password.
        :param Optional[pulumi.Input[str]] repo: Chart repository url where to locate
               the requested chart.
        :param Optional[pulumi.Input[str]] untar_dir: If [untar] is specified, this flag
               specifies the name of the directory into which the chart is
               expanded (default ".").
        :param Optional[pulumi.Input[str]] username: Chart repository username.
        :param Optional[pulumi.Input[str]] home: Location of your Helm config. Overrides
               $HELM_HOME (default "/Users/<user>/.helm").
        :param Optional[pulumi.Input[bool]] devel: Use development versions, too.
               Equivalent to version '>0.0.0-0'. If [version] is set, this is ignored.
        :param Optional[pulumi.Input[bool]] prov: Fetch the provenance file, but don't
               perform verification.
        :param Optional[pulumi.Input[bool]] untar: If set to false, will leave the
               chart as a tarball after downloading.
        :param Optional[pulumi.Input[bool]] verify: Verify the package against its signature.
        """
        self.version = version
        self.ca_file = ca_file
        self.cert_file = cert_file
        self.key_file = key_file
        self.destination = destination
        self.keyring = keyring
        self.password = password
        self.repo = repo
        self.untar_dir = untar_dir
        self.username = username
        self.home = home
        self.devel = devel
        self.prov = prov
        self.untar = untar
        self.verify = verify


class BaseChartOpts:
    """
    BaseChartOpts is a bag of common configuration options for a Helm chart.
    """

    namespace: Optional[pulumi.Input[str]]
    """
    Optional namespace to install chart resources into.
    """

    values: Optional[pulumi.Inputs]
    """
    Optional overrides for chart values.
    """

    transformations: Optional[List[Callable]]
    """
    Optional list of transformations to apply to resources that will be created by this chart prior to
    creation. Allows customization of the chart behaviour without directly modifying the chart itself.
    """

    resource_prefix: Optional[str]
    """
    Optional prefix for the auto-generated resource names.
    Example: A resource created with resource_prefix="foo" would produce a resource named "foo-resourceName".
    """

    def __init__(self, namespace=None, values=None, transformations=None, resource_prefix=None):
        """
        :param Optional[pulumi.Input[str]] namespace: Optional namespace to install chart resources into.
        :param Optional[pulumi.Inputs] values: Optional overrides for chart values.
        :param Optional[List[Tuple[Callable, Optional[pulumi.ResourceOptions]]]] transformations: Optional list
               of transformations to apply to resources that will be created by this chart prior to creation.
               Allows customization of the chart behaviour without directly modifying the chart itself.
        :param Optional[str] resource_prefix: An optional prefix for the auto-generated resource names.
               Example: A resource created with resource_prefix="foo" would produce a resource named "foo-resourceName".
        """
        self.namespace = namespace
        self.values = values
        self.transformations = transformations
        self.resource_prefix = resource_prefix


class ChartOpts(BaseChartOpts):
    """
    ChartOpts is a bag of configuration options for a remote Helm chart.
    """

    chart: pulumi.Input[str]
    """
    The name of the chart to deploy.  If `repo` is provided, this chart name will be prefixed by the repo name.
    Example: repo: "stable", chart: "nginx-ingress" -> "stable/nginx-ingress"
    Example: chart: "stable/nginx-ingress" -> "stable/nginx-ingress"
    """

    repo: Optional[pulumi.Input[str]]
    """
    The repository name of the chart to deploy. 
    Example: "stable"
    """

    version: Optional[pulumi.Input[str]]
    """
    The version of the chart to deploy. If not provided, the latest version will be deployed.
    """

    fetch_opts: Optional[pulumi.Input[FetchOpts]]
    """
    Additional options to customize the fetching of the Helm chart.
    """

    def __init__(self, chart, namespace=None, values=None, transformations=None, resource_prefix=None, repo=None,
                 version=None, fetch_opts=None):
        """
        :param pulumi.Input[str] chart: The name of the chart to deploy.  If `repo` is provided, this chart name
               will be prefixed by the repo name.
               Example: repo: "stable", chart: "nginx-ingress" -> "stable/nginx-ingress"
               Example: chart: "stable/nginx-ingress" -> "stable/nginx-ingress"
        :param Optional[pulumi.Input[str]] namespace: Optional namespace to install chart resources into.
        :param Optional[pulumi.Inputs] values: Optional overrides for chart values.
        :param Optional[List[Tuple[Callable, Optional[pulumi.ResourceOptions]]]] transformations: Optional list of
               transformations to apply to resources that will be created by this chart prior to creation.
               Allows customization of the chart behaviour without directly modifying the chart itself.
        :param Optional[str] resource_prefix: An optional prefix for the auto-generated resource names.
               Example: A resource created with resource_prefix="foo" would produce a resource named "foo-resourceName".
        :param Optional[pulumi.Input[str]] repo: The repository name of the chart to deploy.
               Example: "stable"
        :param Optional[pulumi.Input[str]] version: The version of the chart to deploy. If not provided,
               the latest version will be deployed.
        :param Optional[pulumi.Input[FetchOpts]] fetch_opts: Additional options to customize the
               fetching of the Helm chart.
        """
        super(ChartOpts, self).__init__(namespace, values, transformations, resource_prefix)
        self.chart = chart
        self.repo = repo
        self.version = version
        self.fetch_opts = fetch_opts


class LocalChartOpts(BaseChartOpts):
    """
    LocalChartOpts is a bag of configuration options for a local Helm chart.
    """

    path: pulumi.Input[str]
    """
    The path to the chart directory which contains the `Chart.yaml` file.
    """

    def __init__(self, path, namespace=None, values=None, transformations=None, resource_prefix=None):
        """
        :param pulumi.Input[str] path: The path to the chart directory which contains the
               `Chart.yaml` file.
        :param Optional[pulumi.Input[str]] namespace: Optional namespace to install chart resources into.
        :param Optional[pulumi.Inputs] values: Optional overrides for chart values.
        :param Optional[List[Tuple[Callable, Optional[pulumi.ResourceOptions]]]] transformations: Optional list of
               transformations to apply to resources that will be created by this chart prior to creation.
               Allows customization of the chart behaviour without directly modifying the chart itself.
        :param Optional[str] resource_prefix: An optional prefix for the auto-generated resource names.
               Example: A resource created with resource_prefix="foo" would produce a resource named "foo-resourceName".
        """

        super(LocalChartOpts, self).__init__(namespace, values, transformations, resource_prefix)
        self.path = path


def _run_helm_cmd(all_config: Tuple[List[Union[str, bytes]], Any]) -> str:
    cmd, _ = all_config

    output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
    yaml_str: str = output.stdout
    return yaml_str

def _is_helm_v3() -> bool:

    cmd: List[str] = ['helm', 'version', '--short']

    """ 
    Helm v2 returns version like this:
    Client: v2.16.7+g5f2584f
    Helm v3 returns a version like this:
    v3.1.2+gd878d4d
    --include-crds is available in helm v3.1+ so check for a regex matching that version
    """
    output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True, check=True)
    version: str = output.stdout
    regexp = re.compile(r'^v3\.[1-9]')
    return(bool(regexp.search(version)))


def _write_override_file(all_config: Tuple[TextIO, str]) -> None:
    file, data = all_config

    file.write(data)
    file.flush()


def _cleanup_temp_dir(all_config: Tuple[TextIO, Union[bytes, str], Any]) -> None:
    file, chart_dir, _ = all_config

    file.close()
    shutil.rmtree(chart_dir)


def _parse_chart(all_config: Tuple[str, Union[ChartOpts, LocalChartOpts], pulumi.ResourceOptions]) -> pulumi.Output:
    release_name, config, opts = all_config

    # Create temporary directory and file to hold chart data and override values.
    # Note: We're intentionally using the lower-level APIs here because the async Outputs are being handled in
    # a different scope, which was causing the temporary files/directory to be deleted before they were referenced
    # in the Output handlers. We manually clean these up once we're done with another async handler that depends
    # on the result of the operations.
    overrides, overrides_filename = mkstemp()
    chart_dir = mkdtemp()

    if isinstance(config, ChartOpts):
        if config.repo and 'http' in config.repo:
            raise ValueError('`repo` specifies the name of the Helm chart repo.'
                             'Use `fetch_opts.repo` to specify a URL.')
        chart_to_fetch = f'{config.repo}/{config.chart}' if config.repo else config.chart

        # Configure fetch options.
        fetch_opts_dict = {}
        if config.fetch_opts is not None:
            fetch_opts_dict = {k: v for k, v in vars(config.fetch_opts).items() if v is not None}
        fetch_opts_dict["destination"] = chart_dir
        if config.version is not None:
            fetch_opts_dict["version"] = config.version
        fetch_opts = FetchOpts(**fetch_opts_dict)

        # Fetch the chart.
        _fetch(chart_to_fetch, fetch_opts)
        # Sort the directories into alphabetical order, and choose the first
        fetched_chart_name = sorted(os.listdir(chart_dir), key=str.lower)[0]
        chart = os.path.join(chart_dir, fetched_chart_name)
    else:
        chart = config.path

    default_values = os.path.join(chart, 'values.yaml')

    # Write overrides file.
    vals = config.values if config.values is not None else {}
    data = pulumi.Output.from_input(vals).apply(lambda x: json.dumps(x))
    file = open(overrides, 'w')
    pulumi.Output.all(file, data).apply(_write_override_file)

    namespace_arg = ['--namespace', config.namespace] if config.namespace else []
    crd_arg = [ '--include-crds' ] if _is_helm_v3() else []

    # Use 'helm template' to create a combined YAML manifest.
    cmd = ['helm', 'template', chart, '--name-template', release_name,
           '--values', default_values, '--values', overrides_filename]
    cmd.extend(namespace_arg)
    cmd.extend(crd_arg)

    chart_resources = pulumi.Output.all(cmd, data).apply(_run_helm_cmd)

    # Rather than using the default provider for the following invoke call, use the version specified
    # in package.json.
    invoke_opts = pulumi.InvokeOptions(version=get_version())

    objects = chart_resources.apply(
        lambda text: pulumi.runtime.invoke('kubernetes:yaml:decode', {
            'text': text, 'defaultNamespace': config.namespace}, invoke_opts).value['result'])

    # Parse the manifest and create the specified resources.
    resources = objects.apply(
        lambda objects: _parse_yaml_document(objects, opts, config.transformations))

    pulumi.Output.all(file, chart_dir, resources).apply(_cleanup_temp_dir)
    return resources


def _fetch(chart: str, opts: FetchOpts) -> None:
    cmd: List[str] = ['helm', 'fetch', chart]

    # Untar by default.
    if opts.untar is not False:
        cmd.append('--untar')

    env = os.environ
    # Helm v3 removed the `--home` flag, so we must use an env var instead.
    if opts.home:
        env['HELM_HOME'] = opts.home

    if opts.version:
        cmd.extend(['--version', opts.version])
    if opts.ca_file:
        cmd.extend(['--ca-file', opts.ca_file])
    if opts.cert_file:
        cmd.extend(['--cert-file', opts.cert_file])
    if opts.key_file:
        cmd.extend(['--key-file', opts.key_file])
    if opts.destination:
        cmd.extend(['--destination', opts.destination])
    if opts.keyring:
        cmd.extend(['--keyring', opts.keyring])
    if opts.password:
        cmd.extend(['--password', opts.password])
    if opts.repo:
        cmd.extend(['--repo', opts.repo])
    if opts.untar_dir:
        cmd.extend(['--untardir', opts.untar_dir])
    if opts.username:
        cmd.extend(['--username', opts.username])
    if opts.devel:
        cmd.append('--devel')
    if opts.prov:
        cmd.append('--prov')
    if opts.verify:
        cmd.append('--verify')

    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True, env=env)


class Chart(pulumi.ComponentResource):
    """
    Chart is a component representing a collection of resources described by an arbitrary Helm
    Chart. The Chart can be fetched from any source that is accessible to the `helm` command
    line. Values in the `values.yml` file can be overridden using `ChartOpts.values` (equivalent
    to `--set` or having multiple `values.yml` files). Objects can be transformed arbitrarily by
    supplying callbacks to `ChartOpts.transformations`.

    Chart does not use Tiller. The Chart specified is copied and expanded locally; the semantics
    are equivalent to running `helm template` and then using Pulumi to manage the resulting YAML
    manifests. Any values that would be retrieved in-cluster are assigned fake values, and
    none of Tiller's server-side validity testing is executed.
    """

    resources: pulumi.Output[dict]
    """
    Kubernetes resources contained in this Chart.
    """

    def __init__(self, release_name, config, opts=None):
        """
        Create an instance of the specified Helm chart.

        :param str release_name: Name of the Chart (e.g., nginx-ingress).
        :param Union[ChartOpts, LocalChartOpts] config: Configuration options for the Chart.
        :param Optional[pulumi.ResourceOptions] opts: A bag of options that control this
               resource's behavior.
        """
        if not release_name:
            raise TypeError('Missing release name argument')
        if not isinstance(release_name, str):
            raise TypeError('Expected release name to be a string')
        if config and not isinstance(config, ChartOpts) and not isinstance(config, LocalChartOpts):
            raise TypeError('Expected config to be a ChartOpts or LocalChartOpts instance')
        if opts and not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if config.resource_prefix:
            release_name = f"{config.resource_prefix}-{release_name}"

        super(Chart, self).__init__(
            "kubernetes:helm.sh/v2:Chart",
            release_name,
            __props__,
            opts)

        if opts is not None:
            opts.parent = self
        else:
            opts = pulumi.ResourceOptions(parent=self)

        all_config = pulumi.Output.from_input((release_name, config, opts))

        # Note: Unlike NodeJS, Python requires that we "pull" on our futures in order to get them scheduled for
        # execution. In order to do this, we leverage the engine's RegisterResourceOutputs to wait for the
        # resolution of all resources that this Helm chart created.
        self.resources = all_config.apply(_parse_chart)
        self.register_outputs({"resources": self.resources})

    def get_resource(self, group_version_kind, name, namespace=None) -> pulumi.Output[pulumi.CustomResource]:
        """
        get_resource returns a resource defined by a built-in Kubernetes group/version/kind and
        name. For example: `get_resource("apps/v1/Deployment", "nginx")`

        :param str group_version_kind: Group/Version/Kind of the resource, e.g., `apps/v1/Deployment`
        :param str name: Name of the resource to retrieve
        :param str namespace: Optional namespace of the resource to retrieve
        """

        # `id` will either be `${name}` or `${namespace}/${name}`.
        id = pulumi.Output.from_input(name)
        if namespace is not None:
            id = pulumi.Output.concat(namespace, '/', name)

        resource_id = id.apply(lambda x: f'{group_version_kind}:{x}')
        return resource_id.apply(lambda x: self.resources[x])
