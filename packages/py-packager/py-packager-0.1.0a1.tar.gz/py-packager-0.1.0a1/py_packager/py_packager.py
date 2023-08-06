from cmd import Cmd
from .file_generator import *
from .collectors import PackageAuthorEmailCollector, PackageAuthorNameCollector, \
        PackageDescriptionCollector, PackageLicenseCollector, PackageNameCollector, \
        PackageUrlCollector, PackageVersionCollector

class PyPackager(Cmd):
    intro = "Welcome to py packager! Please follow the instruction to generate package structure. "

    prompts = [
        PackageNameCollector(),
        PackageVersionCollector(),
        PackageDescriptionCollector(),
        PackageUrlCollector(),
        PackageAuthorNameCollector(),
        PackageAuthorEmailCollector(),
        PackageLicenseCollector()
    ]
    index = 0
    prompt = 'pkgr > ' + prompts[index].question + ' => '
    files = [
        "setup.py",
        "requirements.py",
        "README.rst",
        "MANIFEST.in"
        "LICENSE"        
    ]
    _generator = FileGenerator()

    def precmd(self, line): 
        return line

    def postcmd(self, stop, line):
        if self.index < len(self.prompts):
            self.prompt = 'pkgr > ' + self.prompts[self.index].question + ' => '  
        return stop
    
    def preloop(self):
        pass
    
    def default(self, inp):
        self.prompts[self.index].answer = inp
        self.index += 1
        
        if self.index >= len(self.prompts):
            print('Generating structure ..... ')
            self._generator.generate(self.prompts)
            print('Done')
            return True
    