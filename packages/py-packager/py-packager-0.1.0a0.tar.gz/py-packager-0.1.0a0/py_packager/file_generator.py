
from .collectors import *
from datetime import datetime
from importlib_resources import files, read_text
# Reads contents with UTF-8 encoding and returns str.
import json
import os

class FileGenerator():
    def generate_manifest(self):
        with open("MANIFEST.in", "w") as f:
            content = files('py_packager').joinpath('data/MANIFEST.in').read_text()            
            f.writelines(content) 
            f.close()

    def generate_readme(self):
        with open("README.rst", "w") as f:            
            content = files('py_packager').joinpath('data/README.rst').read_text()            
            f.writelines(content) 
            f.close()

    def generate_requirements(self):
        with open("requirements.txt", "w") as f:
            content = files('py_packager').joinpath('data/requirements.txt').read_text()            
            f.writelines(content) 
            f.close()

    def generate_folders(self, prompts):
        name = ""
        for x in prompts:
            if x.key == 'name':
                name = x.answer
        if not os.path.exists("./" + name):
            os.makedirs("./" + name)

        if not os.path.exists("./tests"):
            os.makedirs("./tests")

        if not os.path.exists("./docs"):
            os.makedirs("./docs")

    def generate_setup(self, prompts: list):
        with open("setup-test.py", "w") as f:
            # write first part
            content = files('py_packager').joinpath('data/setup').read_text()            
            f.writelines(content)  

            package_details = {}
            for x in prompts:
                package_details[x.key] = x.answer
                if x.key == 'name':
                    package_details['packages'] = [x.answer]
            
            f.write(json.dumps(package_details, sort_keys=True, indent=4))

            # write 2nd part            
            content = files('py_packager').joinpath('data/setup_2').read_text()            
            f.writelines(content)                  
            f.close()
        

    def generate_license(self, prompts):
        # value for key, name and year
        name = ""
        key = ""
        for x in prompts:
            if x.key == 'license':
                key = x.answer
            if x.key == 'author':
                name = x.answer
        year = str(datetime.now().year)

        license_object = self.__get_license_by_key(key)

        if 'body' in license_object:
            with open('LICENSE', 'w') as f:
                content = license_object['body']
                formatted = content.replace('[year]', str(datetime.now().year)).replace('[fullname]', name)
                f.writelines(formatted)
                f.close()
        else:
            # no license found
            print('Could kind license by key at (https://api.github.com/licenses): ' + key)


    # Downloads license information based on provided key
    def __get_license_by_key(self, key):
          
        import requests
        
        response = requests.get('https://api.github.com/licenses/' + key)
        return json.loads(response.text)


    def generate(self, prompts: list):
        self.generate_setup(prompts)
        self.generate_license(prompts)
        self.generate_folders(prompts)
        self.generate_readme()
        self.generate_manifest()
        self.generate_requirements()
    