import yorm


@yorm.sync("data/{self.owner}/{self.repo}.yml")
class Project(object):
    pass
