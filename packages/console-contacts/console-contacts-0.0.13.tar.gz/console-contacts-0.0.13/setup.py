from setuptools import setup, find_packages 
  
long_description = "console contacts\n======\n\nA simple python app for you to manage your contacts. Tested on python 3,\nprobably not compatible with python 2. \n\nInstallation\n------------\n\nFast install:\n\n::\n\n    pip install console-contacts  \n\nExamples\n--------\n\n:: console-contacts -l\n\nHere is the output:\ncontactName1\ncontactName2\ncontactName3\ncontactName4\n:: console-contacts -s Mary\nOutput:\nMary\nmary@example.com\n1234567890\n\n:: console-contacts -a Bob bob@example.com 0987654321\n\nThis adds a contact with the name Bob, the email bob@example.com, and the phone number 0987654321\n\n:: console-contacts -r Bob bob@example.com\n\nThis removes Bob from your contacts "
  
  
# specify requirements of your package here 
REQUIREMENTS = [] 
  
# some more details 
CLASSIFIERS = [ 
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6', 
    ]

setup(
    name ='console-contacts', 
    version ='0.0.13', 
    author ='Kai Harris', 
    description ='CLI contacts manager', 
    long_description = long_description, 
    long_description_content_type ="text/markdown", 
    license ='MIT',
    entry_points = {
        'console_scripts': ['console-contacts=contacts.command_line:main']
    },
    packages = find_packages(), 
    classifiers = CLASSIFIERS,
    keywords ='console cli contacts contact addressbook', 
    install_requires = REQUIREMENTS, 
    zip_safe = False
)