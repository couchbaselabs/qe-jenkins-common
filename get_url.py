#!/usr/bin/python3
import re
import urllib
import argparse


LATEST_BUILDS_URL = "http://latestbuilds.service.couchbase.com/builds/latestbuilds/couchbase-server"


class Version:

    VERSIONS = {'6.5': 'mad-hatter',
                '7.0': 'cheshire-chat',
                '7.1': 'neo'}

    EDITIONS, PLATFORMS = {'enterprise'}, {'centos7.x86_64.rpm'}

    def __init__(self, version, edition, platform):
        match = re.match(
            '(?P<major>\d\.\d)\.(?P<minor>\d)-(?P<build>\d+)', version)

        if not match:
            raise ValueError(f"The given version {version} is not of the form '7.1.0-1234'.")

        self.major = match.group('major')
        self.minor = match.group('minor')
        self.build = match.group('build')

        if self.major not in Version.VERSIONS:
            raise ValueError(f"The major version {self.major} is unknown.")

        self.edition = edition
        self.platform = platform

        if self.edition not in Version.EDITIONS:
            raise ValueError(f"The edition {self.edition} is unknown.")

        if self.platform not in Version.PLATFORMS:
            raise ValueError(f"The platform {self.platform} is unknown.")

    @property
    def full(self):
        """ Returns a version string of the form "7.1.0-1234. """
        return f"{self.major}.{self.minor}-{self.build}"

    @property
    def name(self):
        """ Returns the official version name e.g. Neo. """
        return Version.VERSIONS[self.major]

    @property
    def get_url(self):
        """ Returns a latestbuilds download link. """
        return (f"{LATEST_BUILDS_URL}"
                f"/{self.name}/{self.build}/couchbase-server-{self.edition}-{self.full}-{self.platform}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Downloads Couchbase packages.")
    parser.add_argument('version', help="Version string e.g. (7.1.0-1234)", type=str)
    parser.add_argument('edition', help="Edition e.g. (enterprise)", type=str)
    parser.add_argument('platform', help="Platform e.g. centos7-x86_64.rpm", type=str)

    args = parser.parse_args()

    print(Version(args.version, args.edition, args.platform).get_url)
