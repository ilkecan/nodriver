# DO NOT EDIT THIS FILE!
#
# This file is generated from the CDP specification. If you need to make
# changes, edit the generator and regenerate all of the modules.
#
# CDP domain: FileSystem (experimental)

from __future__ import annotations
import enum
import typing
from dataclasses import dataclass
from .util import event_class, T_JSON_DICT

from . import network
from . import storage


@dataclass
class File:
    name: str

    #: Timestamp
    last_modified: network.TimeSinceEpoch

    #: Size in bytes
    size: float

    type_: str

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['name'] = self.name
        json['lastModified'] = self.last_modified.to_json()
        json['size'] = self.size
        json['type'] = self.type_
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> File:
        return cls(
            name=str(json['name']),
            last_modified=network.TimeSinceEpoch.from_json(json['lastModified']),
            size=float(json['size']),
            type_=str(json['type']),
        )


@dataclass
class Directory:
    name: str

    nested_directories: typing.List[str]

    #: Files that are directly nested under this directory.
    nested_files: typing.List[File]

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['name'] = self.name
        json['nestedDirectories'] = [i for i in self.nested_directories]
        json['nestedFiles'] = [i.to_json() for i in self.nested_files]
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Directory:
        return cls(
            name=str(json['name']),
            nested_directories=[str(i) for i in json['nestedDirectories']],
            nested_files=[File.from_json(i) for i in json['nestedFiles']],
        )


@dataclass
class BucketFileSystemLocator:
    #: Storage key
    storage_key: storage.SerializedStorageKey

    #: Path to the directory using each path component as an array item.
    path_components: typing.List[str]

    #: Bucket name. Not passing a ``bucketName`` will retrieve the default Bucket. (https://developer.mozilla.org/en-US/docs/Web/API/Storage_API#storage_buckets)
    bucket_name: typing.Optional[str] = None

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['storageKey'] = self.storage_key.to_json()
        json['pathComponents'] = [i for i in self.path_components]
        if self.bucket_name is not None:
            json['bucketName'] = self.bucket_name
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> BucketFileSystemLocator:
        return cls(
            storage_key=storage.SerializedStorageKey.from_json(json['storageKey']),
            path_components=[str(i) for i in json['pathComponents']],
            bucket_name=str(json['bucketName']) if json.get('bucketName', None) is not None else None,
        )


def get_directory(
        bucket_file_system_locator: BucketFileSystemLocator
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,Directory]:
    '''
    :param bucket_file_system_locator:
    :returns: Returns the directory object at the path.
    '''
    params: T_JSON_DICT = dict()
    params['bucketFileSystemLocator'] = bucket_file_system_locator.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'FileSystem.getDirectory',
        'params': params,
    }
    json = yield cmd_dict
    return Directory.from_json(json['directory'])