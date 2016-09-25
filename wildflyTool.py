import sys
import os
import os.path
import shutil
import subprocess

class WildflyTool(object):

    def __init__(self, params):
        self.loadPropertiesFile()
        
    def start(self):
        if not self.checkFiles():
            print "Missing files"
            return
        if self.hasFileToDeploy():
            print "Deploying..."
            self.deploy()
            self.cleanup()
        pass

    def loadPropertiesFile(self):
        self.workFolder = "/opt/wildfly/autodeployer"
        self.wildflyRoot = "/opt/wildfly/wildfly-10.0.0.Final"
        self.uploadFolder = self.workFolder + "/upload"
        self.earFile = "mutitenant-poc-ear.ear"

    def checkFiles(self):
        if (not os.path.isdir(self.wildflyRoot)):
            print "The wildfly root is not a directory!"
            return False
        if (not os.path.isdir(self.uploadFolder)):
            print "The upload folder is not a directory!"
            return False
        if (not os.path.isdir(self.workFolder)):
            print "The work folder is not a directory!"
            return False
        return True

    def hasFileToDeploy(self):
        if not (os.path.isfile(self.uploadFolder + "/" + self.earFile)):
            print "No ear file found"
            return False
        self.copyEarToWorkFolder()
        return True

    def copyEarToWorkFolder(self):
        try:
            shutil.copy(self.uploadFolder + "/" + self.earFile, self.workFolder + "/" + self.earFile)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
        # TODO CRC check

    def runWildflyCommand(self, command):
        print "Run command: " + command
        subprocess.call(["sh", self.wildflyRoot + "/bin/jboss-cli.sh", "--connect", "--command=" + command]);

    def deploy(self):
        # undeploy
        self.runWildflyCommand("undeploy " + self.earFile)
        
        # deploy
        self.runWildflyCommand("deploy " + self.workFolder + "/" + self.earFile)
        pass

    def cleanup(self):
        os.remove(self.workFolder + "/" + self.earFile)
        os.remove(self.uploadFolder + "/" + self.earFile)
        