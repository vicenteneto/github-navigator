from datetime import datetime


class BaseModel(object):
    """
    Base class from which all Github models will inherit.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_dict(cls, data):
        """
        Create a new instance based on a JSON dict.

        :param data: A JSON dict, as converted from the JSON in the Github API.
        :return: The created instance.
        """
        return cls(**data)


class Commit(BaseModel):
    """
    Class to parse GitHub commit.
    """

    @classmethod
    def from_dict(cls, data):
        data['commit'] = CommitInfo.from_dict(data['commit'])
        return Commit(**data)


class CommitInfo(BaseModel):
    """
    Class to parse Github commit info.
    """

    @classmethod
    def from_dict(cls, data):
        data['author'] = User.from_dict(data['author'])
        return CommitInfo(**data)


class Repository(BaseModel):
    """
    Class to parse GitHub repository.
    """

    @classmethod
    def from_dict(cls, data):
        data['owner'] = User.from_dict(data['owner'])
        data['created_at'] = datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        return Repository(**data)


class User(BaseModel):
    """
    Class to parse GitHub user.
    """
