#
# SPDX-License-Identifier: Apache-2.0
#
# Copyright 2020 Andrey Pleshakov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from unittest.mock import NonCallableMock

from thespiae.install.core import ExeInstallHandler, MSIInstallHandler, CommandInstallHandler, SoftwareProcessor, \
    ExeUninstallHandler, MSIUninstallHandler, CommandUninstallHandler, FileInstallHandler, FileUninstallHandler, \
    ArchiveInstallHandler, ArchiveUninstallHandler
from thespiae.install.system import InstallManager, DownloadManager

install_manager = NonCallableMock(spec_set=InstallManager)
download_manager = NonCallableMock(spec_set=DownloadManager)
exe_install_handler = ExeInstallHandler(install_manager)
msi_install_handler = MSIInstallHandler(install_manager)
command_install_handler = CommandInstallHandler(install_manager)
file_install_handler = FileInstallHandler(install_manager)
exe_uninstall_handler = ExeUninstallHandler(install_manager)
msi_uninstall_handler = MSIUninstallHandler(install_manager)
command_uninstall_handler = CommandUninstallHandler(install_manager)
file_uninstall_handler = FileUninstallHandler(install_manager)
archive_install_handler = ArchiveInstallHandler(install_manager)
archive_uninstall_handler = ArchiveUninstallHandler(install_manager)
software_processor = SoftwareProcessor(download_manager, [exe_install_handler,
                                                          msi_install_handler,
                                                          command_install_handler,
                                                          file_install_handler,
                                                          archive_install_handler],
                                       [exe_uninstall_handler,
                                        msi_uninstall_handler,
                                        command_uninstall_handler,
                                        file_uninstall_handler,
                                        archive_uninstall_handler])

real_download_manager = DownloadManager()
real_install_manager = InstallManager()
