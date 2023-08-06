# -*- coding: utf-8 -*-

"""Console script for rcmip."""
import logging
import sys
from glob import glob
from os.path import basename, join

import boto3
import click
import jwt
import semver
from botocore.exceptions import ClientError

from pyrcmip.validate import run_validation

logger = logging.getLogger("rcmip.cli")


class ColorFormatter(logging.Formatter):
    colors = {
        "error": dict(fg="red"),
        "exception": dict(fg="red"),
        "critical": dict(fg="red"),
        "debug": dict(fg="blue"),
        "warning": dict(fg="yellow"),
    }

    def format(self, record):
        if not record.exc_info:
            level = record.levelname.lower()
            msg = record.getMessage()
            if level in self.colors:
                prefix = click.style("{}: ".format(level), **self.colors[level])
                msg = "\n".join(prefix + x for x in msg.splitlines())
            return msg
        return logging.Formatter.format(self, record)


class ClickHandler(logging.Handler):
    _use_stderr = True

    def emit(self, record):
        try:
            msg = self.format(record)
            click.echo(msg, err=self._use_stderr)
        except Exception:  # pragma: no cover
            self.handleError(record)


_default_handler = ClickHandler()
_default_handler.formatter = ColorFormatter()


@click.group(name="rcmip")
@click.option("--log-level", default="INFO")
def cli(log_level):
    root = logging.getLogger()
    root.handlers.append(_default_handler)
    root.setLevel(log_level)


def clean_input_fnames(ctx, param, inp):
    filenames = []

    for f in inp:
        filenames.extend(glob(f))

    for f in filenames:
        logger.info("found {}".format(f))

    if len(filenames) == 0:
        raise click.BadParameter("No valid input files found")

    return sorted(set(filenames))


@cli.command()
@click.argument("input", nargs=-1, type=click.Path(), callback=clean_input_fnames)
def validate(input):
    try:
        run_validation(input)
    except Exception as e:
        raise click.ClickException(str(e))


def validate_version(ctx, param, value):
    try:
        s = semver.VersionInfo.parse(value)

        if s.prerelease is None and s.build is None:
            return value
        else:
            raise click.BadParameter(
                "Version must only contain major, minor and patch values"
            )
    except ValueError:
        raise click.BadParameter("Cannot parse version string")


@cli.command()
@click.option("--validate/--no-validate", default=True)
@click.option(
    "--token",
    required=True,
    help="Authentication token. Contact zebedee.nicholls@climate-energy-college.org for a token",
)
@click.option("--bucket", default="rcmip-uploads-au")
@click.option("--model", required=True)
@click.option(
    "--version",
    required=True,
    callback=validate_version,
    help="Version of the data being uploaded. Must be a valid semver version string (https://semver.org/). "
    "For example 2.0.0",
)
@click.argument("input", nargs=-1, type=click.Path(), callback=clean_input_fnames)
def upload(validate, token, bucket, model, version, input):
    if validate:
        try:
            run_validation(input)
        except Exception:
            raise click.ClickException("Validation failed. Fix issues and rerun")

    # Upload data to S3
    t = jwt.decode(token, verify=False)
    session = boto3.session.Session(
        aws_access_key_id=t["access_key_id"],
        aws_secret_access_key=t["secret_access_key"],
    )
    client = session.client("s3")

    root_key = "{}/{}/{}".format(t["org"], model, version)

    # Check if this version is already uploaded (using the {key}-complete dummy file)
    try:
        client.head_object(Bucket=bucket, Key=root_key + "-complete")

        raise click.ClickException(
            "Data for this version has already been uploaded. Increment the version and try again"
        )
    except ClientError:
        logger.debug("Object with key {} does not exist".format(root_key))

    try:
        for f in input:
            key = join(root_key, basename(f))
            logger.info("Uploading {}".format(f))
            client.upload_file(Bucket=bucket, Key=key, Filename=f)
    except ClientError:  # pragma: no cover
        logger.exception("Failed to upload file")
        raise click.ClickException("Failed to upload file")

    # Finally mark the upload as complete by uploading a dummy file
    # Writing this dummy file will be used to start the processing of the upload
    client.put_object(Bucket=bucket, Key=root_key + "-complete")

    logger.info("All files uploaded successfully")


def run_cli():
    sys.exit(cli(auto_envvar_prefix="RCMIP"))  # pragma: no cover


if __name__ == "__main__":
    run_cli()  # pragma: no cover
