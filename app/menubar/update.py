import platform
import re
import subprocess
import urllib.request as request

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialog

from app.func import Func
from app.info import Info


class Update(QDialog):
    def __init__(self, parent=None):
        super(Update, self).__init__(parent=parent)

        self.setWindowTitle("Quick Update")
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(QIcon(Func.getImage("common/icon.png")))

        self.label = QLabel("The current version is the latest version.")
        self.label.setOpenExternalLinks(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.label.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
        if Info.OS_TYPE == 0:
            self.setMinimumSize(400, 60)
        else:
            self.setMinimumSize(400, 100)
        # self.setFixedSize(600, 100)

    def show(self):
        self.getLatestVersion()
        super(Update, self).show()

    def showGui(self):
        super(Update, self).show()

    @staticmethod
    def netCheck():
        if Info.OS_TYPE == 2:
            # for mac or linux
            result = subprocess.getstatusoutput('ping -c 1 -w 1 www.baidu.com')
        elif Info.OS_TYPE == 1:
            result = subprocess.getstatusoutput('ping -c 1 -t 1 www.baidu.com')
        else:
            result = subprocess.getstatusoutput('ping -n 1 -w 1 www.baidu.com')

        return not(result[0])

    def getLatestVersion(self):
        version_info = "The current version is the latest version."
        #############
        # get latest version information
        url = "https://yzhangpsy.myds.me:8001"
        # url = "www.psybuilder.com/psybuilderVersion.html"

        hasNewVersion = False

        if self.netCheck():
            try:
                res = request.urlopen(url, None, 5)

                if platform.system() == "Windows":
                    versionList = re.findall(r'PsyBuilder(\d+)Win', res.read().decode('utf-8'))
                elif platform.system() == "Darwin":
                    versionList = re.findall(r'PsyBuilder(\d+).dmg', res.read().decode('utf-8'))
                else:
                    versionList = re.findall(r'PsyBuilder(\d+).deb', res.read().decode('utf-8'))

                if versionList:

                    max_date_Str = max(versionList)

                    if Info.LAST_MODIFY_DATE < float(max_date_Str):
                        version_info = f"Running version: {Info.LAST_MODIFY_DATE}<br>An update is available (release time: {max_date_Str})<br>Click<a href ='https://www.psybuilder.com'> me</a> to get the update."
                        hasNewVersion = True
                    else:
                        version_info = f"You are running the latest version of PsyBuilder ({Info.LAST_MODIFY_DATE}) \n Please check back again for updates at a later time."

                else:
                    version_info = "Failed to get PsyBuilder version info, please try it later."

            except:
                version_info = "Failed to consult PsyBuilder website, please try it later."

        else:
            version_info = "Network connection error, please try again later."
        #############
        self.label.setText(version_info)

        return hasNewVersion
