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

from .core import ExeInstallHandler, MSIInstallHandler, CommandInstallHandler, SoftwareProcessor, ExeUninstallHandler, \
    MSIUninstallHandler, CommandUninstallHandler, FileInstallHandler, FileUninstallHandler, ArchiveInstallHandler, \
    ArchiveUninstallHandler
from .system import InstallManager, DownloadManager

install_manager = InstallManager()
download_manager = DownloadManager()
software_processor = SoftwareProcessor(download_manager, [ExeInstallHandler(install_manager),
                                                          MSIInstallHandler(install_manager),
                                                          CommandInstallHandler(install_manager),
                                                          FileInstallHandler(install_manager),
                                                          ArchiveInstallHandler(install_manager)],
                                       [ExeUninstallHandler(install_manager),
                                        MSIUninstallHandler(install_manager),
                                        CommandUninstallHandler(install_manager),
                                        FileUninstallHandler(install_manager),
                                        ArchiveUninstallHandler(install_manager)])
