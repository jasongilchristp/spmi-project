from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = '-e .'

def get_requirements(file_path:str)-> List[str]:
    '''
    This function will retrurn the requirements
    '''
    requirements =[]
    with open(file_path)  as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements] ## Replacing /n with blank

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements


setup(
    name="mproject",
    version="0.0.1",
    author="P Jason Gilchrist",
    author_email="jason.gilchrist.p@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)