#define AppVersion "0.12.1"
#define AppPublisher "timatama01-code"
#define AppURL "https://github.com/timatama01-code/diffuse"
#ifndef AppDistRoot
  #define AppDistRoot "..\..\dist"
#endif

[Setup]
AppId={{0C81D89C-0A53-4A16-8DE8-4F7B6800992B}
AppName=Diffuse
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}/issues
DefaultDirName={localappdata}\Programs\Diffuse
DefaultGroupName=Diffuse
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
Compression=lzma2/ultra64
SolidCompression=yes
OutputDir={#AppDistRoot}\installer
OutputBaseFilename=Diffuse-{#AppVersion}-Windows-x64-Setup
SetupIconFile=..\..\windows-installer\diffuse.ico
UninstallDisplayIcon={app}\Diffuse.exe
WizardStyle=modern

[Files]
Source: "{#AppDistRoot}\Diffuse\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\Diffuse"; Filename: "{app}\Diffuse.exe"

[Run]
Filename: "{app}\Diffuse.exe"; Description: "Launch Diffuse"; Flags: nowait postinstall skipifsilent
