# -Speaker-recognition-Asterisk-
 Speaker recognition for Asterisk 
 
# Get Started

The python file called with EAGI use the File Descriptor to get the audio in realtime
It also perform a simple Voice Activity Detection to detect start of the speech

Dependencies:

flac >= 1.2.1 
libflac-dev >= 1.2.1  
libsndfile >= 1.0.21  
libsndfile-dev >= 1.0.21  
audiolab >= 0.11.0  

Install Debian dists:  
apt-get install libflac-dev  
apt-get install flac  
apt-get install python-numpy  
apt-get install python-scipy  
apt-get install python-dev python-setuptools libsndfile-dev  


Download and install audiolab from:  
http://pypi.python.org/pypi/scikits.audiolab/  

Directory needed in /res to launch the application 
.  
├── ASV_resources  
│   ├── Audio  
│   ├── Models  
│   ├── Params  
│   │   ├── dctbases.mat  
│   │   ├── filterbank.mat  
│   │   └── params.mat  
│   └── UBM  
│       └── ubm.mat  
├── enroll.elf  
├── ID_Models  
│   ├── 596  
│   │   ├── mu.bin  
│   │   ├── sigma.bin  
│   │   └── w.bin  
│   └── 668  
│       ├── mu.bin  
│       ├── sigma.bin  
│       └── w.bin  
└── test.elf  

The speaker binary is not present in this repository  



# Usefull Links

* Asterisk: 
  1. http://www.asterisk.org/
* Git
  1. http://rogerdudler.github.io/git-guide/
* Markdown
  1. https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet


