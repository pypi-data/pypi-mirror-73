from pbr.version import VersionInfo

__version__ = VersionInfo('ipeanim').version_string()
__version_info__ = VersionInfo('ipeanim').semantic_version().version_tuple()
