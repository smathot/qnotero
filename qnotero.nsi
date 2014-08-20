; This file is part of Qnotero.

; Qnotero is free software: you can redistribute it and/or modify
; it under the terms of the GNU General Public License as published by
; the Free Software Foundation, either version 3 of the License, or
; (at your option) any later version.

; Qnotero is distributed in the hope that it will be useful,
; but WITHOUT ANY WARRANTY; without even the implied warranty of
; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
; GNU General Public License for more details.

; You should have received a copy of the GNU General Public License
; along with Qnotero.  If not, see <http://www.gnu.org/licenses/>.

; USAGE
; -----
; This script assumes that the binary is located in
; 	C:\Users\Dévélõpe®\Documents\gît\Qnotero\dist
;
; The extension FileAssociation.nsh must be installed. This can be
; done by downloading the script from the link below and copying it
; to a file named FileAssociation.nsh in the Include folder of NSIS.

; For each new release, adjust the PRODUCT_VERSION as follows:
; 	version-win32-package#

; After compilation, rename the .exe file to (e.g.)
; 	qnotero_{PRODUCT_VERSION}.exe

; This script must be ANSI encoded.

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "Qnotero"
!define PRODUCT_VERSION "1.0.0-win32-1"
!define PRODUCT_PUBLISHER "Sebastiaan Mathot"
!define PRODUCT_WEB_SITE "http://www.cogsci.nl/qnotero"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

; MUI 1.67 compatible ------
!include "MUI.nsh"
!include "FileAssociation.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "C:\Users\Dévélõpe®\Documents\gît\Qnotero\data\qnotero.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!define MUI_FINISHPAGE_RUN "qnotero.exe"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "qnotero_X-win32-X.exe"
InstallDir "$PROGRAMFILES\Qnotero"
ShowInstDetails hide
ShowUnInstDetails hide

Section "Qnotero" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite try
  File /r "C:\Users\Dévélõpe®\Documents\gît\Qnotero\dist\*.*"
SectionEnd

Section -AdditionalIcons
  WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  CreateDirectory "$SMPROGRAMS\Qnotero"
  CreateShortCut "$SMPROGRAMS\Qnotero\Qnotero.lnk" "$INSTDIR\qnotero.exe" "" "$INSTDIR\data\qnotero.ico"
  CreateShortCut "$SMPROGRAMS\Qnotero\Website.lnk" "$INSTDIR\${PRODUCT_NAME}.url"
  CreateShortCut "$SMPROGRAMS\Qnotero\Uninstall.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd

Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  Delete "$SMPROGRAMS\Qnotero\Qnotero.lnk"
  Delete "$SMPROGRAMS\Qnotero\Qnotero (runtime).lnk"
  Delete "$SMPROGRAMS\Qnotero\Website.lnk"
  Delete "$SMPROGRAMS\Qnotero\Uninstall.lnk"
  RMDir "$SMPROGRAMS\Qnotero"
  RMDir /r "$INSTDIR"  
  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  SetAutoClose true
SectionEnd
