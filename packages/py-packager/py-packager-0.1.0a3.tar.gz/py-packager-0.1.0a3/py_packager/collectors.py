import os
from abc import ABC, abstractmethod

class ValueCollector(ABC):

    question = ""
    answer = ""
    key = ""
    
    @abstractmethod
    def collect(self, inp):
        pass
        
    def get_default(self) -> str:
        return ""

    def generate(self):
        pass


class PackageNameCollector(ValueCollector):
    question = "Name of the package?"
    key = 'name'
    def collect(self, inp):
        return super().collect(inp)

    def get_default(self):
        return os.path.basename(os.getcwd())

class PackageVersionCollector(ValueCollector):
    question = "Package version?"
    key = 'version'
    def collect(self, inp):
        return super().collect(inp)

class PackageDescriptionCollector(ValueCollector):
    question = "Description?"
    key = 'description'
    def collect(self, inp):
        return super().collect(inp)

class PackageUrlCollector(ValueCollector):    
    question = "Repository Url?"
    key = 'url'
    def collect(self, inp):
        return super().collect(inp)

class PackageAuthorNameCollector(ValueCollector):
    question = "Author?"
    key = 'author'
    def collect(self, inp):
        return super().collect(inp)

class PackageAuthorEmailCollector(ValueCollector):
    question = "Author Email"
    key = 'author_email'
    def collect(self, inp):
        return super().collect(inp)

class PackageLicenseCollector(ValueCollector):
    question = "License?"
    key = 'license'
    def collect(self, inp):
        return super().collect(inp)